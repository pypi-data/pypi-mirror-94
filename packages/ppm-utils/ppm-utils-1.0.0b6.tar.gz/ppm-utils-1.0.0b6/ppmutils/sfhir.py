import collections
import requests
import json
import uuid
from furl import furl, Query
import random
import re
import base64
from dateutil.parser import parse
from dateutil.tz import tz
from datetime import datetime

from fhirclient.client import FHIRClient
from fhirclient.models.fhirdate import FHIRDate
from fhirclient.models.period import Period
from fhirclient.models.patient import Patient
from fhirclient.models.flag import Flag
from django.utils.safestring import mark_safe
from fhirclient.models.bundle import Bundle, BundleEntry, BundleEntryRequest
from fhirclient.models.list import List, ListEntry
from fhirclient.models.organization import Organization
from fhirclient.models.documentreference import DocumentReference
from fhirclient.models.researchstudy import ResearchStudy
from fhirclient.models.researchsubject import ResearchSubject
from fhirclient.models.fhirreference import FHIRReference
from fhirclient.models.codeableconcept import CodeableConcept
from fhirclient.models.coding import Coding
from fhirclient.models.communication import Communication
from fhirclient.models.device import Device
from fhirclient.models.resource import Resource

from ppmutils.ppm import PPM
from ppmutils.settings import ppm_settings

# Get the app logger
import logging

logger = logging.getLogger(ppm_settings.LOGGER_NAME)


class FHIR(PPM.Service):

    service = "fhir"
    ppm_settings_url_name = "FHIR_URL"
    proxied = True

    #
    # CONSTANTS
    #

    # This is the system used for Patient identifiers based on email
    patient_email_identifier_system = "http://schema.org/email"
    patient_email_telecom_system = "email"
    patient_phone_telecom_system = "phone"
    patient_twitter_telecom_system = "other"

    # Set the coding types
    patient_identifier_system = "https://peoplepoweredmedicine.org/fhir/patient"
    enrollment_flag_coding_system = "https://peoplepoweredmedicine.org/enrollment-status"

    research_study_identifier_system = "https://peoplepoweredmedicine.org/fhir/study"
    research_study_coding_system = "https://peoplepoweredmedicine.org/study"

    research_subject_identifier_system = "https://peoplepoweredmedicine.org/fhir/subject"
    research_subject_coding_system = "https://peoplepoweredmedicine.org/subject"

    device_identifier_system = "https://peoplepoweredmedicine.org/fhir/device"
    device_coding_system = "https://peoplepoweredmedicine.org/device"

    # Type system for PPM data documents
    data_document_reference_identifier_system = "https://peoplepoweredmedicine.org/document-type"

    # Type system for PPM documents
    ppm_document_reference_type_system = "https://peoplepoweredmedicine.org/fhir/ppm/document-type"

    # Type system for PPM consent resources
    ppm_consent_type_system = "http://loinc.org"
    ppm_consent_type_value = "83930-8"
    ppm_consent_type_display = "Research Consent"

    # Point of care codes
    SNOMED_LOCATION_CODE = "SNOMED:43741000"
    SNOMED_VERSION_URI = "http://snomed.info/sct/900000000000207008"

    # PicnicHealth notification flags
    ppm_comm_identifier_system = "https://peoplepoweredmedicine.org/fhir/communication"
    ppm_comm_coding_system = "https://peoplepoweredmedicine.org/ppm-notification"

    # Patient extension flags
    twitter_extension_url = "https://p2m2.dbmi.hms.harvard.edu/fhir/StructureDefinition/uses-twitter"
    fitbit_extension_url = "https://p2m2.dbmi.hms.harvard.edu/fhir/StructureDefinition/uses-fitbit"
    picnichealth_extension_url = "https://p2m2.dbmi.hms.harvard.edu/fhir/" "StructureDefinition/registered-picnichealth"
    facebook_extension_url = "https://p2m2.dbmi.hms.harvard.edu/fhir/StructureDefinition/uses-facebook"
    smart_on_fhir_extension_url = "https://p2m2.dbmi.hms.harvard.edu/fhir/StructureDefinition/uses-smart-on-fhir"
    referral_extension_url = "https://p2m2.dbmi.hms.harvard.edu/fhir/" "StructureDefinition/how-did-you-hear-about-us"
    admin_notified_extension_url = "https://p2m2.dbmi.hms.harvard.edu/fhir/StructureDefinition/admin-notified"

    # Qualtrics IDs
    qualtrics_survey_identifier_system = "https://peoplepoweredmedicine.org/fhir/qualtrics/survey"
    qualtrics_response_identifier_system = "https://peoplepoweredmedicine.org/fhir/qualtrics/response"

    #
    # META
    #

    @classmethod
    def service_url(cls):
        """
        FHIR uses a more standard URL for everything so use this one instead of
        the PPM service stripped down one
        :return: The FHIR URL
        :rtype: str
        """

        # Get from ppm settings
        if not hasattr(ppm_settings, cls.ppm_settings_url_name):
            raise SystemError("FHIR URL not defined in settings".format(cls.service.upper()))

        # Get it
        return getattr(ppm_settings, cls.ppm_settings_url_name)

    @staticmethod
    def get_client(fhir_url):

        # Create the server
        settings = {"app_id": "hms-dbmi-ppm-p2m2-admin", "api_base": fhir_url}

        return FHIRClient(settings=settings)

    @staticmethod
    def _bundle_get(bundle, resource_type, query={}):
        """
        Searches through a bundle for the resource matching the given resourceType
        and query, if passed,
        """

        # Get matching resources
        resources = [entry.resource for entry in bundle.entry if entry.resource.resource_type == resource_type]

        # Match
        for resource in resources:
            for key, value in query:
                attribute = FHIR._get_attribute_or(resource, key)

                # Compare
                if not attribute or attribute != value:
                    break

            # All comparisons passed
            return resource

            return None

    @staticmethod
    def _find_resources(obj, resource_type=None):
        """
        Accepts an arbitrary FHIR object (Bundle, Resource, dict, FHIRResource)
        and returns either the FHIRResources or the immediate resource dicts
        matching the resource type
        :param obj: A bundle or list or resource as a dict or FHIRResource
        :param resource_type: If multiple resources exist, only return these types
        :return: list
        """
        # Check for valid object
        if not obj:
            logger.warning('FHIR: Attempt to extract resource from nothing: "{}"'.format(obj))
            return None

        # Check type
        if isinstance(obj, Resource):

            # Check if in a search bundle
            if type(obj) is Bundle:

                # Get entries
                return FHIR._find_resources(obj.entry, resource_type=resource_type)

            else:

                # Object is resource, return it
                return [obj.as_json()] if not resource_type or obj.resource_type == resource_type else []

        # Check if is a search bundle entry
        if type(obj) is BundleEntry:

            # Return its resource
            return FHIR._find_resources(obj.resource, resource_type=resource_type)

        if type(obj) is list:

            # Get all matching resources
            resources = []
            for r in obj:
                resources.extend(FHIR._find_resources(r, resource_type=resource_type))

            return resources

        if type(obj) is dict:

            # Check for bundle
            if obj.get("resourceType") == "Bundle" and obj.get("entry"):

                # Call this with bundle entries
                return FHIR._find_resources(obj["entry"], resource_type=resource_type)

            # Check for bundle entry
            elif obj.get("resource") and obj.get("fullUrl"):

                # Call this with resource
                return FHIR._find_resources(obj["resource"], resource_type=resource_type)

            elif obj.get("resourceType"):

                # Object is a resource, return it
                return [obj] if not resource_type or obj["resourceType"] == resource_type else []

            else:
                logger.warning(
                    "FHIR: Requested resource as FHIRClient Resource but did not supply"
                    "valid Resource subclass to construct with"
                )

        return []

    @staticmethod
    def _find_resource(obj, resource_type=None):
        """
        Accepts an arbitrary FHIR object (Bundle, Resource, dict, FHIRResource)
        and returns either the first resource found of said type
        :param obj: A bundle or list or resource as a dict or FHIRResource
        :param resource_type: The resource type we are looking for
        :return: object
        """
        return next(iter(FHIR._find_resources(obj, resource_type)), None)

    @staticmethod
    def _get_resources(bundle, resource_type, query=None):
        """
        Searches through a bundle for the resource matching the given resourceType
        and query, if passed,
        """
        # Check type
        if type(bundle) is Bundle:
            bundle = bundle.as_json()
        elif type(bundle) is not dict:
            raise ValueError("Bundle must either be Bundle or dict")

        # Collect resources
        matches = []

        # Get matching resources
        resources = [
            entry["resource"] for entry in bundle["entry"] if entry["resource"]["resourceType"] == resource_type
        ]

        # Match
        for resource in resources:

            # Check query
            matched = query is None

            if query:
                for key, value in query:
                    attribute = FHIR._get_or(resource, key)

                    # Compare
                    if not attribute or attribute != value:
                        matched = False
                        break

            # All comparisons passed
            if matched:
                matches.append(resource)

        return matches

    @staticmethod
    def _get_or(item, keys, default=""):
        """
        Fetch a property from a json object. Keys is a list of keys and indices
        to use to fetch the property. Returns the passed default string if the
        path through the json does not exist.
        :param item: The json to parse properties from
        :type item: json object
        :param keys: The list of keys and indices for the property
        :type keys: A list of string or int
        :param default: The default string to use if a property could not be found
        :type default: String
        :return: The requested property or the default value if missing
        :rtype: String
        """
        try:
            # Try it out.
            for key in keys:
                item = item[key]

            return item
        except (KeyError, IndexError):
            return default

    @staticmethod
    def _get_referenced_id(resource, resource_type, key=None):
        """
        Checks a resource JSON and returns any ID reference for the given resource
        type. If 'key' is passed, that will be forced, if anything is present or not.
        :param resource: The resource JSON to check
        :type resource: dict
        :param resource_type: The type of the referenced resource
        :type resource_type: str
        :param key: The resource key to check for the reference
        :type key: str
        :return: The requested referenced resources ID or None
        :rtype: str
        """
        try:
            # Try it out.
            if key and resource.get(key, {}).get("reference"):
                return resource[key]["reference"].replace(f"{resource_type}/", "")

            else:
                # Find it
                for key, value in resource.items():
                    if type(value) is dict and value.get("reference") and resource_type in value.get("reference"):
                        return value["reference"].replace(f"{resource_type}/", "")

        except (KeyError, IndexError) as e:
            logger.exception(
                "FHIR Error: {}".format(e),
                exc_info=True,
                extra={
                    "resource_type": resource_type,
                    "key": key,
                },
            )

        else:
            logger.warning(f'FHIR Error: No reference found for "{resource_type}"')

        return None

    @staticmethod
    def _get_attribute_or(item, keys, default=None):
        """
        Fetch an attribute from an object. Keys is a list of attribute names and
        indices to use to fetch the property. Returns the passed default object
        if the path through the object does not exist.
        :param item: The object to get from
        :type item: object
        :param keys: The list of keys and indices for the property
        :type keys: A list of string or int
        :param default: The default object to use if a property could not be found
        :type default: object
        :return: The requested property or the default value if missing
        :rtype: object
        """
        try:
            # Try it out.
            for key in keys:

                # Check for integer or string
                if type(key) is str:
                    item = getattr(item, key)

                elif type(key) is int:
                    item = item[key]

            return item
        except (AttributeError, IndexError):
            return default

    @staticmethod
    def _get_resource_type(bundle):

        # Check for entries
        if bundle.get("entry") and len(bundle.get("entry", [])) > 0:
            return bundle["entry"][0]["resource"]["resourceType"]

        logger.error("Could not determine resource type: {}".format(bundle))
        return None

    @staticmethod
    def _get_next_url(bundle, relative=False):

        # Get the next URL
        next_url = next((link["url"] for link in bundle["link"] if link["relation"] == "next"), None)
        if next_url:

            # Check URL type
            if relative:

                # We only want the resource type and the parameters
                resource_type = bundle["entry"][0]["resource"]["resourceType"]

                return "{}?{}".format(resource_type, next_url.split("?", 1)[1])

            else:
                return next_url

        return None

    @staticmethod
    def _fix_bundle_json(bundle_json):
        """
        Random tasks to make FHIR resources compliant. Some resources from early-on
        were'nt strictly compliant and would throw exceptions when building
        FHIRClient objects. This takes the json and adds needed properties/attributes.
        :param bundle_json: FHIR Bundle json from server
        :return: json
        """

        # Appeases the FHIR library by ensuring question items all have linkIds,
        # regardless of an associated answer.
        for question in [
            entry["resource"] for entry in bundle_json["entry"] if entry["resource"]["resourceType"] == "Questionnaire"
        ]:
            for item in question["item"]:
                if "linkId" not in item:
                    # Assign a random string for the linkId
                    item["linkId"] = "".join([random.choice("abcdefghijklmnopqrstuvwxyz1234567890") for _ in range(10)])

        # Appeases the FHIR library by ensuring document references have 'indexed'
        for document in [
            entry["resource"]
            for entry in bundle_json["entry"]
            if entry["resource"]["resourceType"] == "DocumentReference"
        ]:
            if not document.get("indexed"):
                document["indexed"] = datetime.utcnow().isoformat()

        return bundle_json

    @staticmethod
    def _get_list(bundle, resource_type):
        """
        Finds and returns the list resource for the passed resource type
        :param bundle: The FHIR resource bundle
        :type bundle: Bundle
        :param resource_type: The resource type of the list's contained resources
        :type resource_type: str
        :return: The List resource
        :rtype: List
        """

        # Check the bundle type
        if type(bundle) is dict:
            bundle = Bundle(bundle)

        # Quit early for an empty bundle
        if not bundle.entry:
            return None

        for list in [entry.resource for entry in bundle.entry if entry.resource.resource_type == "List"]:

            # Compare the type
            for item in [entry.item for entry in list.entry]:

                # Check for a reference
                if item.reference and resource_type == item.reference.split("/")[0]:

                    return list

        return None

    @staticmethod
    def is_ppm_research_subject(research_subject):
        """
        Accepts a FHIR ResearchSubject resource and returns whether it's
        related to a PPM study or not
        """
        if (
            research_subject.get("identifier", {}).get("system") == FHIR.research_subject_identifier_system
            and research_subject.get("identifier", {}).get("value") in PPM.Study.identifiers()
        ):

            return True

        return False

    @staticmethod
    def is_ppm_research_study(research_study):
        """
        Accepts a FHIR ResearchStudy resource and returns whether it's related
        to a PPM study or not
        """
        for identifier in research_study.get("identifier", []):
            if (
                identifier.get("system") == FHIR.research_study_identifier_system
                and identifier.get("value") in PPM.Study.identifiers()
            ):

                return True

        # Compare id
        if research_study["id"] in PPM.Study.identifiers():
            return True

        return False

    @staticmethod
    def get_study_from_research_subject(research_subject):
        """
        Accepts a FHIR resource representation (ResearchSubject, dict or bundle entry)
        and parses out the identifier which contains the code of the study this
        belongs too. This is necessary since for some reason DSTU3 does not allow
        searching on ResearchSubject by study, ugh.
        :param research_subject: The ResearchSubject resource
        :type research_subject: object
        :return: The study or None
        :rtype: str
        """

        # Check type and convert the JSON resource
        if type(research_subject) is ResearchSubject:
            research_subject = research_subject.as_json()
        elif type(research_subject) is dict and research_subject.get("resource"):
            research_subject = research_subject.get("resource")
        elif type(research_subject) is not dict or research_subject.get("resourceType") != "ResearchSubject":
            raise ValueError("Passed ResearchSubject is not a valid resource: {}".format(research_subject))

        # Parse the identifier
        identifier = research_subject.get("identifier", {}).get("value")
        if identifier:

            # Split off the 'ppm-' prefix if needed
            if "ppm-" in identifier:
                return identifier.replace("ppm-", "")

            else:
                return identifier

        return None

    @staticmethod
    def _format_date(date_string, date_format):

        try:
            # Parse it
            date = parse(date_string)

            # Set UTC as timezone
            from_zone = tz.gettz("UTC")
            to_zone = tz.gettz("America/New_York")
            utc = date.replace(tzinfo=from_zone)

            # If UTC time was 00:00:00, assume a time was missing and
            # return the date as is so
            # the ET conversion does not change the date.
            if utc.hour == 0 and utc.minute == 0 and utc.second == 0:
                return utc.strftime(date_format)

            # Convert time zone to assumed ET
            et = utc.astimezone(to_zone)

            # Format it and return it
            return et.strftime(date_format)

        except ValueError as e:
            logger.exception(
                "FHIR date parsing error: {}".format(e),
                exc_info=True,
                extra={"date_string": date_string, "date_format": date_format},
            )

            return "--/--/----"

    @staticmethod
    def _patient_query(identifier):
        """
        Accepts an identifier and builds the query for resources related to that
        Patient. Identifier can be a FHIR ID, an email address, or a Patient object.
        Optionally specify the parameter key to be used, defaults to 'patient'.
        :param identifier: object
        :param key: str
        :return: dict
        """
        # Check types
        if type(identifier) is str and re.match(r"^\d+$", identifier):

            # Likely a FHIR ID
            return {"_id": identifier}

        # Check for an email address
        elif type(identifier) is str and re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", identifier):

            # An email address
            return {"identifier": "{}|{}".format(FHIR.patient_email_identifier_system, identifier)}

        # Check for a resource
        elif type(identifier) is dict and identifier.get("resourceType") == "Patient":

            return {"_id": identifier["id"]}

        # Check for a bundle entry
        elif type(identifier) is dict and identifier.get("resource", {}).get("resourceType") == "Patient":

            return {"_id": identifier["resource"]["id"]}

        # Check for a Patient object
        elif type(identifier) is Patient:

            return {"_id": identifier.id}

        else:
            raise ValueError("Unhandled instance of a Patient identifier: {}".format(identifier))

    @staticmethod
    def _patient_id(identifier):
        """
        Accepts an identifier and returns the actual Patient ID
        to 'patient'.
        :param identifier: object
        :return: str
        """
        # Check types
        if type(identifier) is str and re.match(r"^\d+$", identifier):

            # Likely a FHIR ID
            return identifier

        # Check for an email address
        elif type(identifier) is str and re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", identifier):

            # An email address
            return FHIR.get_ppm_id(identifier)

        # Check for a resource
        elif type(identifier) is dict and identifier.get("resourceType") == "Patient":

            return identifier["id"]

        # Check for a bundle entry
        elif type(identifier) is dict and identifier.get("resource", {}).get("resourceType") == "Patient":

            return identifier["resource"]["id"]

        # Check for a bundle
        elif (
            type(identifier) is dict
            and identifier.get("resource", {}).get("resourceType") == "Bundle"
            and FHIR._find_resource(identifier, resource_type="Patient")
        ):

            return FHIR._find_resource(identifier, resource_type="Patient")["id"]

        # Check for a Patient object
        elif type(identifier) is Patient:

            return identifier.id

        else:
            raise ValueError("Unhandled instance of a Patient identifier: {}".format(identifier))

    @staticmethod
    def _patient_resource_query(identifier, key="patient"):
        """
        Accepts an identifier and builds the query for resources related to that
         Patient. Identifier can be a FHIR ID, an email address, or a Patient object.
         Optionally specify the parameter key to be used, defaults to 'patient'.
        :param identifier: object
        :param key: str
        :return: dict
        """
        # Check types
        if type(identifier) is str and re.match(r"^\d+$", identifier):

            # Likely a FHIR ID
            return {key: identifier}

        # Check for an email address
        elif type(identifier) is str and re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", identifier):

            # An email address
            return {
                "{}:patient.identifier".format(key): "{}|{}".format(FHIR.patient_email_identifier_system, identifier)
            }

        # Check for a resource
        elif type(identifier) is dict and identifier.get("resourceType") == "Patient":

            return {key: identifier["id"]}

        # Check for a bundle entry
        elif type(identifier) is dict and identifier.get("resource", {}).get("resourceType") == "Patient":

            return {key: identifier["resource"]["id"]}

        # Check for a Patient object
        elif type(identifier) is Patient:

            return {key: identifier.id}

        else:
            raise ValueError("Unhandled instance of a Patient identifier: {}".format(identifier))

    @staticmethod
    def get_created_resource_id(response, resource_type):
        """
        Accepts a response from a FHIR operation to create a resource and returns
        the ID and URL of the newly created resource in FHIR
        :param response: The raw HTTP response object from FHIR
        :param resource_type: The resource type of the created resource
        :return: str, str
        """
        # Check status
        if not response.ok:
            logger.error(
                f"FHIR Error: Cannot get resource details from a failed response: "
                f"{response.status_code} : {response.content.decode()}"
            )
            return None, None

        try:
            # Get the URL from headers
            url = furl(response.headers.get("Location"))

            # Get ID
            resource_id = url.path.segments[2]

            # Trim off history part
            if len(url.path.segments) > 3:
                url.path.segments = url.path.segments[:3]

            # Return
            return resource_id, url.url

        except Exception as e:
            logger.exception(
                f"FHIR Error: {e}",
                exc_info=True,
                extra={
                    "response": response.content.decode(),
                    "headers": response.headers,
                    "status": response.status_code,
                },
            )

        # Try based off the body of the response
        pattern = rf"{resource_type}\/([0-9]+)\/"
        matches = re.findall(pattern, response.content.decode())
        if matches:
            logger.error(f"FHIR ERROR: Could not determine resource ID from " f"response: {response.content.decode()}")

            # Build URL
            url = furl(PPM.fhir_url())
            url.path.segments.extend([resource_type, matches[0]])

            return matches[0], url.url

        # Could not figure it out
        return None, None

    #
    # CREATE
    #

    @staticmethod
    def create_ppm_research_study(request, project, title):
        """
        Creates a project list if not already created
        """
        research_study_data = FHIR.Resources.ppm_research_study(project, title)

        # Use the FHIR client lib to validate our resource.
        # "If-None-Exist" can be used for conditional create operations in FHIR.
        # If there is already a Patient resource identified by the provided email
        # address, no duplicate records will be created.
        ResearchStudy(research_study_data)

        research_study_request = BundleEntryRequest(
            {
                "url": "ResearchStudy/ppm-{}".format(project),
                "method": "PUT",
                "ifNoneExist": str(
                    Query(
                        {
                            "_id": project,
                        }
                    )
                ),
            }
        )
        research_study_entry = BundleEntry(
            {
                "resource": research_study_data,
            }
        )
        research_study_entry.request = research_study_request

        # Validate it.
        bundle = Bundle()
        bundle.entry = [research_study_entry]
        bundle.type = "transaction"

        logger.debug("Creating...")

        # Create the Patient and Flag on the FHIR server.
        # If we needed the Patient resource id, we could follow the redirect
        # returned from a successful POST operation, and get the id out of the
        # new resource. We don't though, so we can save an HTTP request.
        response = FHIR.post(request=request, path="/", data=bundle.as_json())

        return response.ok

    @staticmethod
    def create_ppm_research_subject(request, project, patient_id):
        """
        Creates a project list if not already created
        """
        # Get the study, or create it
        study = FHIR._query_resource(
            request,
            "ResearchStudy",
            query={"identifier": "{}|{}".format(FHIR.research_study_identifier_system, project)},
        )
        if not study:
            FHIR.create_ppm_research_study(request, project, PPM.Project.title(project))

        # Generate resource data
        research_subject_data = FHIR.Resources.ppm_research_subject(project, "Patient/{}".format(patient_id))

        # Create a placeholder ID for the list.
        research_subject_id = uuid.uuid1().urn

        # Use the FHIR client lib to validate our resource.
        # "If-None-Exist" can be used for conditional create operations in FHIR.
        # If there is already a Patient resource identified by the provided email
        # address, no duplicate records will be created.
        ResearchSubject(research_subject_data)

        research_subject_request = BundleEntryRequest(
            {
                "url": "ResearchSubject",
                "method": "POST",
            }
        )
        research_subject_entry = BundleEntry({"resource": research_subject_data, "fullUrl": research_subject_id})
        research_subject_entry.request = research_subject_request

        # Validate it.
        bundle = Bundle()
        bundle.entry = [research_subject_entry]
        bundle.type = "transaction"

        logger.debug("Creating...")

        # Create the Patient and Flag on the FHIR server.
        # If we needed the Patient resource id, we could follow the redirect
        # returned from a successful POST operation, and get the id out of the
        # new resource. We don't though, so we can save an HTTP request.
        response = FHIR.post(request=request, path="/", data=bundle.as_json())

        return response.ok

    @staticmethod
    def create_ppm_device(request, patient_id, item, identifier=None, shipped=None, returned=None):
        """
        Creates a project list if not already created
        """
        device_data = FHIR.Resources.ppm_device(
            item=item,
            patient_ref="Patient/{}".format(patient_id),
            identifier=identifier,
            shipped=shipped,
            returned=returned,
        )

        # Use the FHIR client lib to validate our resource.
        Device(device_data)

        device_request = BundleEntryRequest(
            {
                "url": "Device",
                "method": "POST",
            }
        )
        device_entry = BundleEntry(
            {
                "resource": device_data,
            }
        )
        device_entry.request = device_request

        # Validate it.
        bundle = Bundle()
        bundle.entry = [device_entry]
        bundle.type = "transaction"

        logger.debug("Creating...")

        # Create the Device on the FHIR server.
        # If we needed the Patient resource id, we could follow the redirect
        # returned from a successful POST operation, and get the id out of the
        # new resource. We don't though, so we can save an HTTP request.
        response = FHIR.post(request=request, path="/", data=bundle.as_json())

        return response.ok

    @staticmethod
    def create_patient(request, form, project):
        """
        Create a Patient resource in the FHIR server.
        """
        # Get the study, or create it
        study = FHIR._query_resource(
            request,
            "ResearchStudy",
            query={"identifier": "{}|{}".format(FHIR.research_study_identifier_system, project)},
        )
        if not study:
            FHIR.create_ppm_research_study(request, project, PPM.Project.title(project))

        # Build out patient JSON
        patient_data = FHIR.Resources.patient(form)

        # Create a placeholder ID for the patient the flag can reference.
        patient_uuid = uuid.uuid1()

        # Use the FHIR client lib to validate our resource.
        # "If-None-Exist" can be used for conditional create operations in FHIR.
        # If there is already a Patient resource identified by the provided email
        # address, no duplicate records will be created.
        Patient(patient_data)

        # Add the UUID identifier
        patient_data.get("identifier", []).append(
            {"system": FHIR.patient_identifier_system, "value": str(patient_uuid)}
        )

        patient_request = BundleEntryRequest(
            {
                "url": "Patient",
                "method": "POST",
                "ifNoneExist": str(
                    Query(
                        {
                            "identifier": "http://schema.org/email|" + form.get("email"),
                        }
                    )
                ),
            }
        )
        patient_entry = BundleEntry({"resource": patient_data, "fullUrl": patient_uuid.urn})
        patient_entry.request = patient_request

        # Build enrollment flag.
        flag = Flag(FHIR.Resources.enrollment_flag(patient_uuid.urn, "registered"))
        flag_request = BundleEntryRequest({"url": "Flag", "method": "POST"})
        flag_entry = BundleEntry({"resource": flag.as_json()})
        flag_entry.request = flag_request

        # Build research subject
        research_subject_data = FHIR.Resources.ppm_research_subject(project, patient_uuid.urn, "candidate")
        research_subject_request = BundleEntryRequest({"url": "ResearchSubject", "method": "POST"})
        research_subject_entry = BundleEntry({"resource": research_subject_data})
        research_subject_entry.request = research_subject_request

        # Validate it.
        bundle = Bundle()
        bundle.entry = [patient_entry, flag_entry, research_subject_entry]
        bundle.type = "transaction"

        # Create the Patient and Flag on the FHIR server.
        # If we needed the Patient resource id, we could follow the redirect
        # returned from a successful POST operation, and get the id out of the
        # new resource. We don't though, so we can save an HTTP request.
        response = FHIR.post(request=request, path="/", data=bundle.as_json())
        # Parse out created identifiers
        for result in response.json():

            # Do something
            logging.debug("Created: {}".format(result))

        return response.ok

    @staticmethod
    def create_patient_enrollment(request, patient_id, status="registered"):
        """
        Create a Flag resource in the FHIR server to indicate a user's enrollment.
        :param patient_id:
        :param status:
        :return:
        """
        logger.debug("Patient: {}".format(patient_id))

        # Use the FHIR client lib to validate our resource.
        flag = Flag(FHIR.Resources.enrollment_flag("Patient/{}".format(patient_id), status))

        # Set a date if enrolled.
        if status == "accepted":
            now = FHIRDate(datetime.now().isoformat())
            period = Period()
            period.start = now
            flag.period = period

        # Build the FHIR Flag destination URL.
        logger.debug("Creating flag")

        response = FHIR.post(request=request, path="/Flag", data=flag.as_json())

        return response

    @staticmethod
    def create_communication(request, patient_id, content, identifier):
        """
        Create a record of a communication to a participant
        :param patient_id:
        :param content: The content of the email
        :param identifier: The identifier of the communication
        :return:
        """
        logger.debug("Patient: {}".format(patient_id))

        # Use the FHIR client lib to validate our resource.
        communication = Communication(
            FHIR.Resources.communication(
                patient_ref="Patient/{}".format(patient_id),
                identifier=identifier,
                content=content,
                sent=datetime.now().isoformat(),
            )
        )

        # Build the FHIR Communication destination URL.
        response = FHIR.post(request=request, path="/Communication", data=communication.as_json())

        return response

    @staticmethod
    def create_research_study(request, patient_id, research_study_title):
        logger.debug("Create ResearchStudy: {}".format(research_study_title))

        # Create temp identifier for the study
        research_study_id = uuid.uuid1().urn

        # Create the organization
        research_study = ResearchStudy()
        research_study.title = research_study_title
        research_study.status = "completed"

        research_study_request = BundleEntryRequest(
            {
                "url": "ResearchStudy",
                "method": "POST",
                "ifNoneExist": str(Query({"title:exact": research_study_title})),
            }
        )

        research_study_entry = BundleEntry({"resource": research_study.as_json(), "fullUrl": research_study_id})

        research_study_entry.request = research_study_request

        research_study_reference = FHIRReference()
        research_study_reference.reference = research_study_id

        patient_reference = FHIRReference()
        patient_reference.reference = "Patient/{}".format(patient_id)

        # Create the subject
        research_subject = ResearchSubject()
        research_subject.study = research_study_reference
        research_subject.individual = patient_reference
        research_subject.status = "completed"

        # Add Research Subject to bundle.
        research_subject_request = BundleEntryRequest()
        research_subject_request.method = "POST"
        research_subject_request.url = "ResearchSubject"

        # Create the Research Subject entry
        research_subject_entry = BundleEntry({"resource": research_subject.as_json()})
        research_subject_entry.request = research_subject_request

        # Validate it.
        bundle = Bundle()
        bundle.entry = [research_study_entry, research_subject_entry]
        bundle.type = "transaction"

        logger.debug("Creating: {}".format(research_study_title))

        response = FHIR.post(request=request, path="/", data=bundle.as_json())

        return response.json()

    @staticmethod
    def create_point_of_care_list(request, patient_id, point_of_care_list):
        """
        Replace current point of care list with submitted list.
        """

        # This is a FHIR resources that allows references between resources.
        # Create one for referencing patients.
        patient_reference = FHIRReference()
        patient_reference.reference = "Patient/" + patient_id

        # The list will hold Organization resources representing where patients
        # have received care.
        data_list = List()

        data_list.subject = patient_reference
        data_list.status = "current"
        data_list.mode = "working"

        # We use the SNOMED code for location to define the context of items added
        # to the list.
        coding = Coding()
        coding.system = FHIR.SNOMED_VERSION_URI
        coding.code = FHIR.SNOMED_LOCATION_CODE

        codeable = CodeableConcept()
        codeable.coding = [coding]

        # Add it
        data_list.code = codeable

        # Start building the bundle. Bundles are used to submit multiple related
        # resources.
        bundle_entries = []

        # Add Organization objects to bundle.
        list_entries = []
        for point_of_care in point_of_care_list:

            # Create the organization
            organization = Organization()
            organization.name = point_of_care
            organization_id = uuid.uuid1().urn

            bundle_item_org_request = BundleEntryRequest()
            bundle_item_org_request.method = "POST"
            bundle_item_org_request.url = "Organization"

            # Don't recreate Organizations if we can find them by the exact name.
            # No fuzzy matching.
            bundle_item_org_request.ifNoneExist = str(Query({"name:exact": organization.name}))

            bundle_item_org = BundleEntry()
            bundle_item_org.resource = organization
            bundle_item_org.fullUrl = organization_id
            bundle_item_org.request = bundle_item_org_request

            bundle_entries.append(bundle_item_org)

            # Set the reference
            reference = FHIRReference()
            reference.reference = organization_id

            # Add it
            list_entry = ListEntry()
            list_entry.item = reference
            list_entries.append(list_entry)

        # Set it on the list
        data_list.entry = list_entries

        bundle_item_list_request = BundleEntryRequest()
        bundle_item_list_request.url = "List"
        bundle_item_list_request.method = "POST"
        bundle_item_list_request.ifNoneExist = str(
            Query(
                {
                    "patient": patient_id,
                    "code": FHIR.SNOMED_VERSION_URI + "|" + FHIR.SNOMED_LOCATION_CODE,
                    "status": "current",
                }
            )
        )

        bundle_item_list = BundleEntry()
        bundle_item_list.resource = data_list
        bundle_item_list.request = bundle_item_list_request

        bundle_entries.append(bundle_item_list)

        # Create and send the full bundle.
        full_bundle = Bundle()
        full_bundle.entry = bundle_entries
        full_bundle.type = "transaction"

        response = FHIR.post(request=request, path="/", data=full_bundle.as_json())

        return response.ok

    @staticmethod
    def create_consent_document_reference(
        request, study, ppm_id, filename, url, hash, size, composition, identifiers=None
    ):
        """
        Accepts details and rendering of a signed PPM consent and saves that data as a
        DocumentReference to the participant's FHIR record as well as includes a
        reference to the DocumentReference in the
        participant's consent Composition resource.
        :param study: The PPM study for which this consent was signed
        :type study: str
        :param ppm_id: The Patient object who owns the consent PDF
        :type ppm_id: str
        :param filename: The filename of the file
        :type filename: str
        :param url: The URL of the file
        :type url: str
        :param hash: The md5 hash of the file
        :type hash: str
        :param size: The size of the file
        :type size: int
        :param composition: The consent Composition object
        :type composition: dict
        :param identifiers: An optional list if identifier objects to attach to
        the DocumentReference
        :type identifiers: list
        :return: The DocumentReference URL
        """
        # Retain the response content for debugging
        content = None
        try:
            # Build the resource
            resource = {
                "resourceType": "DocumentReference",
                "subject": {"reference": "Patient/" + ppm_id},
                "type": {
                    "coding": [
                        {
                            "system": FHIR.ppm_consent_type_system,
                            "code": FHIR.ppm_consent_type_value,
                            "display": FHIR.ppm_consent_type_display,
                        }
                    ]
                },
                "created": datetime.now().strftime("%Y-%m-%d"),
                "indexed": datetime.now().isoformat(),
                "status": "current",
                "content": [
                    {
                        "attachment": {
                            "contentType": "application/pdf",
                            "language": "en-US",
                            "url": url,
                            "creation": datetime.now().isoformat(),
                            "title": filename,
                            "hash": hash,
                            "size": size,
                        }
                    }
                ],
                "context": {
                    "related": [
                        {
                            "ref": {"reference": f"ResearchStudy/{PPM.Study.fhir_id(study)}"},
                        }
                    ]
                },
            }

            # If passed, add identifiers
            if identifiers:
                resource.setdefault("identifier", []).extend(identifiers)

            # Start a bundle request
            bundle = Bundle()
            bundle.entry = []
            bundle.type = "transaction"

            # Create the document reference
            document_reference = DocumentReference(resource)

            # Create placeholder ID
            document_reference_id = uuid.uuid1().urn

            # Add Organization objects to bundle.
            document_reference_request = BundleEntryRequest()
            document_reference_request.method = "POST"
            document_reference_request.url = "DocumentReference"

            # Create the organization entry
            organization_entry = BundleEntry({"resource": document_reference.as_json()})
            organization_entry.request = document_reference_request
            organization_entry.fullUrl = document_reference_id

            # Add it
            bundle.entry.append(organization_entry)

            # Update the composition
            composition["section"].append({"entry": [{"reference": document_reference_id}]})

            # Ensure it's related to a study
            for entry in [
                section["entry"][0]
                for section in composition["section"]
                if "entry" in section and len(section["entry"])
            ]:
                if entry.get("reference") and PPM.Study.fhir_id(study) in entry["reference"]:
                    break
            else:
                # Add it
                logger.debug(f"PPM/{study}/{ppm_id}: Adding study reference to composition")
                composition["section"].append({"entry": [{"reference": f"ResearchStudy/{PPM.Study.fhir_id(study)}"}]})

            # Add List objects to bundle.
            composition_request = BundleEntryRequest()
            composition_request.method = "PUT"
            composition_request.url = "Composition/{}".format(composition["id"])

            # Create the organization entry
            composition_entry = BundleEntry({"resource": composition})
            composition_entry.request = composition_request

            # Add it
            bundle.entry.append(composition_entry)

            # Post the transaction
            response = FHIR.post(request=request, path="/", data=bundle.as_json())
            response.raise_for_status()

            # Check response
            return response.ok

        except (requests.HTTPError, TypeError, ValueError):
            logger.error(
                "Create consent DocumentReference failed",
                exc_info=True,
                extra={"study": study, "ppm_id": ppm_id, "response": content},
            )

        return False

    #
    # READ
    #

    @staticmethod
    def _query_resources(request, resource_type, query=None, bundled=False):
        """
        This method will fetch all resources for a given type, including paged results.
        :param resource_type: FHIR resource type
        :type resource_type: str
        :param query: A dict of key value pairs for searching resources
        :type query: dict
        :param bundled: Return a list of BundleEntry resources containing the queried resources
        :type bundled: bool
        :return: A list of FHIR resource dicts
        :rtype: list
        """
        logger.debug("Query resources: {} : {}".format(resource_type, query))

        # Update query
        if not query:
            query = {}

        # Add query if passed and set a return count to a high number, despite the server
        # probably ignoring it.
        query.update(
            {
                "_count": 1000,
            }
        )

        # Collect them.
        total_bundle = None

        # The url will be set to none on the second iteration if all resources
        # were returned, or it will be set to the next page of resources if more exist.
        while query is not None:

            # Parse the JSON.
            bundle = FHIR.get(request, path=f"/{resource_type}", data=query)
            if total_bundle is None:
                total_bundle = bundle
            elif bundle.get("total", 0) > 0:
                total_bundle["entry"].extend(bundle.get("entry"))

            for link in bundle.get("link", []):
                if link["relation"] == "next":
                    query = dict(furl(link["url"]).query.params)
                    break
            else:
                query = None

        # If bundled, return BundleEntry resources without unwrapping
        if bundled:
            return total_bundle.get("entry", []) if total_bundle else []
        else:
            return [r["resource"] for r in total_bundle.get("entry", [])] if total_bundle else []

    @staticmethod
    def _query_resource(request, resource_type, query=None):
        """
        This method will fetch the first resource for a given type and query.
        :param resource_type: FHIR resource type
        :type resource_type: str
        :param query: A dict of key value pairs for searching resources
        :type query: dict
        :return: A list of FHIR resource dicts
        :rtype: object
        """
        logger.debug("Query resource: {} : {}".format(resource_type, query))

        # Query
        resources = FHIR._query_resources(request, resource_type, query)
        if not resources:
            return None
        elif len(resources) > 1:
            logger.debug(f"Query {resource_type} - {query}: returned {len(resources)} resources")

        return next(iter(resources))

    @staticmethod
    def _query_bundle(request, resource_type, query=None):
        """
        This method will fetch all resources for a given type, including paged results.
        :param resource_type: FHIR resource type
        :type resource_type: str
        :param query: A dict of key value pairs for searching resources
        :type query: dict
        :return: A Bundle of FHIR resources
        :rtype: Bundle
        """
        logger.debug("Query bundle: {} : {}".format(resource_type, query))

        # Update query
        if not query:
            query = {}

        # Add page count
        query.update(
            {
                "_count": 1000,
            }
        )

        # Get the preliminary bundle
        bundle = FHIR.get(request, path=f"/{resource_type}", data=query)

        # Check for a next URL
        next_url = next((link["url"] for link in bundle.get("link", []) if link["relation"] == "next"), None)
        if next_url:

            # Parse out query
            query = dict(furl(next_url).query.params)

            # Get remaining entries
            bundle["entry"].extend(FHIR._query_resources(request, resource_type, query, bundled=True))

        return Bundle(bundle)

    @staticmethod
    def _get_resource(request, resource_type, _id):
        """
        This method will fetch a resource for a given type.
        :param resource_type: FHIR resource type
        :type resource_type: str
        :param _id: The ID of the resource
        :type _id: str
        :return: A FHIR resource
        :rtype: dict
        """
        logger.debug('Query resource "{}": {}'.format(resource_type, _id))

        return FHIR.get(request, path=f"/{resource_type}/{_id}")

    @staticmethod
    def query_participants(request, studies=None, enrollments=None, active=None, testing=False):
        """
        Queries the current set of participants. This allows filtering on study,
        enrollment, status, etc. A list of matching participants are returned
        as flattened Patient resource dicts.
        :param studies: A list of PPM studies to filter on
        :param enrollments: A list of PPM enrollments to filter on
        :param active: Select on whether the Patient.active flag is set or not
        :param testing: Whether to include testing participants or not
        :return: list
        """
        logger.debug(
            "Querying participants - Enrollments: {} - "
            "Studies: {} - Active: {} - Testing: {}".format(enrollments, studies, active, testing)
        )

        # Ensure we are using values
        if studies:
            studies = [PPM.Study.get(study).value for study in studies]
        if enrollments:
            enrollments = [PPM.Enrollment.get(enrollment).value for enrollment in enrollments]

        # Build the query
        query = {"_revinclude": ["ResearchSubject:individual", "Flag:subject"]}

        # Check if filtering on active
        if active is not None:
            query["active"] = "false" if not active else "true"

        # Peel out patients
        bundle = FHIR._query_bundle(request, "Patient", query)

        # Check for empty query set
        if not bundle.entry:
            return []

        # Build a dictionary keyed by FHIR IDs containing enrollment status
        patient_enrollments = {
            entry.resource.subject.reference.split("/")[1]: {
                "status": entry.resource.code.coding[0].code,
                "date_accepted": entry.resource.period.start.origval if entry.resource.period else "",
                "date_updated": entry.resource.meta.lastUpdated.origval,
            }
            for entry in bundle.entry
            if entry.resource.resource_type == "Flag"
        }

        # Build a dictionary keyed by FHIR IDs containing flattened study objects
        patient_studies = {
            entry.resource.individual.reference.split("/")[1]: {
                "study": FHIR.get_study_from_research_subject(entry.resource),
                "date_registered": entry.resource.period.start.origval,
            }
            for entry in bundle.entry
            if entry.resource.resource_type == "ResearchSubject"
            and FHIR.is_ppm_research_subject(entry.resource.as_json())
        }

        # Process patients
        patients = []
        for patient in [entry.resource for entry in bundle.entry if entry.resource.resource_type == "Patient"]:
            try:
                # Fetch their email
                email = next(
                    identifier.value
                    for identifier in patient.identifier
                    if identifier.system == FHIR.patient_email_identifier_system
                )

                # Check if tester
                if not testing and PPM.is_tester(email):
                    continue

                # Get values and compare to filters
                patient_enrollment = patient_enrollments.get(patient.id)
                patient_study = patient_studies.get(patient.id)

                if enrollments and patient_enrollment["status"].lower() not in enrollments:
                    continue

                if studies and patient_study.get("study").lower() not in studies:
                    continue

                # Pull out dates, both formatted and raw
                date_registered = FHIR._format_date(patient_study.get("date_registered"), "%m/%d/%Y")
                datetime_registered = patient_study.get("date_registered")
                date_enrollment_updated = FHIR._format_date(patient_enrollment.get("date_updated"), "%m/%d/%Y")
                datetime_enrollment_updated = patient_enrollment.get("date_updated")

                # Build the dict
                patient_dict = {
                    "email": email,
                    "fhir_id": patient.id,
                    "ppm_id": patient.id,
                    "enrollment": patient_enrollment["status"],
                    "status": patient_enrollment["status"],
                    "study": patient_study.get("study"),
                    "project": patient_study.get("study"),
                    "date_registered": date_registered,
                    "datetime_registered": datetime_registered,
                    "date_enrollment_updated": date_enrollment_updated,
                    "datetime_enrollment_updated": datetime_enrollment_updated,
                }

                # Check acceptance
                if patient_enrollment.get("date_accepted"):
                    patient_dict["date_accepted"] = FHIR._format_date(patient_enrollment["date_accepted"], "%m/%d/%Y")
                    patient_dict["datetime_accepted"] = patient_enrollment["date_accepted"]

                # Wrap the patient resource in a fake bundle and flatten them
                flattened_patient = FHIR.flatten_patient({"entry": [{"resource": patient.as_json()}]})
                if flattened_patient:
                    patient_dict.update(flattened_patient)

                # Add it
                patients.append(patient_dict)

            except Exception as e:
                logger.exception("Resources malformed for Patient/{}: {}".format(patient.id, e))

        return patients

    @staticmethod
    def query_patients(request, study=None, enrollment=None, active=None, testing=False, include_deceased=True):
        logger.debug(
            "Getting patients - enrollment: {}, study: {}, "
            "active: {}, testing: {}".format(enrollment, study, active, testing)
        )

        # Check for multiples
        enrollments = enrollment.split(",") if enrollment else None
        studies = study.split(",") if study else None

        # Call the query_participants method
        return FHIR.query_participants(request, studies, enrollments, active, testing)

    @staticmethod
    def query_participant(request, patient, flatten_return=False):

        # Add query for patient
        data = FHIR._patient_query(patient)
        data["_include"] = "*"
        data["_revinclude"] = "*"

        # Make the FHIR request.
        bundle = FHIR.get(request, path="Patient", data=data)
        if not bundle.get("entry"):
            return {}

        # Return accordingly
        if flatten_return:
            return FHIR.flatten_participant(request, bundle)
        else:
            return bundle

    @staticmethod
    def get_participant(request, patient, flatten_return=False):

        # Add query for patient
        data = FHIR._patient_query(patient)
        data["_include"] = "*"
        data["_revinclude"] = "*"

        # Make the FHIR request.
        bundle = FHIR.get(request, path="Patient", data=data)
        if not bundle.get("entry"):
            return {}

        if flatten_return:
            return FHIR.flatten_participant(request, bundle)
        else:
            return [entry["resource"] for entry in bundle.get("entry")]

        return None

    @staticmethod
    def get_patient(request, patient, flatten_return=False):

        # Add query for patient
        data = FHIR._patient_query(patient)
        data["_include"] = "*"
        data["_revinclude"] = "*"

        # Make the FHIR request.
        bundle = FHIR.get(request, path="Patient", data=data)
        if bundle:

            if flatten_return:
                return FHIR.flatten_patient(bundle)
            else:
                return next((entry["resource"] for entry in bundle.get("entry", [])), None)

        return None

    @staticmethod
    def query_consent_compositions(request, patient, study=None, flatten_return=False):
        """
        Gets and returns any Compositions storing the user's signed consent resources
        :param patient: The Patient object who owns the consent
        :type patient: str
        :param study: The study for which the consent was signed
        :type study: str
        :param flatten_return: Whether to return FHIR JSON or a flattened dict
        :type flatten_return: bool
        :return: The Composition object
        """
        # Build the query
        query = {"type": f"{FHIR.ppm_consent_type_system}|{FHIR.ppm_consent_type_value}"}

        # Check study
        if study:
            query["related-ref"] = f"ResearchStudy/{PPM.Study.fhir_id(study)}"

        # Build the query
        query.update(FHIR._patient_resource_query(patient))

        # Get resources
        resources = FHIR._query_resources(request, "Composition", query=query)
        if resources:

            # Handle the format of return
            if flatten_return:
                # If flattening, we need to query all related resources per Composition
                bundles = [
                    FHIR._query_bundle(
                        request,
                        "Composition",
                        query={
                            "id": resource["id"],
                            "_include": "*",
                            "_revinclude": "*",
                        },
                    )
                    for resource in resources
                ]
                return [FHIR.flatten_consent_composition(bundle) for bundle in bundles]
            else:
                return resources

        return None

    @staticmethod
    def get_consent_composition(request, patient, study, flatten_return=False):
        """
        Gets and returns the Composition storing the user's signed consent resources
        :param patient: The Patient object who owns the consent
        :type patient: str
        :param study: The study for which the consent was signed
        :type study: str
        :param flatten_return: Whether to return FHIR JSON or a flattened dict
        :type flatten_return: bool
        :return: The Composition object
        """
        # Build the query
        query = {
            "type": f"{FHIR.ppm_consent_type_system}|{FHIR.ppm_consent_type_value}",
            "related-ref": f"ResearchStudy/{PPM.Study.fhir_id(study)}",
        }

        # Build the query
        query.update(FHIR._patient_resource_query(patient))

        # Get resources
        resources = FHIR._query_resources(request, "Composition", query=query)
        if resources:

            # Check for multiple
            if len(resources) > 1:
                logger.error(
                    f"FHIR Error: Multiple consent Compositions " f"returned for {study}/{patient}",
                    extra={
                        "compositions": [f"Composition/{r['id']}" for r in resources],
                    },
                )

            # Handle the format of return
            if flatten_return:
                # If flattening, we need all related resources
                bundle = FHIR._query_bundle(
                    request,
                    "Composition",
                    query={
                        "id": resources[0]["id"],
                        "_include": "*",
                        "_revinclude": "*",
                    },
                )
                return FHIR.flatten_consent_composition(bundle)
            else:
                return resources[0]

        return None

    @staticmethod
    def get_consent_document_reference(request, patient, study, flatten_return=False):
        """
        Gets and returns the DocumentReference storing the user's signed consent PDF
        :param patient: The Patient object who owns the consent PDF
        :type patient: str
        :param study: The study for which the consent was signed
        :type study: str
        :param flatten_return: Whether to return FHIR JSON or a flattened dict
        :type flatten_return: bool
        :return: The DocumentReference object
        """
        # Build the query
        query = {
            "type": f"{FHIR.ppm_consent_type_system}|{FHIR.ppm_consent_type_value}",
            "related-ref": PPM.Study.fhir_id(study),
        }

        # Add query for patient
        query.update(FHIR._patient_resource_query(patient))

        # Get resources
        resources = FHIR._query_resources(request, "DocumentReference", query=query)
        if resources:

            # Check for multiple
            if len(resources) > 1:
                logger.error(
                    f"FHIR Error: Multiple consent DocumentReferences " f"returned for {study}/{patient}",
                    extra={
                        "document_references": [f"DocumentReference/{r['id']}" for r in resources],
                    },
                )

            # Handle the format of return
            if flatten_return:
                return FHIR.flatten_document_reference(resources[0])
            else:
                return resources[0]

        return None

    @staticmethod
    def query_consent_document_references(request, patient, flatten_return=False):
        """
        Gets and returns the DocumentReference storing the user's signed consent PDF
        :param patient: The Patient object who owns the consent PDF
        :type patient: str
        :param flatten_return: Whether to return FHIR JSON or a flattened dict
        :type flatten_return: bool
        :return: The DocumentReference object
        """
        # Build the query
        query = {"type": f"{FHIR.ppm_consent_type_system}|{FHIR.ppm_consent_type_value}"}

        # Add query for patient
        query.update(FHIR._patient_resource_query(patient))

        # Get resources
        resources = FHIR._query_resources(request, "DocumentReference", query=query)

        if flatten_return:
            return [FHIR.flatten_document_reference(resource) for resource in resources]
        else:
            return resources

    @staticmethod
    def query_patient_id(request, email):
        """
        Returns the PPM/FHIR ID for the patient with the passed email address
        :param request: The current request object
        :type request: HttpRequest
        :param email: The email address to use for the lookup
        :type email: str
        :return: The PPM/FHIR ID if it exists
        """
        # Get the patient
        patient = FHIR.get_patient(request, email)
        if patient:
            return patient["id"]

        return None

    @staticmethod
    def query_ppm_devices(request, patient=None, item=None, identifier=None, flatten_return=False):
        """
        Queries the participants FHIR record for any PPM-related Device
        resources. These are used to track kits, etc that
        are sent to participants for collecting samples and other information/data.
        :param request: The current request object
        :type request: HttpRequest
        :param patient: The patient identifier/ID/object
        :type patient: object
        :param item: The PPM item type
        :type item: str
        :param identifier: The device identifier
        :type identifier: str
        :param flatten_return: Whether to flatten the resource or not
        :type flatten_return: bool
        :return: A list of resources
        :rtype: list
        """
        # Check item type
        if item:
            query = {
                "type": "{}|{}".format(FHIR.device_coding_system, item),
            }
        else:

            query = {
                "type": "{}|".format(FHIR.device_coding_system),
            }

        # Check for an identifier
        if identifier:
            query["identifier"] = "{}|{}".format(FHIR.device_identifier_system, identifier)

        # Update for the patient query
        if patient:
            query.update(FHIR._patient_resource_query(patient))

        # Get the devices
        devices = FHIR._query_resources(request, "Device", query=query)

        if flatten_return:
            return [FHIR.flatten_ppm_device(resource) for resource in devices]
        else:
            return devices

    @staticmethod
    def query_ppm_research_subjects(request, patient=None, flatten_return=False):

        # Get flags for current user
        query = {
            "identifier": "{}|".format(FHIR.research_subject_identifier_system),
        }

        # Update for the patient query
        if patient:
            query.update(FHIR._patient_resource_query(patient))

        # Get the resources
        resources = FHIR._query_resources(request, "ResearchSubject", query=query)

        if flatten_return:
            return [FHIR.flatten_research_subject(resource) for resource in resources]
        else:
            return resources

    @staticmethod
    def query_research_subjects(request, patient=None, flatten_return=False):

        # Build query
        query = {}
        if patient:
            query = FHIR._patient_resource_query(patient)

        # Get the resources
        resources = FHIR._query_resources(request, "ResearchSubject", query=query)

        # Filter out PPM subjects
        research_subjects = [
            entry
            for entry in resources
            if entry.get("study", {}).get("reference", None)
            not in ["ResearchStudy/ppm-{}".format(study.value) for study in PPM.Project]
        ]

        if flatten_return:
            return [FHIR.flatten_research_subject(resource) for resource in research_subjects]
        else:
            return research_subjects

    @staticmethod
    def query_enrollment_flag(request, patient, flatten_return=False):

        # Get flags for current user
        query = FHIR._patient_resource_query(patient, "subject")

        # Make the fetch
        flag = FHIR._query_resource(request, "Flag", query=query)
        if flatten_return:
            return FHIR.flatten_enrollment_flag(flag)
        else:
            return flag

    @staticmethod
    def query_questionnaire_responses(request, patient=None, questionnaire_id=None):

        # Build the query
        query = {
            "questionnaire": "Questionnaire/{}".format(questionnaire_id),
            "_include": "*",
            "_revinclude": "*",
        }

        # Check patient
        if patient:
            query.update(FHIR._patient_query(patient))

        # Query resources
        bundle = FHIR._query_bundle(request, "QuestionnaireResponse", query=query)

        return bundle

    @staticmethod
    def get_questionnaire_response(request, patient=None, questionnaire_id=None, flatten_return=False):

        # Build the query
        query = {
            "questionnaire": "Questionnaire/{}".format(questionnaire_id),
            "_include": "*",
            "_revinclude": "*",
        }

        # Check patient
        query.update(FHIR._patient_resource_query(identifier=patient, key="source"))

        # Query resources
        bundle = FHIR._query_bundle(request, "QuestionnaireResponse", query=query)
        if flatten_return:
            return FHIR.flatten_questionnaire_response(bundle, questionnaire_id)
        else:

            # Fetch the questionnaire response from the bundle
            questionnaire_response = next(
                (r.resource for r in bundle.entry if r.resource.resource_type == "QuestionnaireResponse"),
                None,
            )
            return questionnaire_response.as_json()

    @staticmethod
    def query_document_references(request, patient=None, query=None, flatten_return=False):
        """
        Queries the current user's FHIR record for any DocumentReferences related to this type
        :return: A list of DocumentReference resources
        :rtype: list
        """
        # Build the query
        if query is None:
            query = {}

        if patient:
            query.update(FHIR._patient_resource_query(patient))

        # Get resources
        resources = FHIR._query_resources(request, "DocumentReference", query=query)

        if flatten_return:
            return [FHIR.flatten_document_reference(resource) for resource in resources]
        else:
            return resources

    @staticmethod
    def query_data_document_references(request, patient=None, provider=None, status=None, flatten_return=False):
        """
        Queries the current user's FHIR record for any DocumentReferences
        related to this type
        :return: A list of DocumentReference resources
        :rtype: list
        """
        # Build the query
        query = {}

        if patient:
            query.update(FHIR._patient_resource_query(patient))

        # Set the provider, if passed
        if provider:
            query["type"] = f"{FHIR.data_document_reference_identifier_system}|{provider}"
        else:
            query["type"] = f"{FHIR.data_document_reference_identifier_system}|"

        # Set preference on status
        if status:
            query["status"] = status

        # Get resources
        resources = FHIR._query_resources(request, "DocumentReference", query=query)

        if flatten_return:
            return [FHIR.flatten_document_reference(resource) for resource in resources]
        else:
            return resources

    @staticmethod
    def query_enrollment_status(request, patient_ref):

        try:
            # Make the FHIR request.
            response = FHIR.query_enrollment_flag(request, patient_ref)

            # Parse the bundle.
            bundle = Bundle(response)
            if bundle.total > 0:

                # Check flags.
                for flag in [entry.resource for entry in bundle.entry if entry.resource.resource_type == "Flag"]:

                    # Get the code's value
                    state = flag.code.coding[0].code
                    logger.debug('Fetched state "{}" for user'.format(state))

                    return state

            else:
                logger.debug("No flag found for user!")

        except KeyError as e:
            logger.exception("FHIR Error: {}".format(e), exc_info=True)

        return None

    @staticmethod
    def query_ppm_research_studies(request, email, flatten_return=True):

        # Find Research subjects (without identifiers, so as to exclude PPM resources)
        research_subjects = FHIR.query_ppm_research_subjects(request, email, flatten_return=False)

        if not research_subjects:
            logger.debug("No Research Subjects, no Research Studies")
            return None

        # Get study IDs
        research_study_ids = [subject["study"]["reference"].split("/")[1] for subject in research_subjects]

        # Get the IDs
        research_studies = FHIR._query_resources(request, "ResearchStudy", query={"_id": ",".join(research_study_ids)})

        # Return the titles
        if flatten_return:
            return [research_study["title"] for research_study in research_studies]
        else:
            return [research_study for research_study in research_studies]

    @staticmethod
    def query_research_studies(request, email, flatten_return=True):

        # Find Research subjects (without identifiers, so as to exclude PPM resources)
        research_subjects = FHIR.query_research_subjects(request, email, flatten_return=False)

        if not research_subjects:
            logger.debug("No Research Subjects, no Research Studies")
            return None

        # Get study IDs
        research_study_ids = [subject["study"]["reference"].split("/")[1] for subject in research_subjects]

        # Get the IDs
        research_studies = FHIR._query_resources(request, "ResearchStudy", query={"_id": ",".join(research_study_ids)})

        # Return the titles
        if flatten_return:
            return [research_study["title"] for research_study in research_studies]
        else:
            return [research_study for research_study in research_studies]

    @staticmethod
    def get_point_of_care_list(request, patient, flatten_return=False):
        """
        Query the list object which has a patient and a snomed code.
        If it exists we'll need the URL to update the object later.
        """
        # Build the query for their point of care list
        query = {
            "code": FHIR.SNOMED_VERSION_URI + "|" + FHIR.SNOMED_LOCATION_CODE,
            "_include": "List:item",
        }

        # Add patient query
        query.update(FHIR._patient_resource_query(patient))

        # Find matching resource(s)
        bundle = FHIR._query_bundle(request, "List", query=query)

        if flatten_return:
            return FHIR.flatten_list(bundle, "Organization")
        else:
            return next((entry["resource"] for entry in bundle.as_json().get("entry", [])), None)

    @staticmethod
    def query_ppm_communications(request, patient=None, identifier=None, flatten_return=False):
        """
        Find all Communications filtered by patient, study and/or identifier
        :param patient: The patient to query on (FHIR ID, email, Patient object)
        :type patient: str
        :param identifier: The identifier of the Communications
        :type identifier: str
        :param flatten_return: Flatten the resources
        :type flatten_return: bool
        :return: The FHIR bundle
        :rtype: dict
        """

        # Build the query
        query = {}
        if patient:
            query.update(FHIR._patient_resource_query(patient, "recipient"))

        if identifier:
            query["identifier"] = f"{FHIR.ppm_comm_identifier_system}|{identifier}"

        # Find all resources
        resources = FHIR._query_resources(request, "Communication", query=query)

        if flatten_return:
            return [FHIR.flatten_communication(resource) for resource in resources]
        else:
            return resources

    #
    # UPDATE
    #

    @staticmethod
    def update_patient(request, fhir_id, form):

        # Get their resource
        patient = FHIR._query_resource(request, "Patient", fhir_id)

        # Check form data and make updates where necessary
        first_name = form.get("firstname")
        if first_name:
            patient["name"][0]["given"][0] = first_name

        last_name = form.get("lastname")
        if last_name:
            patient["name"][0]["family"] = last_name

        # Update the whole address
        street_address1 = form.get("street_address1")
        street_address2 = form.get("street_address2")
        if street_address1:
            patient["address"][0]["line"] = (
                [street_address1] if not street_address2 else [street_address1, street_address2]
            )

        city = form.get("city")
        if city:
            patient["address"][0]["city"] = city

        state = form.get("state")
        if state:
            patient["address"][0]["state"] = state

        zip_code = form.get("zip")
        if zip_code:
            patient["address"][0]["postalCode"] = zip_code

        phone = form.get("phone")
        if phone:
            for telecom in patient.get("telecom", []):
                if telecom["system"] == FHIR.patient_phone_telecom_system:
                    telecom["value"] = phone
                    break
            else:
                # Add it
                patient.setdefault("telecom", []).append({"system": FHIR.patient_phone_telecom_system, "value": phone})

        email = form.get("contact_email")
        if email:
            for telecom in patient.get("telecom", []):
                if telecom["system"] == FHIR.patient_email_telecom_system:
                    telecom["value"] = email
                    break
            else:
                # Add it
                patient.setdefault("telecom", []).append({"system": FHIR.patient_email_telecom_system, "value": email})

        else:
            # Delete an existing email if it exists
            for telecom in patient.get("telecom", []):
                if telecom["system"] == FHIR.patient_email_telecom_system:
                    patient["telecom"].remove(telecom)
                    break

        # Update their referral method if needed
        referral = form.get("how_did_you_hear_about_us")
        if referral:
            for extension in patient.get("extension", []):
                if extension["url"] == FHIR.referral_extension_url:
                    extension["valueString"] = referral
                    break
            else:
                # Add it
                patient.setdefault("extension", []).append(
                    {"url": FHIR.referral_extension_url, "valueString": referral}
                )

        else:
            # Delete this if not specified
            for extension in patient.get("extension", []):
                if extension["url"] == FHIR.referral_extension_url:
                    patient["extension"].remove(extension)
                    break

        active = form.get("active")
        if active is not None:
            patient["active"] = False if active in ["false", False] else True

        # Put it
        response = FHIR.put(request, path=f"/Patient/{fhir_id}")

        return response.ok

    @staticmethod
    def update_patient_active(request, patient_id, active):
        """
        Flips the switch on the Patients active status
        :param request:
        :param patient_id:
        :param active:
        :return:
        """

        # Build the update
        patch = [{"op": "replace", "path": "/active", "value": True if active else False}]

        # Set headers for patch operation
        headers = {"Content-Type": "application/json-patch+json"}

        # Get patient ID
        ppm_id = FHIR._patient_id(request, patient_id)

        response = FHIR.request(
            "patch", headers=headers, request=request, path=f"/Patient/{ppm_id}", data=patch, check=True
        )

        return response.ok

    @staticmethod
    def update_ppm_device(request, patient_id, item, identifier=None, shipped=None, returned=None):

        # Get the device
        device = next(iter(FHIR.query_ppm_devices(request, patient=patient_id, item=item)), None)
        if not device:
            logger.debug(f"No PPM device could be found for {patient_id}/{item}/{identifier}")
            return False

        # Update the resource identifier
        if identifier:

            # Get the PPM identifier dictionary
            identifiers = device.get("identifier", [])
            ppm_identifier = next(
                (_id for _id in identifiers if _id.get("system") == FHIR.device_identifier_system),
                None,
            )
            if ppm_identifier:

                # Update it
                ppm_identifier["value"] = identifier.lower()

            else:

                # Add a new one
                identifiers.append(
                    {
                        "system": FHIR.device_identifier_system,
                        "value": identifier.lower(),
                    }
                )

            # Set it
            device["identifier"] = identifiers

        # Check dates
        if shipped:
            device["manufactureDate"] = shipped.isoformat()
        elif device.get("manufactureDate"):
            del device["manufactureDate"]

        if returned:
            device["expirationDate"] = returned.isoformat()
        elif device.get("expirationDate"):
            del device["expirationDate"]

        # Post the transaction
        response = FHIR.put(request, path=f'/Device/{device["id"]}', data=device)

        return response.ok

    @staticmethod
    def update_patient_deceased(request, patient_id, date=None, active=None):
        """
        Updates a participant as deceased. If a date is passed, they are marked
        as such as well as updated be being inactive. If passed, 'active' will
        update this flag on the Patient simultaneously.
        :param patient_id: The patient identifier
        :param date: The date of death for the Patient
        :param active: The value to set on the Patient's 'active' flag
        :return: boolean
        """
        # Build the update
        if date:
            patch = [
                {
                    "op": "replace",
                    "path": "/deceasedDateTime",
                    "value": date.isoformat(),
                }
            ]
        else:
            patch = [{"op": "remove", "path": "/deceasedDateTime"}]

        # Update active if needed
        if active is not None:
            patch.append({"op": "replace", "path": "/active", "value": active})

        # Set headers for patch operation
        headers = {"Content-Type": "application/json-patch+json"}

        # Get patient ID
        ppm_id = FHIR._patient_id(request, patient_id)

        response = FHIR.request(
            "patch", headers=headers, request=request, path=f"/Patient/{ppm_id}", data=patch, check=True
        )

        return response.ok

    @staticmethod
    def update_patient_enrollment(request, patient_id, status):
        logger.debug("Patient: {}, Status: {}".format(patient_id, status))

        # Build the query
        query = FHIR._patient_resource_query(patient_id, key="subject")

        # Fetch the flag.
        resource = FHIR._query_resource(request, "Flag", query)

        # Check for nothing.
        if not resource:
            logger.error(
                "FHIR Error: Flag does not already exist for Patient/{}".format(patient_id), extra={"status": status}
            )

            # Create it.
            return FHIR.create_patient_enrollment(request, patient_id, status)

        else:
            logger.debug("Existing enrollment flag found")

            # Create flag
            flag = Flag(resource, strict=True)

            # Get the first and only flag.
            code = flag.code.coding[0]

            # Update flag properties for particular states.
            logger.debug("Current status: {}".format(code.code))
            if code.code != "accepted" and status == "accepted":
                logger.debug('Setting enrollment flag status to "active"')

                # Set status.
                flag.status = "active"

                # Set a start date.
                if flag.period and flag.period.start:

                    # Remove the end
                    flag.period.end = None

                else:
                    now = FHIRDate(datetime.now().isoformat())
                    period = Period()
                    period.start = now
                    flag.period = period

            elif code.code != "terminated" and status == "terminated":
                logger.debug('Setting enrollment flag status to "terminated"')

                # Set status.
                flag.status = "inactive"

                # Set an end date if a flag is present
                if flag.period:
                    now = FHIRDate(datetime.now().isoformat())
                    flag.period.end = now
                else:
                    logger.debug("Flag has no period/start, cannot set end: Patient/{}".format(patient_id))

            elif code.code != "completed" and status == "completed":
                logger.debug('Setting enrollment flag status to "completed"')

                # Set status.
                flag.status = "inactive"

                # Set an end date if a flag is present
                if flag.period:
                    now = FHIRDate(datetime.now().isoformat())
                    flag.period.end = now
                else:
                    logger.debug("Flag has no period/start, cannot set end: Patient/{}".format(patient_id))

            elif code.code == "accepted" and status != "accepted":
                logger.debug("Reverting back to inactive with no dates")

                # Flag defaults to inactive with no start or end dates.
                flag.status = "inactive"
                flag.period = None

            elif code.code != "ineligible" and status == "ineligible":
                logger.debug("Setting as ineligible, inactive with no dates")

                # Flag defaults to inactive with no start or end dates.
                flag.status = "inactive"
                flag.period = None

            else:
                logger.debug("Unhandled flag update: {} -> {}".format(code.code, status))

            # Set the code.
            code.code = status
            code.display = status.title()
            flag.code.text = status.title()

            # Post the transaction
            response = FHIR.put(request, path=f"/Flag/{flag.id}", data=flag.as_json())

            return response.ok

    @staticmethod
    def update_consent_composition(request, patient, study, document_reference_id=None, composition=None):
        """
        Updates a participant's consent Composition resource for changes in
        related references, e.g. the DocumentReference referencing a rendered
        PDF of the signed consent.
        :param patient: The patient's identifier
        :param study: The study for which this consent was signed
        :param document_reference_id: An updated document reference ID, if any
        :param composition: The Composition resource, if available
        :return:
        """
        logger.debug(
            "Patient: {}, Composition: {}, Study: {}, DocumentReference: {}".format(
                patient,
                composition["id"] if composition else None,
                study,
                document_reference_id,
            )
        )

        # If not composition, get it
        if not composition:
            composition = FHIR.get_consent_composition(request, patient=patient, study=study)

        # Get references
        references = [
            s["entry"][0]["reference"]
            for s in composition["section"]
            if s.get("entry") and s["entry"] is list and len(s["entry"]) and "reference" in s["entry"][0]
        ]
        if document_reference_id:
            for reference in references:
                # Check type
                if "DocumentReference" in reference:

                    # Update it
                    reference = {
                        "reference": f"DocumentReference/{document_reference_id}",
                        "display": FHIR.ppm_consent_type_display,
                    }
                    logger.debug(f"{study}/Patient/{patient}: Updated Composition " f"DocumentReference: {reference}")
        else:
            # Remove it if included
            sections = []
            for section in composition["section"]:
                if "entry" in section:
                    for entry in section.get("entry", []):
                        if "reference" in entry and "DocumentReference" in entry["reference"]:
                            # Nothing to do as we want to leave it out
                            pass
                        else:
                            sections.append(section)
                else:
                    sections.append(section)

            # Set the new sections
            composition["section"] = sections

        for reference in references:
            # Ensure study is set
            if "ResearchStudy" in reference:
                break
        else:
            # Add it
            composition["section"].append({"reference": f"ResearchStudy/{PPM.Study.fhir_id(study)}"})

        # Post the transaction
        response = FHIR.put(request, path=f"/Composition/{composition['id']}", data=composition)

        return response.ok

    @staticmethod
    def update_research_subject(request, patient_id, research_subject_id, start=None, end=None):
        logger.debug(
            "Patient: {}, ResearchSubject: {}, Start: {}, End: {}".format(patient_id, research_subject_id, start, end)
        )

        # Build the update
        if end:
            patch = [{"op": "add", "path": "/period/end", "value": end.isoformat()}]
        else:
            patch = [{"op": "remove", "path": "/period/end"}]
        if start:
            patch.append({"op": "update", "path": "/period/start", "value": start.isoformat()})

        # Set headers for patch operation
        headers = {"Content-Type": "application/json-patch+json"}

        return FHIR.request(
            "patch",
            headers=headers,
            request=request,
            path=f"/ResearchSubject/{research_subject_id}",
            data=patch,
            check=True,
        )

    @staticmethod
    def update_ppm_research_subject(request, patient_id, study=None, start=None, end=None):
        logger.debug("Patient: {}, Study: {}, Start: {}, End: {}".format(patient_id, study, start, end))

        # Build the query
        query = FHIR._patient_resource_query(patient_id)

        # Build study identifier
        study_query = "{}|".format(FHIR.research_subject_identifier_system)
        if study:
            study_query += PPM.Study.get(study).value

        # Add study query
        query["identifier"] = study_query

        # Fetch the research subject.
        research_subjects = FHIR._query_resources(request, "ResearchSubject", query=query)

        # Iterate studies
        for research_subject_id in [resource["id"] for resource in research_subjects]:
            logger.debug(f"{patient_id}: Found ResearchSubject/{research_subject_id} -> {end}")

            # Do the update
            FHIR.update_research_subject(request, patient_id, research_subject_id, start, end)

        return True

    @staticmethod
    def update_point_of_care_list(request, patient, point_of_care):
        """
        Adds a point of care to a Participant's existing list and returns the flattened
        updated list of points of care (just a list with the name of the Organization).
        Will return the existing list if the point of care is already in the list. Will
        look for an existing Organization before creating.
        :param patient: The participant's email address
        :param point_of_care: The name of the point of care
        :return: [str]
        """
        logger.debug("Add point of care: {}".format(point_of_care))

        # Get the flattened list
        point_of_care_list = FHIR.get_point_of_care_list(request, patient, flatten_return=False)
        points_of_care = FHIR.flatten_list(point_of_care_list)

        # Check if the name exists in the list already
        for organization in points_of_care:
            if organization == point_of_care:
                logger.debug("Organization is already in List!")

                # Just return the list as is
                return points_of_care

        # Check for existing resource
        org = FHIR._query_resource(request, "Organization", query={"name": point_of_care})

        # Start a bundle request
        bundle = Bundle()
        bundle.entry = []
        bundle.type = "transaction"

        if org:
            logger.debug("Found existing organization!")

            # Get the ID
            organization_id = "Organization/{}".format(org["id"])
            logger.debug("Existing organization: {}".format(organization_id))

        else:
            logger.debug("No existing organization, creating...")

            # Create the organization
            organization = Organization()
            organization.name = point_of_care

            # Create placeholder ID
            organization_id = uuid.uuid1().urn

            # Add Organization objects to bundle.
            organization_request = BundleEntryRequest()
            organization_request.method = "POST"
            organization_request.url = "Organization"

            # Create the organization entry
            organization_entry = BundleEntry({"resource": organization.as_json()})
            organization_entry.request = organization_request
            organization_entry.fullUrl = organization_id

            # Add it
            bundle.entry.append(organization_entry)

        # Add it to the list
        point_of_care_list["entry"].append({"item": {"reference": organization_id}})

        # Add List objects to bundle.
        list_request = BundleEntryRequest()
        list_request.method = "PUT"
        list_request.url = "List/{}".format(point_of_care_list["id"])

        # Create the organization entry
        list_entry = BundleEntry({"resource": point_of_care_list})
        list_entry.request = list_request

        # Add it
        bundle.entry.append(list_entry)

        # Post the transaction
        FHIR.post(request, path="/", data=bundle.as_json())

        # Return the flattened list with the new organization
        points_of_care.append(point_of_care)

        return points_of_care

    @staticmethod
    def update_twitter(request, patient_id, handle=None, uses_twitter=None):
        """
        Accepts details of a Twitter integration and updates the Patient record.
        A handle automatically sets the 'uses-twitter' extension as true, whereas
        no handle and no value for 'uses-twitter' deletes the extension and the
        handle from the Patient.
        :param patient_id: Patient email, ID or object
        :param handle: The user's Twitter handle
        :param uses_twitter: The flag to set for whether the user has opted
        out of the integration
        :return: bool
        """
        logger.debug("Twitter handle: {}, Uses Twitter: {}".format(handle, uses_twitter))

        # Fetch the Patient.
        patient = FHIR.get_patient(request, patient_id)

        # Check if handle submitted or not
        if handle:

            # Set the value
            twitter = {
                "system": FHIR.patient_twitter_telecom_system,
                "value": "https://twitter.com/" + handle,
            }

            # Add it to their contact points
            patient.setdefault("telecom", []).append(twitter)

        else:
            # Check for existing handle and remove it
            for telecom in patient.get("telecom", []):
                if "twitter.com" in telecom["value"]:
                    patient["telecom"].remove(telecom)

        # Check for an existing Twitter status extension
        extension = next(
            (extension for extension in patient.get("extension", []) if "uses-twitter" in extension.get("url")),
            None,
        )

        # See if we need to update the extension
        if handle is not None or uses_twitter is not None:

            # Set preference
            value = handle is not None or uses_twitter
            logger.debug('({}) Updating "uses_twitter" -> {}'.format(patient["id"], value))

            if not extension:
                # Add an extension indicating their use of Twitter
                extension = {
                    "url": FHIR.twitter_extension_url,
                    "valueBoolean": value,
                }

                # Add it to their extensions
                patient.setdefault("extension", []).append(extension)

            # Update the flag
            extension["valueBoolean"] = value

        elif extension:
            logger.debug('({}) Deleting "uses_twitter" -> None'.format(patient["id"]))

            # Remove this extension
            patient["extension"].remove(extension)

        return FHIR.request("put", request=request, path=f'/Patient/{patient["id"]}', data=patient, check=True)

    @staticmethod
    def update_patient_extension(request, patient_id, extension_url, value=None):
        """
        Accepts an extension URL and a value and does the necessary update on the
        Patient. If None is passed for the value and the extension already exists,
        it is deleted from the Patient.
        :param patient_id: Patient email, ID or object
        :param extension_url: The URL for the extension
        :param value: The value to set: str, bool, int or None
        :return: bool
        """
        logger.debug('Patient extension: "{}" -> "{}"'.format(extension_url, value))

        # Fetch the Patient.
        patient = FHIR.get_patient(request, patient_id)

        # Check for an existing Facebook status extension
        extension = next(
            (
                extension
                for extension in patient.get("extension", [])
                if extension_url.lower() == extension.get("url", "").lower()
            ),
            None,
        )
        if value is not None:
            logger.debug('({}) Updating "{}" -> "{}"'.format(patient["id"], extension_url, value))

            # Check if an existing one was found
            if not extension:

                # Add an extension indicating their use of Facebook
                extension = {"url": extension_url}

                # Add it to their extensions
                patient.setdefault("extension", []).append(extension)

            # Check type and set the value accordingly
            if type(value) is str:
                extension["valueString"] = value
            elif type(value) is bool:
                extension["valueBoolean"] = value
            elif type(value) is int:
                extension["valueInteger"] = value
            elif type(value) is datetime:
                extension["valueDateTime"] = value.isoformat()
            else:
                logger.error('Unhandled value type "{}" : "{}"'.format(value, type(value)))
                return False

        elif extension:
            logger.debug("({}) Deleting {} -> None".format(patient["id"], extension_url))

            # Remove this extension
            patient["extension"].remove(extension)

        return FHIR.put(request, path=f'/Patient/{patient["id"]}', data=patient)

    @staticmethod
    def update_picnichealth(request, patient_id, registered=True):
        logger.debug("Picnichealth registration: {} -> {}".format(patient_id, registered))

        # Fetch the Patient.
        patient = FHIR.get_patient(request, patient_id)

        # Check for an existing Twitter status extension
        extension = next(
            (
                extension
                for extension in patient.get("extension", [])
                if FHIR.picnichealth_extension_url in extension.get("url")
            ),
            None,
        )
        if extension:

            # Update the flag
            extension["valueBoolean"] = True if registered else False

        else:
            # Add an extension indicating their use of Twitter
            extension = {
                "url": FHIR.picnichealth_extension_url,
                "valueBoolean": True if registered else False,
            }

            # Add it to their extensions
            patient.setdefault("extension", []).append(extension)

        return FHIR.put(request, path=f'/Patient/{patient["id"]}', data=patient)

    @staticmethod
    def update_document_reference(request, document_reference, status="current"):
        logger.debug("Supersede DocumentReference: {}".format(document_reference["id"]))

        # Set headers for patch operation
        headers = {"Content-Type": "application/json-patch+json"}

        # Prepare the list of updated operations
        data = [
            {"op": "replace", "path": "/status", "value": status},
        ]

        return FHIR.request(
            "patch",
            headers=headers,
            request=request,
            path=f'/DocumentReference/{document_reference["id"]}',
            data=data,
            check=True,
        )

    #
    # DELETE
    #

    @staticmethod
    def _delete_resources(request, source_resource_type, source_resource_id, target_resource_types=[]):
        """
        Removes a source resource and all of its related resources. Delete is done in a transaction
        so if an error occurs, the system will revert to its original state (in theory). This
        seems to bypass dependency issues and will just delete everything with impunity so
        use with caution.
        :param source_resource_type: The FHIR resource type of the source resource (e.g. Patient)
        :type source_resource_type: String
        :param source_resource_id: The FHIR id of the source resource
        :type source_resource_id: String
        :param target_resource_types: The resource types which should all be deleted
        if related to the source
        resource
        :type target_resource_types: [String]
        :return: Whether the delete succeeded or not
        :rtype: Bool
        """
        content = None
        try:
            logger.debug("Target resource: {}/{}".format(source_resource_type, source_resource_id))
            logger.debug("Target related resources: {}".format(target_resource_types))

            # Query existing resources
            query = {
                "_id": source_resource_id,
                "_include": "*",
                "_revinclude": "*",
            }

            # Make the request.
            source_response = FHIR.get(request, path="/", data=query)

            # Build the initial delete transaction bundle.
            transaction = {"resourceType": "Bundle", "type": "transaction", "entry": []}

            # Fetch IDs
            entries = source_response.json().get("entry", [])
            for resource in [
                entry["resource"]
                for entry in entries
                if entry.get("resource") is not None and entry["resource"]["resourceType"] in target_resource_types
            ]:
                # Get the ID and resource type
                _id = resource.get("id")
                resource_type = resource.get("resourceType")

                # Form the resource ID/URL
                resource_id = "{}/{}".format(resource_type, _id)

                # Add it.
                logger.debug("Add: {}".format(resource_id))
                transaction["entry"].append({"request": {"url": resource_id, "method": "DELETE"}})

            logger.debug("Delete request: {}".format(json.dumps(transaction)))

            # Do the delete.
            deleted = FHIR.post(request, path="/", data=transaction)
            if deleted:

                # Log it.
                logger.debug("Delete response: {}".format(deleted))
                logger.debug(
                    "Successfully deleted all for resource: {}/{}".format(source_resource_type, source_resource_id)
                )

            return deleted

        except Exception as e:
            logger.exception(
                "Delete error: {}".format(e),
                exc_info=True,
                extra={
                    "resource": "{}/{}".format(source_resource_type, source_resource_id),
                    "included_resources": target_resource_types,
                    "content": content,
                },
            )

        return False

    @staticmethod
    def _delete_resource(request, resource_type, resource_id):
        logger.debug("Delete request: {}/{}".format(resource_type, resource_id))

        # Do the delete.
        return FHIR.delete(request, path=f"/{resource_type}/{resource_id}")

    @staticmethod
    def delete_participant(patient_id):
        """
        Deletes the participant's entire FHIR record
        :param patient_id: The FHIR ID of the Patient
        :return: bool
        """
        # Set resources to purge
        resources = [
            "Patient",
            "QuestionnaireResponse",
            "Flag",
            "Consent",
            "Contract",
            "RelatedPerson",
            "Composition",
            "List",
            "DocumentReference",
            "ResearchSubject",
            "Communication",
            "Device",
        ]

        # Do the delete
        FHIR._delete_resources("Patient", patient_id, resources)

    @staticmethod
    def delete_patient(request, patient_id):
        """
        Deletes the patient resource
        :param patient_id: The identifier of the patient
        :return: bool
        """
        # Attempt to delete the patient and all related resources.
        return FHIR.delete(request, path=f"/Patient/{FHIR._patient_id(request, patient_id)}")

    @staticmethod
    def delete_research_subjects(request, patient_id):
        """
        Deletes the patient's points of care list
        :param patient_id: The identifier of the patient
        :return: bool
        """
        # Find it
        research_subjects = FHIR.query_research_subjects(request, patient_id, flatten_return=False)
        for research_subject in research_subjects:

            # Attempt to delete the patient and all related resources.
            FHIR.delete(request, path=f'/ResearchSubject/{research_subject["id"]}')

        else:
            logger.warning("Cannot delete")

    @staticmethod
    def delete_point_of_care_list(request, patient_id):
        """
        Deletes the patient's points of care list
        :param patient_id: The identifier of the patient
        :return: bool
        """
        # Find it
        point_of_care_list = FHIR.get_point_of_care_list(request, patient_id, flatten_return=False)
        if point_of_care_list:

            # Attempt to delete the patient and all related resources.
            FHIR.delete(request, path=f'/List/{point_of_care_list["id"]}')

        else:
            logger.warning("Cannot delete")

    @staticmethod
    def delete_questionnaire_response(request, patient_id, project):
        logger.debug("Deleting questionnaire response: Patient/{} - {}".format(patient_id, project))

        # Get the questionnaire ID
        questionnaire_id = PPM.Questionnaire.questionnaire_for_study(study=project)

        # Find it
        questionnaire_response = FHIR.get_questionnaire_response(request, patient_id, questionnaire_id)
        if questionnaire_response:

            # Delete it
            FHIR.delete(request, path=f'/QuestionnaireResponse/{questionnaire_response["id"]}')

        else:
            logger.error(
                "Could not delete QuestionnaireResponse, does not exist: Patient/{} - {}".format(
                    patient_id, questionnaire_id
                )
            )

    @staticmethod
    def delete_consent(request, patient_id, project):
        logger.debug("Deleting consents: Patient/{}".format(patient_id))

        # Build the transaction
        transaction = {"resourceType": "Bundle", "type": "transaction", "entry": []}

        # Add the composition delete
        transaction["entry"].append(
            {
                "request": {
                    "url": "Composition?subject=Patient/{}".format(patient_id),
                    "method": "DELETE",
                }
            }
        )

        # Add the consent delete
        transaction["entry"].append(
            {
                "request": {
                    "url": "Consent?patient=Patient/{}".format(patient_id),
                    "method": "DELETE",
                }
            }
        )

        # Add the contract delete
        transaction["entry"].append(
            {
                "request": {
                    "url": "Contract?signer=Patient/{}".format(patient_id),
                    "method": "DELETE",
                }
            }
        )

        # Add the consent document delete
        transaction["entry"].append(
            {
                "request": {
                    "url": "DocumentReference?subject=Patient/{}&type={}|{}&"
                    "related-ref={}".format(
                        patient_id,
                        FHIR.ppm_consent_type_system,
                        FHIR.ppm_consent_type_value,
                        PPM.Study.fhir_id(project),
                    ),
                    "method": "DELETE",
                }
            }
        )

        # Check project
        if project == "autism":

            questionnaire_ids = [
                "ppm-asd-consent-guardian-quiz",
                "ppm-asd-consent-individual-quiz",
                "individual-signature-part-1",
                "guardian-signature-part-1",
                "guardian-signature-part-2",
                "guardian-signature-part-3",
            ]

            # Add the questionnaire response delete
            for questionnaire_id in questionnaire_ids:
                transaction["entry"].append(
                    {
                        "request": {
                            "url": "QuestionnaireResponse?"
                            "questionnaire=Questionnaire/{}&source=Patient/{}".format(questionnaire_id, patient_id),
                            "method": "DELETE",
                        }
                    }
                )

            # Add the contract delete
            transaction["entry"].append(
                {
                    "request": {
                        "url": "Contract?signer.patient={}".format(patient_id),
                        "method": "DELETE",
                    }
                }
            )

            # Remove related persons
            transaction["entry"].append(
                {
                    "request": {
                        "url": "RelatedPerson?patient=Patient/{}".format(patient_id),
                        "method": "DELETE",
                    }
                }
            )

        elif project == "neer":

            # Delete questionnaire responses
            questionnaire_ids = ["neer-signature", "neer-signature-v2"]
            for questionnaire_id in questionnaire_ids:
                transaction["entry"].append(
                    {
                        "request": {
                            "url": "QuestionnaireResponse?"
                            "questionnaire=Questionnaire/{}&source=Patient/{}".format(questionnaire_id, patient_id),
                            "method": "DELETE",
                        }
                    }
                )

        else:
            logger.error("Unsupported project: {}".format(project), extra={"ppm_id": patient_id})

        # Make the FHIR request.
        return FHIR.post(request, path="/", data=json.dumps(transaction))

    #
    # BUNDLES
    #

    @staticmethod
    def get_ppm_research_studies(request, bundle, flatten_result=True):

        # Find Research subjects (without identifiers, so as to exclude PPM resources)
        subjects = FHIR.get_ppm_research_subjects(bundle, flatten_result=False)
        if not subjects:
            logger.debug("No Research Subjects, no Research Studies")
            return None

        # Get study IDs
        research_study_ids = [subject["study"]["reference"].split("/")[1] for subject in subjects]

        # Make the query
        query = {"_id": ",".join(research_study_ids)}

        # Get the IDs
        research_studies = FHIR._query_resources(request, resource_type="ResearchStudy", query=query)

        if flatten_result:
            # Return the titles
            return [research_study["title"] for research_study in research_studies]
        else:
            return research_studies

    @staticmethod
    def get_research_studies(request, bundle, flatten_result=True):

        # Find Research subjects (without identifiers, so as to exclude PPM resources)
        subjects = FHIR.get_research_subjects(bundle, flatten_result=False)
        if not subjects:
            logger.debug("No Research Subjects, no Research Studies")
            return None

        # Get study IDs
        research_study_ids = [subject["study"]["reference"].split("/")[1] for subject in subjects]

        # Make the query
        query = {"_id": ",".join(research_study_ids)}

        # Get the IDs
        research_studies = FHIR._query_resources(request, resource_type="ResearchStudy", query=query)

        if flatten_result:
            # Return the titles
            return [research_study["title"] for research_study in research_studies]
        else:
            return research_studies

    @staticmethod
    def get_ppm_research_subjects(bundle, flatten_result=True):

        # Find Research subjects (without identifiers, so as to exclude PPM resources)
        research_subjects = [
            entry["resource"]
            for entry in bundle["entry"]
            if entry["resource"]["resourceType"] == "ResearchSubject"
            and entry["resource"].get("study", {}).get("reference", None)
            in ["ResearchStudy/ppm-{}".format(study.value) for study in PPM.Project]
        ]

        if flatten_result:
            # Return the titles
            return [FHIR.flatten_research_subject(resource) for resource in research_subjects]
        else:
            return [resource for resource in research_subjects]

    @staticmethod
    def get_research_subjects(bundle, flatten_result=True):

        # Find Research subjects (without identifiers, so as to exclude PPM resources)
        research_subjects = [
            entry["resource"]
            for entry in bundle["entry"]
            if entry["resource"]["resourceType"] == "ResearchSubject"
            and entry["resource"].get("study", {}).get("reference", None)
            not in ["ResearchStudy/ppm-{}".format(study.value) for study in PPM.Project]
        ]

        if flatten_result:
            # Return the titles
            return [FHIR.flatten_research_subject(resource) for resource in research_subjects]
        else:
            return [resource for resource in research_subjects]

    #
    # OUTPUT
    #

    @staticmethod
    def get_ppm_id(request, email):

        # Return patient
        patient = FHIR.get_patient(request, email)
        if not patient:
            return None

        return patient.get("id", None)

    @staticmethod
    def get_name(patient, full=False):

        # Default to a generic name
        names = []

        # Check official names
        for name in [name for name in patient["name"] if name.get("use") == "official"]:
            if name.get("given"):
                names.extend(name["given"])

            # Add family if full name
            if name.get("family") and (full or not names):
                names.append(name["family"])

        if not names:
            logger.error("Could not find name for {}".format(patient.id))

            # Default to their email address
            email = next(
                (
                    identifier["value"]
                    for identifier in patient["identifier"]
                    if identifier.get("system") == FHIR.patient_email_identifier_system
                ),
                None,
            )

            if email:
                names.append(email)

            else:
                logger.error("Could not find email for {}".format(patient.id))

        if not names:
            names = ["Participant"]

        return " ".join(names)

    @staticmethod
    def flatten_participant(request, bundle):
        """
        Accepts a Bundle containing everything related to a Patient resource
        and flattens the data into something easier to build templates/views with.
        :param bundle: The Patient resource bundle as JSON/dict
        :type bundle: dict
        :return: A flattened dictionary of the Participant/Patient's entire FHIR
        data record
        :rtype: dict
        """

        # Build a dictionary
        participant = {}

        # Set aside common properties
        ppm_id = None
        email = None

        try:
            # Flatten patient profile
            participant = FHIR.flatten_patient(bundle)
            if not participant:
                logger.debug("No Patient in bundle")
                return {}

            # Get props
            ppm_id = participant["fhir_id"]
            email = participant["email"]

            # Get the PPM study/project resources
            studies = FHIR.flatten_ppm_studies(bundle)
            if len(studies) > 1:
                logger.warning("Patient/{} has more than one PPM study: {}".format(ppm_id, studies))

            # Check for accepted and a start date
            participant["project"] = participant["study"] = studies[0]["study"]
            participant["date_registered"] = FHIR._format_date(studies[0]["start"], "%m/%d/%Y")
            participant["datetime_registered"] = studies[0]["start"]

            # Get the enrollment properties
            enrollment = FHIR.flatten_enrollment(bundle)

            # Set status and dates
            participant["enrollment"] = enrollment["enrollment"]
            participant["date_enrollment_updated"] = FHIR._format_date(enrollment["updated"], "%m/%d/%Y")
            participant["datetime_enrollment_updated"] = enrollment["updated"]
            if enrollment.get("start"):

                # Convert time zone to assumed ET
                participant["enrollment_accepted_date"] = FHIR._format_date(enrollment["start"], "%m/%d/%Y")

            else:
                participant["enrollment_accepted_date"] = ""

            # Check for completed/terminated
            if enrollment.get("end"):

                # Convert time zone to assumed ET
                participant["enrollment_terminated_date"] = FHIR._format_date(enrollment["end"], "%m/%d/%Y")
            #
            # else:
            #     participant['enrollment_terminated_date'] = ''

            # Flatten consent composition
            participant["composition"] = FHIR.flatten_consent_composition(bundle)

            # Get the project
            _questionnaire_id = PPM.Questionnaire.questionnaire_for_study(study=participant["project"])

            # Parse out the responses
            participant["questionnaire"] = FHIR.flatten_questionnaire_response(bundle, _questionnaire_id)

            # Flatten points of care
            participant["points_of_care"] = FHIR.flatten_list(bundle, "Organization")

            # Flatten consent composition
            participant["devices"] = FHIR.flatten_ppm_devices(bundle)

            # Check for research studies
            research_studies = FHIR.get_research_studies(request, bundle)
            if research_studies:
                participant["research_studies"] = research_studies

            # Autism has a special consent with a quiz, get that content and add it
            if participant["project"] == PPM.Study.ASD.value:

                # Initially none
                participant["consent_quiz"] = None
                participant["consent_quiz_answers"] = None

                # Check if they've even consented
                if participant.get("composition"):

                    # Get the Questionnaire ID used for the quiz portion of the consent
                    quiz_id = PPM.Questionnaire.questionnaire_for_consent(participant.get("composition"))

                    # Flatten the Q's and A's for output
                    quiz = FHIR.flatten_questionnaire_response(bundle, quiz_id)
                    if quiz:

                        # Add it
                        participant["consent_quiz"] = quiz
                        participant["consent_quiz_answers"] = FHIR.questionnaire_answers(bundle, quiz_id)

            # Get study specific resources
            if PPM.Study.enum(participant["study"]) is PPM.Study.NEER:
                participant[PPM.Study.NEER.value] = FHIR._flatten_neer_participant(bundle=bundle, ppm_id=ppm_id)

            elif PPM.Study.enum(participant["study"]) is PPM.Study.RANT:
                participant[PPM.Study.RANT.value] = FHIR._flatten_rant_participant(bundle=bundle, ppm_id=ppm_id)

            elif PPM.Study.enum(participant["study"]) is PPM.Study.ASD:
                participant[PPM.Study.ASD.value] = FHIR._flatten_asd_participant(bundle=bundle, ppm_id=ppm_id)

            elif PPM.Study.enum(participant["study"]) is PPM.Study.EXAMPLE:
                participant[PPM.Study.EXAMPLE.value] = FHIR._flatten_example_participant(bundle=bundle, ppm_id=ppm_id)

        except Exception as e:
            logger.exception(
                "FHIR error: {}".format(e),
                exc_info=True,
                extra={"ppm_id": ppm_id, "email": email},
            )

        return participant

    @staticmethod
    def _flatten_asd_participant(bundle, ppm_id):
        """
        Continues flattening a participant by adding any study specific data to
        their record. This will include answers in questionnaires, etc.
        :param bundle: The participant's entire FHIR record
        :param ppm_id: The PPM ID of the participant
        :return: dict
        """
        logger.debug(f"PPM/{ppm_id}/FHIR: Flattening ASD participant")

        # Put values in a dictionary
        values = {}

        # TODO: Implement this
        logger.warning(f"PPM/ASD/{ppm_id}/FHIR: Flattening ASD participant needs to be " f"fully implemented")

        return values

    @staticmethod
    def _flatten_neer_participant(bundle, ppm_id):
        """
        Continues flattening a participant by adding any study specific data to their
        record. This will include answers in questionnaires, etc.
        :param bundle: The participant's entire FHIR record
        :param ppm_id: The PPM ID of the participant
        :return: dict
        """
        logger.debug(f"PPM/{ppm_id}/FHIR: Flattening NEER participant")

        # Put values in a dictionary
        values = {}

        # Get questionnaire answers
        questionnaire_response = next(
            (
                q
                for q in FHIR._find_resources(bundle, "QuestionnaireResponse")
                if q["questionnaire"]["reference"] == f"Questionnaire/{PPM.Questionnaire.NEERQuestionnaire.value}"
            ),
            None,
        )
        if questionnaire_response:
            logger.debug(f"PPM/{ppm_id}/FHIR: Flattening QuestionnaireResponse/" f'{questionnaire_response["id"]}')

            # Map linkIds to keys
            text_answers = {
                "question-12": "diagnosis",
                "question-24": "pcp",
                "question-25": "oncologist",
            }

            date_answers = {
                "question-5": "birthdate",
                "question-14": "date_diagnosis",
            }

            # Iterate items
            for link_id, key in text_answers.items():
                try:
                    # Get the answer
                    answer = next(
                        i["answer"][0]["valueString"] for i in questionnaire_response["item"] if i["linkId"] == link_id
                    )

                    # Assign it
                    values[key] = answer
                except Exception as e:
                    logger.exception(
                        f"PPM/{ppm_id}/Questionnaire/{link_id}: {e}",
                        exc_info=True,
                        extra={
                            "ppm_id": ppm_id,
                            "link_id": link_id,
                            "key": key,
                            "questionnaire_response": f"QuestionnaireResponse/" f'{questionnaire_response["id"]}',
                            "item": next(
                                (i for i in questionnaire_response["item"] if i["linkId"] == link_id),
                                "",
                            ),
                        },
                    )

                    # Assign default value
                    values[key] = "---"

            # Iterate date items and attempt to parse dates, otherwise treat as text
            for link_id, key in date_answers.items():

                try:
                    # Get the answer
                    answer = next(
                        i["answer"][0]["valueString"] for i in questionnaire_response["item"] if i["linkId"] == link_id
                    )

                    try:
                        # Attempt to parse it
                        answer_date = parse(answer)

                        # Assign it
                        values[key] = answer_date.isoformat()

                    except ValueError:
                        logger.debug(f"PPM/{ppm_id}/Questionnaire/{link_id}: " f"Invalid date: {answer}")

                        # Assign the raw value
                        values[key] = answer

                except Exception as e:
                    logger.exception(
                        f"PPM/{ppm_id}/Questionnaire/{link_id}: {e}",
                        exc_info=True,
                        extra={
                            "ppm_id": ppm_id,
                            "link_id": link_id,
                            "key": key,
                            "questionnaire_response": f"QuestionnaireResponse/" f'{questionnaire_response["id"]}',
                            "item": next(
                                (i for i in questionnaire_response["item"] if i["linkId"] == link_id),
                                "",
                            ),
                        },
                    )

                    # Assign default value
                    values[key] = "---"

        return values

    @staticmethod
    def _flatten_rant_participant(bundle, ppm_id):
        """
        Continues flattening a participant by adding any study specific data to their
        record. This will include answers in questionnaires, etc.
        :param bundle: The participant's entire FHIR record
        :param ppm_id: The PPM ID of the participant
        :return: dict
        """
        logger.debug(f"PPM/{ppm_id}/FHIR: Flattening RANT participant")

        # Put values in a dictionary
        values = {}

        # Get questionnaire answers
        questionnaire_response = next(
            (
                q
                for q in FHIR._find_resources(bundle, "QuestionnaireResponse")
                if q["questionnaire"]["reference"] == f"Questionnaire/{PPM.Questionnaire.RANTQuestionnaire.value}"
            ),
            None,
        )
        if questionnaire_response:
            logger.debug(f"PPM/{ppm_id}/FHIR: Flattening QuestionnaireResponse/" f'{questionnaire_response["id"]}')

            # Map linkIds to keys
            text_answers = {
                "question-12": "diagnosis",
                "question-24": "pcp",
                "question-25": "oncologist",
            }

            date_answers = {
                "question-5": "birthdate",
                "question-14": "date_diagnosis",
            }

            # Iterate items
            for link_id, key in text_answers.items():
                try:
                    # Get the answer
                    answer = next(
                        i["answer"][0]["valueString"] for i in questionnaire_response["item"] if i["linkId"] == link_id
                    )

                    # Assign it
                    values[key] = answer
                except Exception as e:
                    logger.exception(
                        f"PPM/{ppm_id}/Questionnaire/{link_id}: {e}",
                        exc_info=True,
                        extra={
                            "ppm_id": ppm_id,
                            "link_id": link_id,
                            "key": key,
                            "questionnaire_response": f"QuestionnaireResponse/" f'{questionnaire_response["id"]}',
                            "item": next(
                                (i for i in questionnaire_response["item"] if i["linkId"] == link_id),
                                "",
                            ),
                        },
                    )

                    # Assign default value
                    values[key] = "---"

            # Iterate date items and attempt to parse dates, otherwise treat as text
            for link_id, key in date_answers.items():

                try:
                    # Get the answer
                    answer = next(
                        i["answer"][0]["valueString"] for i in questionnaire_response["item"] if i["linkId"] == link_id
                    )

                    try:
                        # Attempt to parse it
                        answer_date = parse(answer)

                        # Assign it
                        values[key] = answer_date.isoformat()

                    except ValueError:
                        logger.debug(f"PPM/{ppm_id}/Questionnaire/{link_id}: Invalid date: " f"{answer}")

                        # Assign the raw value
                        values[key] = answer

                except Exception as e:
                    logger.exception(
                        f"PPM/{ppm_id}/Questionnaire/{link_id}: {e}",
                        exc_info=True,
                        extra={
                            "ppm_id": ppm_id,
                            "link_id": link_id,
                            "key": key,
                            "questionnaire_response": f"QuestionnaireResponse/" f'{questionnaire_response["id"]}',
                            "item": next(
                                (i for i in questionnaire_response["item"] if i["linkId"] == link_id),
                                "",
                            ),
                        },
                    )

                    # Assign default value
                    values[key] = "---"

        return values

    @staticmethod
    def _flatten_example_participant(bundle, ppm_id):
        """
        Continues flattening a participant by adding any study specific data to
        their record. This will include answers in questionnaires, etc.
        :param bundle: The participant's entire FHIR record
        :param ppm_id: The PPM ID of the participant
        :return: dict
        """
        logger.debug(f"PPM/{ppm_id}/FHIR: Flattening EXAMPLE participant")

        # Put values in a dictionary
        values = {}

        # Get questionnaire answers
        questionnaire_response = next(
            (
                q
                for q in FHIR._find_resources(bundle, "QuestionnaireResponse")
                if q["questionnaire"]["reference"] == f"Questionnaire/{PPM.Questionnaire.EXAMPLEQuestionnaire.value}"
            ),
            None,
        )
        if questionnaire_response:
            logger.debug(f"PPM/{ppm_id}/FHIR: Flattening QuestionnaireResponse/" f'{questionnaire_response["id"]}')

            # Map linkIds to keys
            text_answers = {
                "question-12": "diagnosis",
                "question-24": "pcp",
                "question-25": "oncologist",
            }

            date_answers = {
                "question-5": "birthdate",
                "question-14": "date_diagnosis",
            }

            # Iterate items
            for link_id, key in text_answers.items():
                try:
                    # Get the answer
                    answer = next(
                        i["answer"][0]["valueString"] for i in questionnaire_response["item"] if i["linkId"] == link_id
                    )

                    # Assign it
                    values[key] = answer
                except Exception as e:
                    logger.exception(
                        f"PPM/{ppm_id}/Questionnaire/{link_id}: {e}",
                        exc_info=True,
                        extra={
                            "ppm_id": ppm_id,
                            "link_id": link_id,
                            "key": key,
                            "questionnaire_response": f"QuestionnaireResponse/" f'{questionnaire_response["id"]}',
                            "item": next(
                                (i for i in questionnaire_response["item"] if i["linkId"] == link_id),
                                "",
                            ),
                        },
                    )

                    # Assign default value
                    values[key] = "---"

            # Iterate date items and attempt to parse dates, otherwise treat as text
            for link_id, key in date_answers.items():

                try:
                    # Get the answer
                    answer = next(
                        i["answer"][0]["valueString"] for i in questionnaire_response["item"] if i["linkId"] == link_id
                    )

                    try:
                        # Attempt to parse it
                        answer_date = parse(answer)

                        # Assign it
                        values[key] = answer_date.isoformat()

                    except ValueError:
                        logger.debug(f"PPM/{ppm_id}/Questionnaire/{link_id}: Invalid date: " f"{answer}")

                        # Assign the raw value
                        values[key] = answer

                except Exception as e:
                    logger.exception(
                        f"PPM/{ppm_id}/Questionnaire/{link_id}: {e}",
                        exc_info=True,
                        extra={
                            "ppm_id": ppm_id,
                            "link_id": link_id,
                            "key": key,
                            "questionnaire_response": f"QuestionnaireResponse/" f'{questionnaire_response["id"]}',
                            "item": next(
                                (i for i in questionnaire_response["item"] if i["linkId"] == link_id),
                                "",
                            ),
                        },
                    )

                    # Assign default value
                    values[key] = "---"

        return values

    @staticmethod
    def flatten_questionnaire_response(bundle_dict, questionnaire_id):
        """
        Picks out the relevant Questionnaire and QuestionnaireResponse resources and
        returns a dict mapping the text of each question to a list of answer texts.
        To handle duplicate question texts, each question is prepended with an index.
        :param bundle_dict: The parsed JSON response from a FHIR query
        :param questionnaire_id: The ID of the Questionnaire to parse for
        :return: dict
        """

        # Build the bundle
        bundle = Bundle(bundle_dict)

        # Pick out the questionnaire and its response
        questionnaire = next(
            (entry.resource for entry in bundle.entry if entry.resource.id == questionnaire_id),
            None,
        )
        questionnaire_response = next(
            (
                entry.resource
                for entry in bundle.entry
                if entry.resource.resource_type == "QuestionnaireResponse"
                and entry.resource.questionnaire.reference == "Questionnaire/{}".format(questionnaire_id)
            ),
            None,
        )

        # Ensure resources exist
        if not questionnaire or not questionnaire_response:
            logger.debug("User has no responses for Questionnaire/{}, returning".format(questionnaire_id))
            return None

        # Get questions and answers
        questions = FHIR._questions(questionnaire.item)
        answers = FHIR._answers(questionnaire_response.item)

        # Process sub-questions first
        for linkId, condition in {
            linkId: condition for linkId, condition in questions.items() if type(condition) is dict
        }.items():

            try:
                # Assume only one condition, fetch the parent question linkId
                parent = next(iter(condition))
                if not parent:
                    logger.warning(
                        "FHIR Error: Subquestion not properly specified: {}:{}".format(linkId, condition),
                        extra={
                            "questionnaire": questionnaire_id,
                            "ppm_id": questionnaire_response.source,
                            "questionnaire_response": questionnaire_response.id,
                        },
                    )
                    continue

                if len(condition) > 1:
                    logger.warning(
                        "FHIR Error: Subquestion has multiple conditions: {}:{}".format(linkId, condition),
                        extra={
                            "questionnaire": questionnaire_id,
                            "ppm_id": questionnaire_response.source,
                            "questionnaire_response": questionnaire_response.id,
                        },
                    )

                # Ensure they've answered this one
                if not answers.get(parent) or condition[parent] not in answers.get(parent):
                    continue

                # Get the question and answer item
                answer = answers[parent]
                index = answer.index(condition[parent])

                # Check for commas
                sub_answers = answers[linkId]
                if "," in next(iter(sub_answers)):

                    # Split it
                    sub_answers = [sub.strip() for sub in next(iter(sub_answers)).split(",")]

                # Format them
                value = '{} <span class="label label-primary">{}</span>'.format(
                    answer[index],
                    '</span>&nbsp;<span class="label label-primary">'.join(sub_answers),
                )

                # Append the value
                answer[index] = mark_safe(value)

            except Exception as e:
                logger.exception(
                    "FHIR error: {}".format(e),
                    exc_info=True,
                    extra={
                        "questionnaire": questionnaire_id,
                        "link_id": linkId,
                        "ppm_id": questionnaire_response.source,
                    },
                )

        # Build the response
        response = collections.OrderedDict()

        # Process top-level questions first
        top_questions = collections.OrderedDict(
            sorted(
                {linkId: question for linkId, question in questions.items() if type(question) is str}.items(),
                key=lambda q: int(q[0].split("-")[1]),
            )
        )
        for linkId, question in top_questions.items():

            # Check for the answer
            answer = answers.get(linkId)
            if not answer:
                answer = [mark_safe('<span class="label label-info">N/A</span>')]
                logger.debug(
                    f"FHIR Questionnaire: No answer found for {linkId}",
                    extra={
                        "questionnaire": questionnaire_id,
                        "link_id": linkId,
                        "ppm_id": questionnaire_response.source,
                    },
                )

            # Format the question text
            text = "{}. {}".format(len(response.keys()) + 1, question)

            # Add the answer
            response[text] = answer

        # Add the date that the questionnaire was completed
        authored_date = questionnaire_response.authored.origval
        formatted_authored_date = FHIR._format_date(authored_date, "%m/%d/%Y")

        return {
            "ppm_id": FHIR._get_referenced_id(questionnaire_response.as_json(), "Patient"),
            "authored": formatted_authored_date,
            "responses": response,
        }

    @staticmethod
    def _questions(items):

        # Iterate items
        questions = {}
        for item in items:

            # Leave out display or ...
            if item.type == "display":
                continue

            elif item.type == "group" and item.item:

                # Get answers
                sub_questions = FHIR._questions(item.item)

                # Add them
                questions.update(sub_questions)

            elif item.enableWhen:

                # This is a sub-question
                questions[item.linkId] = {
                    next(condition.question for condition in item.enableWhen): next(
                        condition.answerString for condition in item.enableWhen
                    )
                }

            else:

                # Ensure it has text
                if item.text:
                    # List them out
                    questions[item.linkId] = item.text

                else:
                    # Indicate a blank question text, presumably a sub-question
                    questions[item.linkId] = "-"

                # Check for subtypes
                if item.item:
                    # Get answers
                    sub_questions = FHIR._questions(item.item)

                    # Add them
                    questions.update(sub_questions)

        return questions

    @staticmethod
    def _answers(items):

        # Iterate items
        responses = {}
        for item in items:

            # List them out
            responses[item.linkId] = []

            # Ensure we've got answers
            if not item.answer:
                logger.error(
                    "FHIR questionnaire error: Missing items for question",
                    extra={"link_id": item.linkId},
                )
                responses[item.linkId] = ["------"]

            else:

                # Iterate answers
                for answer in item.answer:

                    # Get the value
                    if answer.valueBoolean is not None:
                        responses[item.linkId].append(answer.valueBoolean)
                    elif answer.valueString is not None:
                        responses[item.linkId].append(answer.valueString)
                    elif answer.valueInteger is not None:
                        responses[item.linkId].append(answer.valueInteger)
                    elif answer.valueDate is not None:
                        responses[item.linkId].append(answer.valueDate)
                    elif answer.valueDateTime is not None:
                        responses[item.linkId].append(answer.valueDateTime)
                    elif answer.valueDateTime is not None:
                        responses[item.linkId].append(answer.valueDateTime)

                    else:
                        logger.warning(
                            "Unhandled answer value type: {}".format(answer.as_json()),
                            extra={"link_id": item.linkId},
                        )

            # Check for subtypes
            if item.item:
                # Get answers
                sub_answers = FHIR._answers(item.item)

                # Add them
                responses[item.linkId].extend(sub_answers)

        return responses

    @staticmethod
    def flatten_patient(bundle_dict):

        # Get the patient
        resource = next(
            (
                entry["resource"]
                for entry in bundle_dict.get("entry", [])
                if entry["resource"]["resourceType"] == "Patient"
            ),
            None,
        )

        # Check for a resource
        if not resource:
            logger.debug("Cannot flatten Patient, one did not exist in bundle")
            return None

        # Collect properties
        patient = dict()

        # Get FHIR IDs
        patient["fhir_id"] = patient["ppm_id"] = resource["id"]

        # Parse out email
        patient["email"] = next(
            (
                identifier["value"]
                for identifier in resource.get("identifier", [])
                if identifier.get("system") == FHIR.patient_email_identifier_system
            )
        )
        if not patient.get("email"):
            logger.error("Could not parse email from Patient/{}! This should not be possible".format(resource["id"]))
            return {}

        # Get status
        patient["active"] = FHIR._get_or(resource, ["active"], "")

        # Get the remaining optional properties
        patient["firstname"] = FHIR._get_or(resource, ["name", 0, "given", 0], "")
        patient["lastname"] = FHIR._get_or(resource, ["name", 0, "family"], "")
        patient["street_address1"] = FHIR._get_or(resource, ["address", 0, "line", 0], "")
        patient["street_address2"] = FHIR._get_or(resource, ["address", 0, "line", 1], "")
        patient["city"] = FHIR._get_or(resource, ["address", 0, "city"], "")
        patient["state"] = FHIR._get_or(resource, ["address", 0, "state"], "")
        patient["zip"] = FHIR._get_or(resource, ["address", 0, "postalCode"], "")
        patient["phone"] = FHIR._get_or(resource, ["telecom", 0, "postalCode"], "")

        # Check for deceased
        if FHIR._get_or(resource, ["deceasedDateTime"], None):
            patient["deceased"] = FHIR._format_date(resource["deceasedDateTime"], "%m/%d/%Y")

        # Parse telecom properties
        patient["phone"] = next(
            (
                telecom.get("value", "")
                for telecom in resource.get("telecom", [])
                if telecom.get("system") == FHIR.patient_phone_telecom_system
            ),
            "",
        )
        patient["twitter_handle"] = next(
            (
                telecom.get("value", "")
                for telecom in resource.get("telecom", [])
                if telecom.get("system") == FHIR.patient_twitter_telecom_system
            ),
            "",
        )
        patient["contact_email"] = next(
            (
                telecom.get("value", "")
                for telecom in resource.get("telecom", [])
                if telecom.get("system") == FHIR.patient_email_telecom_system
            ),
            "",
        )

        # Determine if admins have been notified of their completion of initial registration
        patient["admin_notified"] = next(
            (
                extension["valueDateTime"]
                for extension in resource.get("extension", [])
                if "admin-notified" in extension.get("url")
            ),
            None,
        )

        # Get how they heard about PPM
        patient["how_did_you_hear_about_us"] = next(
            (
                extension["valueString"]
                for extension in resource.get("extension", [])
                if "how-did-you-hear-about-us" in extension.get("url")
            ),
            "",
        )

        # Get if they are not using Twitter
        patient["uses_twitter"] = next(
            (
                extension["valueBoolean"]
                for extension in resource.get("extension", [])
                if "uses-twitter" in extension.get("url")
            ),
            True,
        )

        # Get if they are not using Fitbit
        patient["uses_fitbit"] = next(
            (
                extension["valueBoolean"]
                for extension in resource.get("extension", [])
                if "uses-fitbit" in extension.get("url")
            ),
            True,
        )

        # Get if they are not using Fitbit
        patient["uses_facebook"] = next(
            (
                extension["valueBoolean"]
                for extension in resource.get("extension", [])
                if "uses-facebook" in extension.get("url")
            ),
            True,
        )

        # Get if they are not using SMART on FHIR / EHR
        patient["uses_smart_on_fhir"] = next(
            (
                extension["valueBoolean"]
                for extension in resource.get("extension", [])
                if "uses-smart-on-fhir" in extension.get("url")
            ),
            True,
        )

        # Get if they are registered with Picnichealth
        patient["picnichealth"] = next(
            (
                extension["valueBoolean"]
                for extension in resource.get("extension", [])
                if FHIR.picnichealth_extension_url in extension.get("url")
            ),
            False,
        )

        return patient

    @staticmethod
    def flatten_research_subject(resource):

        # Get the actual resource in case we were handed a BundleEntry
        resource = FHIR._get_or(resource, ["resource"], resource)

        # Get the resource.
        record = dict()

        # Try and get the values
        record["start"] = FHIR._get_or(resource, ["period", "start"])
        record["end"] = FHIR._get_or(resource, ["period", "end"])

        # Get the study ID
        record["study"] = FHIR.get_study_from_research_subject(resource)

        # Link back to participant
        record["ppm_id"] = FHIR._get_referenced_id(resource, "Patient")

        return record

    @staticmethod
    def flatten_research_study(resource):

        # Get the actual resource in case we were handed a BundleEntry
        resource = FHIR._get_or(resource, ["resource"], resource)

        # Get the resource.
        record = dict()

        # Try and get the values
        record["start"] = FHIR._get_or(resource, ["period", "start"])
        record["end"] = FHIR._get_or(resource, ["period", "end"])
        record["status"] = FHIR._get_or(resource, ["status"])
        record["title"] = FHIR._get_or(resource, ["title"])

        if resource.get("identifier"):
            record["identifier"] = FHIR._get_or(resource, ["identifier", 0, "value"])

        return record

    @staticmethod
    def flatten_ppm_studies(bundle):
        """
        Find and returns the flattened PPM research studies
        """
        # Collect them
        research_subjects = []
        for research_subject in FHIR._find_resources(bundle, "ResearchSubject"):

            # Ensure it's the PPM kind
            if FHIR.is_ppm_research_subject(research_subject):

                # Flatten it and add it
                research_subjects.append(FHIR.flatten_research_subject(research_subject))

        if not research_subjects:
            logger.debug("No ResearchSubjects found in bundle")

        return research_subjects

    @staticmethod
    def flatten_ppm_devices(bundle):
        """
        Find and returns the flattened Devices used to track PPM items/devices/kits
        """
        # Collect flattened items
        devices = []

        # Iterate all Device resources in the bundle
        for device in FHIR._find_resources(bundle, "Device"):

            # Ensure it's a PPM device
            for identifier in device.get("identifier", []):
                if identifier.get("system") == FHIR.device_identifier_system:

                    # Flatten it
                    devices.append(FHIR.flatten_ppm_device(device))

        return devices

    @staticmethod
    def flatten_ppm_device(resource):

        # Get the actual resource in case we were handed a BundleEntry
        resource = FHIR._get_or(resource, ["resource"], resource)

        # Get the resource.
        record = dict()

        # Try and get the values
        record["status"] = FHIR._get_or(resource, ["status"])
        record["shipped"] = FHIR._get_or(resource, ["manufactureDate"])
        record["returned"] = FHIR._get_or(resource, ["expirationDate"])

        # Get the proper identifier
        for identifier in resource.get("identifier", []):
            if identifier.get("system") == FHIR.device_identifier_system:

                # Set properties
                record["identifier"] = identifier["value"]
                break

        else:
            record["identifier"] = ""

        # Get the proper coding
        for coding in FHIR._get_or(resource, ["type", "coding"], []):
            if coding.get("system") == FHIR.device_coding_system:

                # Set properties
                record["type"] = coding["code"]
                record["name"] = coding["display"]
                break

        else:
            record["type"] = ""
            record["name"] = ""

        # Link back to participant
        record["ppm_id"] = FHIR._get_referenced_id(resource, "Patient", key="patient")

        return record

    @staticmethod
    def flatten_enrollment(bundle):
        """
        Find and returns the flattened enrollment Flag used to track PPM enrollment
        status
        """
        for flag in FHIR._find_resources(bundle, "Flag"):

            # Ensure it's the enrollment flag
            if FHIR.enrollment_flag_coding_system == FHIR._get_or(flag, ["code", "coding", 0, "system"]):

                # Flatten and return it
                return FHIR.flatten_enrollment_flag(flag)

            logger.error("No Flag with coding: {} found".format(FHIR.enrollment_flag_coding_system))

        logger.debug("No Flags found in bundle")
        return None

    @staticmethod
    def flatten_enrollment_flag(resource):

        # Get the actual resource in case we were handed a BundleEntry
        resource = FHIR._get_or(resource, ["resource"], resource)

        # Get the resource.
        record = dict()

        # Try and get the values
        record["enrollment"] = FHIR._get_or(resource, ["code", "coding", 0, "code"])
        record["status"] = FHIR._get_or(resource, ["status"])
        record["start"] = FHIR._get_or(resource, ["period", "start"])
        record["end"] = FHIR._get_or(resource, ["period", "end"])
        record["updated"] = FHIR._get_or(resource, ["meta", "lastUpdated"])

        # Link back to participant
        record["ppm_id"] = FHIR._get_referenced_id(resource, "Patient")

        return record

    @staticmethod
    def flatten_consent_composition(bundle_json):
        logger.debug("Flatten composition")

        # Add link IDs.
        FHIR._fix_bundle_json(bundle_json)

        # Parse the bundle in not so strict mode
        incoming_bundle = Bundle(bundle_json, strict=True)

        # Prepare the object.
        consent_object = {
            "consent_questionnaires": [],
            "assent_questionnaires": [],
        }
        consent_exceptions = []
        assent_exceptions = []

        if incoming_bundle.total > 0:

            for bundle_entry in incoming_bundle.entry:
                if bundle_entry.resource.resource_type == "Consent":

                    signed_consent = bundle_entry.resource

                    # We can pull the date from the Consent Resource. It's stamped
                    # in a few places.
                    date_time = signed_consent.dateTime.origval

                    # Format it
                    consent_object["date_signed"] = FHIR._format_date(date_time, "%m/%d/%Y")

                    # Exceptions are for when they refuse part of the consent.
                    if signed_consent.except_fhir:
                        for consent_exception in signed_consent.except_fhir:

                            # Check for conversion
                            display = consent_exception.code[0].display
                            consent_exceptions.append(FHIR._exception_description(display))

                elif bundle_entry.resource.resource_type == "Composition":

                    composition = bundle_entry.resource

                    entries = [section.entry for section in composition.section if section.entry is not None]
                    references = [
                        entry[0].reference for entry in entries if len(entry) > 0 and entry[0].reference is not None
                    ]
                    text = [section.text.div for section in composition.section if section.text is not None][0]

                    # Check the references for a Consent object, making this comp the
                    # consent one.
                    if len([r for r in references if "Consent" in r]) > 0:
                        consent_object["consent_text"] = text
                    else:
                        consent_object["assent_text"] = text

                elif bundle_entry.resource.resource_type == "RelatedPerson":
                    pass
                elif bundle_entry.resource.resource_type == "Contract":

                    contract = bundle_entry.resource

                    # Contracts with a binding reference are either the individual
                    # consent or the guardian consent.
                    if contract.bindingReference:

                        # Fetch the questionnaire and its responses.
                        questionnaire_response_id = re.search(
                            r"[^\/](\d+)$", contract.bindingReference.reference
                        ).group(0)
                        q_response = next(
                            (
                                entry.resource
                                for entry in incoming_bundle.entry
                                if entry.resource.resource_type == "QuestionnaireResponse"
                                and entry.resource.id == questionnaire_response_id
                            ),
                            None,
                        )

                        if not q_response:
                            logger.error("Could not find bindingReference QR for " "Contract/{}".format(contract.id))
                            break

                        # Get the questionnaire and its response.
                        questionnaire_id = q_response.questionnaire.reference.split("/")[1]
                        questionnaire = [
                            entry.resource
                            for entry in incoming_bundle.entry
                            if entry.resource.resource_type == "Questionnaire" and entry.resource.id == questionnaire_id
                        ][0]

                        if not q_response or not questionnaire:
                            logger.error(
                                "FHIR Error: Could not find bindingReference "
                                "Questionnaire/Response for Contract/{}".format(contract.id),
                                extra={
                                    "ppm_id": contract.subject,
                                    "questionnaire": questionnaire_id,
                                    "questionnaire_response": questionnaire_response_id,
                                },
                            )
                            break

                        # The reference refers to a Questionnaire which is linked to
                        # a part of the consent form.
                        if q_response.questionnaire.reference == "Questionnaire/guardian-signature-part-1":

                            # This is a person consenting for someone else.
                            consent_object["type"] = "GUARDIAN"

                            related_id = contract.signer[0].party.reference.split("/")[1]
                            related_person = [
                                entry.resource
                                for entry in incoming_bundle.entry
                                if entry.resource.resource_type == "RelatedPerson" and entry.resource.id == related_id
                            ][0]

                            consent_object["signer_name"] = related_person.name[0].text
                            consent_object["signer_relationship"] = related_person.relationship.text

                            consent_object["participant_name"] = (
                                contract.signer[0].signature[0].onBehalfOfReference.display
                            )
                            consent_object["signer_signature"] = base64.b64decode(
                                contract.signer[0].signature[0].blob
                            ).decode()

                        elif q_response.questionnaire.reference == "Questionnaire/guardian-signature-part-2":

                            # This is the question about being able to get
                            # acknowledgement from the participant by the
                            # guardian/parent.
                            consent_object["participant_acknowledgement"] = next(
                                item.answer[0].valueString for item in q_response.item if item.linkId == "question-1"
                            ).title()

                            # If the answer to the question is no, grab the reason.
                            if consent_object["participant_acknowledgement"].lower() == "no":
                                consent_object["participant_acknowledgement_reason"] = next(
                                    item.answer[0].valueString
                                    for item in q_response.item
                                    if item.linkId == "question-1-1"
                                )

                            # This is the Guardian's signature letting us know they
                            # tried to explain this study.
                            consent_object["explained_signature"] = base64.b64decode(
                                contract.signer[0].signature[0].blob
                            ).decode()

                        elif q_response.questionnaire.reference == "Questionnaire/guardian-signature-part-3":

                            # A contract without a reference is the assent page.
                            consent_object["assent_signature"] = base64.b64decode(
                                contract.signer[0].signature[0].blob
                            ).decode()
                            consent_object["assent_date"] = contract.issued.origval

                            # Append the Questionnaire Text if the response is true.
                            for current_response in q_response.item:

                                if current_response.answer[0].valueBoolean:
                                    answer = [
                                        item for item in questionnaire.item if item.linkId == current_response.linkId
                                    ][0]
                                    assent_exceptions.append(FHIR._exception_description(answer.text))

                        # The default is a standard signature Questionnaire. Used for
                        # ASD-I, NEER, and Example studies
                        else:

                            # This is a person consenting for themselves.
                            consent_object["type"] = "INDIVIDUAL"
                            consent_object["signer_signature"] = base64.b64decode(
                                contract.signer[0].signature[0].blob
                            ).decode()
                            consent_object["participant_name"] = contract.signer[0].signature[0].whoReference.display

                            # These don't apply on an Individual consent.
                            consent_object["participant_acknowledgement_reason"] = "N/A"
                            consent_object["participant_acknowledgement"] = "N/A"
                            consent_object["signer_name"] = "N/A"
                            consent_object["signer_relationship"] = "N/A"
                            consent_object["assent_signature"] = "N/A"
                            consent_object["assent_date"] = "N/A"
                            consent_object["explained_signature"] = "N/A"

                        # Prepare to parse the questionnaire.
                        questionnaire_object = {
                            "template": "dashboard/{}.html".format(questionnaire.id),  # TODO: Remove this after PPM-603
                            "questionnaire": questionnaire.id,
                            "questions": [],
                        }

                        for item in questionnaire.item:

                            question_object = {
                                "type": item.type,
                            }

                            if item.type == "display":
                                question_object["text"] = item.text

                            elif item.type == "boolean" or item.type == "question":
                                # Get the answer.
                                for response in q_response.item:
                                    if response.linkId == item.linkId:
                                        # Process the question, answer and response.
                                        if item.type == "boolean":
                                            question_object["text"] = item.text
                                            question_object["answer"] = response.answer[0].valueBoolean

                                        elif item.type == "question":
                                            question_object["yes"] = item.text
                                            question_object["no"] = (
                                                "I was not able to explain this study "
                                                "to my child or individual in my care "
                                                "who will be participating"
                                            )
                                            question_object["answer"] = response.answer[0].valueString.lower() == "yes"

                            # Add it.
                            questionnaire_object["questions"].append(question_object)

                        # Check the type.
                        if q_response.questionnaire.reference == "Questionnaire/guardian-signature-part-3":
                            consent_object["assent_questionnaires"].append(questionnaire_object)
                        else:
                            consent_object["consent_questionnaires"].append(questionnaire_object)

                        # Link back to participant
                        consent_object["ppm_id"] = FHIR._get_referenced_id(q_response.as_json(), "Patient")

        consent_object["exceptions"] = consent_exceptions
        consent_object["assent_exceptions"] = assent_exceptions

        return consent_object

    @staticmethod
    def _exception_description(display):

        # Check the various exception display values
        if "equipment monitoring" in display.lower() or "fitbit" in display.lower():
            return mark_safe('<span class="label label-danger">Fitbit monitoring</span>')

        elif "referral to clinical trial" in display.lower():
            return mark_safe('<span class="label label-danger">Future contact/questionnaires</span>')

        elif "saliva" in display.lower():
            return mark_safe('<span class="label label-danger">Saliva sample</span>')

        elif "blood sample" in display.lower():
            return mark_safe('<span class="label label-danger">Blood sample</span>')

        elif "stool sample" in display.lower():
            return mark_safe('<span class="label label-danger">Stool sample</span>')

        elif "tumor" in display.lower():
            return mark_safe('<span class="label label-danger">Tumor tissue samples</span>')

        else:
            logger.warning("Could not format exception: {}".format(display))
            return display

    @staticmethod
    def flatten_list(bundle, resource_type):

        # Check the bundle type
        if type(bundle) is dict:
            bundle = Bundle(bundle)

        resource = FHIR._get_list(bundle, resource_type)
        if not resource:
            logger.debug("No List for resource {} found".format(resource_type))
            return None

        # Get the references
        references = [entry.item.reference for entry in resource.entry if entry.item.reference]

        # Find it in the bundle
        resources = [
            entry.resource for entry in bundle.entry if "{}/{}".format(resource_type, entry.resource.id) in references
        ]

        # Flatten them according to type
        if resource_type == "Organization":

            return [organization.name for organization in resources]

        elif resource_type == "ResearchStudy":

            return [study.title for study in resources]

        else:
            logger.error("Unhandled list resource type: {}".format(resource_type))
            return None

    @staticmethod
    def flatten_document_references(bundle):

        return [FHIR.flatten_document_reference(r) for r in FHIR._find_resources(bundle, "DocumentReference")]

    @staticmethod
    def flatten_document_reference(resource):

        # Get the actual resource in case we were handed a BundleEntry
        resource = FHIR._get_or(resource, ["resource"], resource)

        # Pick out properties and build a dict
        reference = dict({"id": FHIR._get_or(resource, ["id"])})

        # Get dates
        reference["timestamp"] = FHIR._get_or(resource, ["indexed"])
        if reference.get("timestamp"):
            reference["date"] = FHIR._format_date(reference["timestamp"], "%m/%d/%Y")

        # Get data provider
        reference["code"] = FHIR._get_or(resource, ["type", "coding", 0, "code"])
        reference["display"] = FHIR._get_or(resource, ["type", "coding", 0, "display"])

        # Get data properties
        reference["title"] = FHIR._get_or(resource, ["content", 0, "attachment", "title"])
        reference["size"] = FHIR._get_or(resource, ["content", 0, "attachment", "size"])
        reference["hash"] = FHIR._get_or(resource, ["content", 0, "attachment", "hash"])
        reference["url"] = FHIR._get_or(resource, ["content", 0, "attachment", "url"])

        # Flatten the list of identifiers into a key value dictionary
        if resource.get("identifier"):
            for identifier in resource.get("identifier", []):
                if identifier.get("system") and identifier.get("value"):
                    reference[identifier.get("system")] = identifier.get("value")

        # Get person
        reference["patient"] = FHIR._get_or(resource, ["subject", "reference"])
        if reference.get("patient"):
            reference["ppm_id"] = reference["fhir_id"] = FHIR._get_referenced_id(resource, "Patient")

        # Check for data
        reference["data"] = FHIR._get_or(resource, ["content", 0, "attachment", "data"])

        return reference

    @staticmethod
    def flatten_communication(resource):

        # Get the actual resource in case we were handed a BundleEntry
        resource = FHIR._get_or(resource, ["resource"], resource)

        # Build it out
        record = dict()

        # Get identifier
        record["identifier"] = FHIR._get_or(resource, ["identifier", 0, "value"])
        record["sent"] = FHIR._get_or(resource, ["sent"])
        record["payload"] = FHIR._get_or(resource, ["payload", 0, "contentString"])

        # Get the recipient
        record["ppm_id"] = FHIR._get_referenced_id(resource, "Patient")

        return record

    @staticmethod
    def questionnaire_answers(bundle_dict, questionnaire_id):
        """
        Returns a list of the correct answer values for the given questionnaire quiz.
        This is pretty hardcoded so not that useful for anything but ASD consent
        quizzes.
        :param bundle_dict: A bundle resource from FHIR containing the Questionnaire
        :type bundle_dict: dict
        :param questionnaire_id: The FHIR ID of the Questionnaire to handle
        :type questionnaire_id: str
        :return: List of correct answer values
        :rtype: [str]
        """

        # Build the bundle
        bundle = Bundle(bundle_dict)

        # Pick out the questionnaire and its response
        questionnaire = next(
            (entry.resource for entry in bundle.entry if entry.resource.id == questionnaire_id),
            None,
        )

        # Ensure resources exist
        if not questionnaire:
            logger.debug("Missing Questionnaire: {}".format(questionnaire_id))
            return []

        # Return the correct answers
        answers = []

        # Check which questionnaire
        if questionnaire_id == "ppm-asd-consent-individual-quiz":

            answers = [
                questionnaire.item[0].option[0].valueString,
                questionnaire.item[1].option[0].valueString,
                questionnaire.item[2].option[1].valueString,
                questionnaire.item[3].option[3].valueString,
            ]

        elif questionnaire_id == "ppm-asd-consent-guardian-quiz":

            answers = [
                questionnaire.item[0].option[0].valueString,
                questionnaire.item[1].option[0].valueString,
                questionnaire.item[2].option[1].valueString,
                questionnaire.item[3].option[3].valueString,
            ]

        return answers

    class Resources:
        @staticmethod
        def enrollment_flag(patient_ref, status="proposed", start=None, end=None):

            data = {
                "resourceType": "Flag",
                "meta": {"lastUpdated": datetime.now().isoformat()},
                "status": "active" if status == "accepted" else "inactive",
                "category": {
                    "coding": [
                        {
                            "system": "http://hl7.org/fhir/flag-category",
                            "code": "admin",
                            "display": "Admin",
                        }
                    ],
                    "text": "Admin",
                },
                "code": {
                    "coding": [
                        {
                            "system": "https://peoplepoweredmedicine.org/" "enrollment-status",
                            "code": status,
                            "display": status.title(),
                        }
                    ],
                    "text": status.title(),
                },
                "subject": {"reference": patient_ref},
            }

            # Set dates if specified.
            if start:
                data["period"] = {"start": start.isoformat()}
                if end:
                    data["period"]["end"] = end.isoformat()

            return data

        @staticmethod
        def research_study(title):

            data = {
                "resourceType": "ResearchStudy",
                "title": title,
            }

            return data

        @staticmethod
        def research_subject(patient_ref, research_study_ref):

            data = {
                "resourceType": "ResearchSubject",
                "study": {"reference": research_study_ref},
                "individual": {"reference": patient_ref},
            }

            return data

        @staticmethod
        def ppm_research_study(project, title):

            data = {
                "resourceType": "ResearchStudy",
                "id": project,
                "identifier": [
                    {
                        "system": FHIR.research_study_identifier_system,
                        "value": f"ppm-{project}",
                    }
                ],
                "status": "in-progress",
                "title": "People-Powered Medicine - {}".format(title),
            }

            # Hard code dates
            if "neer" in project:
                data["period"] = {"start": "2018-05-01T00:00:00Z"}

            elif "autism" in project:
                data["period"] = {"start": "2017-07-01T00:00:00Z"}

            return data

        @staticmethod
        def ppm_research_subject(project, patient_ref, status="candidate", consent=None):

            data = {
                "resourceType": "ResearchSubject",
                "identifier": {
                    "system": FHIR.research_subject_identifier_system,
                    "value": "ppm-{}".format(project),
                },
                "period": {"start": datetime.now().isoformat()},
                "status": status,
                "study": {"reference": "ResearchStudy/ppm-{}".format(project)},
                "individual": {"reference": patient_ref},
            }

            # Hard code dates
            if consent:
                data["consent"] = {"reference": "Consent/{}".format(consent)}

            return data

        @staticmethod
        def ppm_device(
            item,
            patient_ref,
            identifier=None,
            shipped=None,
            returned=None,
            status="active",
        ):

            data = {
                "resourceType": "Device",
                "type": {
                    "coding": [
                        {
                            "system": FHIR.device_coding_system,
                            "code": item,
                            "display": dict(PPM.TrackedItem.choices())[item],
                        }
                    ],
                    "text": dict(PPM.TrackedItem.choices())[item],
                },
                "status": status,
                "patient": {"reference": patient_ref},
            }

            # Prefill some details based on the item type
            if item is PPM.TrackedItem.BloodSampleKit:
                pass
            elif item is PPM.TrackedItem.SalivaSampleKit:
                pass
            elif item is PPM.TrackedItem.uBiomeFecalSampleKit:
                pass
            elif item is PPM.TrackedItem.Fitbit:
                pass

            # Add identifier
            if identifier:
                data["identifier"] = [{"system": FHIR.device_identifier_system, "value": identifier}]

            # Check dates
            if shipped:
                data["manufactureDate"] = shipped.isoformat()

            if returned:
                data["expirationDate"] = returned.isoformat()

            return data

        @staticmethod
        def communication(
            patient_ref,
            identifier,
            content=None,
            status="completed",
            sent=datetime.now().isoformat(),
        ):

            data = {
                "resourceType": "Communication",
                "identifier": [
                    {
                        "system": FHIR.ppm_comm_identifier_system,
                        "value": identifier,
                    }
                ],
                "sent": sent,
                "recipient": [{"reference": patient_ref}],
                "status": status,
            }

            # Hard code dates
            if content:
                data["payload"] = [{"contentString": content}]

            return data

        @staticmethod
        def patient(form):

            # Build a FHIR-structured Patient resource.
            patient_data = {
                "resourceType": "Patient",
                "active": True,
                "identifier": [
                    {
                        "system": FHIR.patient_email_identifier_system,
                        "value": form.get("email"),
                    },
                ],
                "name": [
                    {
                        "use": "official",
                        "family": form.get("lastname"),
                        "given": [form.get("firstname")],
                    },
                ],
                "address": [
                    {
                        "line": [
                            form.get("street_address1"),
                            form.get("street_address2"),
                        ],
                        "city": form.get("city"),
                        "postalCode": form.get("zip"),
                        "state": form.get("state"),
                    }
                ],
                "telecom": [
                    {
                        "system": FHIR.patient_phone_telecom_system,
                        "value": form.get("phone"),
                    },
                ],
            }

            if form.get("contact_email"):
                logger.debug("Adding contact email")
                patient_data["telecom"].append(
                    {
                        "system": FHIR.patient_email_telecom_system,
                        "value": form.get("contact_email"),
                    }
                )

            if form.get("how_did_you_hear_about_us"):
                logger.debug('Adding "How did you hear about is"')
                patient_data["extension"] = [
                    {
                        "url": FHIR.referral_extension_url,
                        "valueString": form.get("how_did_you_hear_about_us"),
                    }
                ]

            # Convert the twitter handle to a URL
            if form.get("twitter_handle"):
                logger.debug("Adding Twitter handle")
                patient_data["telecom"].append(
                    {
                        "system": FHIR.patient_twitter_telecom_system,
                        "value": "https://twitter.com/" + form["twitter_handle"],
                    }
                )

            return patient_data

        @staticmethod
        def coding(system, code):
            """
            Returns a coding resource
            """
            return {"coding": [{"system": system, "code": code}]}
