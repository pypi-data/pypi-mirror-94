import getpass
import xml
import sys
import logging
import json
import collections
from enum import Enum
import tabulate
import argparse
import os

import xmltodict
import pan.xapi

from .versions import APP_NAME, APP_BUILD, APP_VERSION
from .default_data import *

# default log handler
logger = logging.getLogger(__name__)

__license__ = """
    MIT License
    
    Copyright (c) 2020 Aaron Edwards
    
    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:
    
    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.
    
    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
"""

# Try getting AUTH_TOKEN
PANORAMA_HOST = os.environ.get("PANORAMA_HOST")
PANORAMA_USER = os.environ.get("PANORAMA_USER")
PANORAMA_PASS = os.environ.get("PANORAMA_PASS")

# Try getting Prisma API key from env var
PANORAMA_API_KEY = os.environ.get("PANORAMA_API_KEY")


# add a version from the build data.
__version__ = "{0}-{1}".format(APP_VERSION, APP_BUILD)

# Prisma Edge to Compute Map
PRISMA_EDGE_COMPUTE_MAP = {
    'canada-central': "canada-central",
    'ca-central-1': "canada-central",
    'canada-west': "us-northwest",
    'us-west-2': "us-northwest",
    'costa-rica': "us-southeast",
    'mexico-central': "us-southeast",
    'panama': "us-southeast",
    'us-southeast': "us-southeast",
    'columbia': "us-southeast",
    'mexico-west': "us-southwest",
    'us-west-201': "us-southwest",
    'us-west-1': "us-southwest",
    'us-east-2': "us-central",
    'us-south': "us-central",
    'us-east-1': "us-east",
    'us-northeast': "us-east",
    'argentina': "south-america-east",
    'bolivia': "south-america-east",
    'brazil-central': "south-america-east",
    'brazil-east': "south-america-east",
    'sa-east-1': "south-america-east",
    'chile': "south-america-east",
    'ecuador': "south-america-east",
    'paraguay': "south-america-east",
    'peru': "south-america-east",
    'venezuela': "south-america-east",
    'andorra': "europe-central",
    'austria': "europe-central",
    'bulgaria': "europe-central",
    'croatia': "europe-central",
    'czech-republic': "europe-central",
    'eu-central-1': "europe-central",
    'germany-north': "europe-central",
    'germany-south': "europe-central",
    'greece': "europe-central",
    'hungary': "europe-central",
    'italy': "europe-central",
    'liechtenstein': "europe-central",
    'luxembourg': "europe-central",
    'moldova': "europe-central",
    'monaco': "europe-central",
    'poland': "europe-central",
    'portugal': "europe-central",
    'romania': "europe-central",
    'slovakia': "europe-central",
    'slovenia': "europe-central",
    'spain-central': "europe-central",
    'spain-east': "europe-central",
    'ukraine': "europe-central",
    'uzbekistan': "europe-central",
    'egypt': "europe-central",
    'israel': "europe-central",
    'jordan': "europe-central",
    'kuwait': "europe-central",
    'saudi-arabia': "europe-central",
    'turkey': "europe-central",
    'uae': "europe-central",
    'kenya': "europe-central",
    'nigeria': "europe-central",
    'south-africa-central': "europe-central",
    'belarus': "europe-north",
    'finland': "europe-north",
    'lithuania': "europe-north",
    'norway': "europe-north",
    'russia-central': "europe-north",
    'russia-northwest': "europe-north",
    'sweden': "europe-north",
    'belgium': "belgium",
    'denmark': "europe-west",
    'netherlands-central': "europe-west",
    'netherlands-south': "europe-west",
    'eu-west-3': "france-north",
    'france-south': "europe-northwest",
    'eu-west-2': "europe-northwest",
    'eu-west-1': "ireland",
    'switzerland': "switzerland",
    'me-south-1': "bahrain",
    'south-africa-west': "south-africa-west",
    'bangladesh': "asia-south",
    'india-north': "asia-south",
    'india-south': "asia-south",
    'ap-south-1': "asia-south",
    'pakistan-south': "asia-south",
    'pakistan-west': "asia-south",
    'cambodia': "asia-southeast",
    'indonesia': "asia-southeast",
    'malaysia': "asia-southeast",
    'myanmar': "asia-southeast",
    'philippines': "asia-southeast",
    'ap-southeast-1': "asia-southeast",
    'thailand': "asia-southeast",
    'vietnam': "asia-southeast",
    'hong-kong': "hong-kong",
    'papua-new-guinea': "australia-southeast",
    'australia-east': "australia-southeast",
    'australia-south': "australia-southeast",
    'ap-southeast-2': "australia-southeast",
    'new-zealand': "australia-southeast",
    'ap-northeast-2': "south-korea",
    'taiwan': "taiwan",
    'ap-northeast-1': "asia-northeast",
    'japan-south': "japan-south",
}

PRISMA_REGIONS = [
    "canada-central",
    "ca-central-1",
    "canada-west",
    "costa-rica",
    "mexico-central",
    "mexico-west",
    "panama",
    "us-east-2",
    "us-east-1",
    "us-northeast",
    "us-west-2",
    "us-south",
    "us-southeast",
    "us-west-201",
    "us-west-1",
    "argentina",
    "bolivia",
    "brazil-central",
    "brazil-east",
    "sa-east-1",
    "chile",
    "columbia",
    "ecuador",
    "paraguay",
    "peru",
    "venezuela",
    "andorra",
    "austria",
    "belarus",
    "belgium",
    "bulgaria",
    "croatia",
    "czech-republic",
    "denmark",
    "finland",
    "eu-west-3",
    "france-south",
    "eu-central-1",
    "germany-north",
    "germany-south",
    "greece",
    "hungary",
    "eu-west-1",
    "italy",
    "liechtenstein",
    "lithuania",
    "luxembourg",
    "moldova",
    "monaco",
    "netherlands-central",
    "netherlands-south",
    "norway",
    "poland",
    "portugal",
    "romania",
    "russia-central",
    "russia-northwest",
    "slovakia",
    "slovenia",
    "spain-central",
    "spain-east",
    "sweden",
    "switzerland",
    "eu-west-2",
    "ukraine",
    "uzbekistan",
    "me-south-1",
    "egypt",
    "israel",
    "jordan",
    "kuwait",
    "saudi-arabia",
    "turkey",
    "uae",
    "kenya",
    "nigeria",
    "south-africa-central",
    "south-africa-west",
    "bangladesh",
    "cambodia",
    "hong-kong",
    "india-north",
    "india-south",
    "ap-south-1",
    "indonesia",
    "malaysia",
    "myanmar",
    "pakistan-south",
    "pakistan-west",
    "papua-new-guinea",
    "philippines",
    "ap-southeast-1",
    "ap-northeast-2",
    "taiwan",
    "thailand",
    "vietnam",
    "ap-northeast-1",
    "japan-south",
    "australia-east",
    "australia-south",
    "ap-southeast-2",
    "new-zealand"
]


class PanoramaOperations(object):
    """
    Object to interact with Panorama.
    Leverages pan-python, but this object does XML -> Dict/JSON mapping to make it more python-native.
    """
    xapi = None

    log_level = 0

    # Root device name
    root_device = 'localhost.localdomain'

    def __init__(self, *args, **kwargs):
        """
        When creating the object, use pan-python's XAPI object, and pass through everything by default.
        """
        # set pan.xapi
        self.xapi = pan.xapi.PanXapi(*args, **kwargs)

        # set exception for later catch
        self.PanXapiError = pan.xapi.PanXapiError

        # Bind API method classes to this object
        subclasses = self._subclass_container()
        self.show = subclasses["show"]()
        self.list = subclasses["list"]()
        self.op = subclasses["op"]()

        return

    def set_debug(self, log_level=None):
        """
        Enable/disable printing of debug messages.
        :param log_level: Int (0-3)
        :return: No Return.
        """

        if log_level is not None:
            self.log_level = log_level

        if isinstance(self.log_level, int) and self.log_level > 0:

            if self.log_level >= 3:
                logger.setLevel(logging.DEBUG - 2)
            elif self.log_level == 2:
                logger.setLevel(logging.DEBUG - 1)
            elif self.log_level == 1:
                logger.setLevel(logging.DEBUG)

            log_format = '%(message)s'
            handler = logging.StreamHandler()
            formatter = logging.Formatter(log_format)
            handler.setFormatter(formatter)
            logger.addHandler(handler)

        else:
            # Remove all handlers
            for handler in logging.root.handlers[:]:
                logging.root.removeHandler(handler)
            for handler in logger.handlers[:]:
                logger.removeHandler(handler)
            # set logging level to default
            logger.setLevel(logging.WARNING)

        return

    def _subclass_container(self):
        # For binding broken out Classes to this object, while allowing parent references.
        _parent_class = self

        class ShowWrapper(_PRISMAShow):

            def __init__(self):
                self._parent_class = _parent_class

        class ListWrapper(_PRISMAList):

            def __init__(self):
                self._parent_class = _parent_class

        class OpWrapper(_PRISMAOp):

            def __init__(self):
                self._parent_class = _parent_class

        return {"show": ShowWrapper,
                "list": ListWrapper,
                "op": OpWrapper}

    def update_regions(self, tenant=None):
        """
        Update global regions from Panorama
        :return: Status text, mutates globals in place.
        """
        global PRISMA_REGIONS

        original_count = len(PRISMA_REGIONS)
        final_count = 0

        # pull regions
        try:
            regions_resp = self.op.get_region_list(tenant=tenant)
        except self.PanXapiError:
            return_msg = "PANW: Unable to update Prisma Regions from Panorama."
            return return_msg

        # check response #1
        if not isinstance(regions_resp.response, dict):
            return_msg = "PANW: Unable to parse Prisma Regions from Panorama. Got {0}." \
                         "".format(regions_resp.response)
            return return_msg

        # check response #2
        regions_result = regions_resp.response.get('result', {})
        if not isinstance(regions_result, dict):
            return_msg = "PANW: Unable to parse Prisma Regions from Panorama. Got {0}." \
                         "".format(regions_resp.response)
            return return_msg

        # check response #3
        regions_msg = regions_result.get('msg', [])
        if not regions_msg or not isinstance(regions_msg, list):
            return_msg = "PANW: Unable to parse Prisma Regions from Panorama. Got {0}." \
                         "".format(regions_resp.response)
            return return_msg

        # ok, set global.
        PRISMA_REGIONS = regions_msg
        final_count = len(regions_msg)

        return "PANW: Parsed {0} Regions (previously {1})".format(final_count, original_count)

    def verify_tenant_name(self, tenant):
        """
        Verify the entered tenant name. If it does not exist, exit loop.
        tenant: tenant name
        :return: bool (True if exists, false if not), return Message.
        """
        return_msg = "PANW: Verified Tenant {0} exists.".format(tenant)

        if not isinstance(tenant, str):
            return_msg = "PANW: Passed tenant value was not str: got {0}".format(repr(tenant))
            return False, return_msg

        # Check tenant!
        resp = self.list.tenants()

        # check response #1
        if not isinstance(resp.list, list):
            return_msg = "PANW: Unable to query Multi-Tenant Tenants: {0}".format(resp.response)
            return False, return_msg

        if tenant not in resp.list:
            return_msg = 'PANW: Tenant {0} not configured. Configured tenants: {1}'.format(tenant,
                                                                                           ', '.join(resp.list))
            return False, return_msg
        else:
            # tenant name verified
            return True, return_msg

    def is_multi_tenant_enabled(self):
        """
        Verify multi tenant is enabled, or not.
        :return: tuple of (Bool, message) - bool is True if enabled, False if not or error.
        """
        resp = self.show.multi_tenant_enable()
        if isinstance(resp.response, (dict, collections.OrderedDict)):
            status = resp.response.get('multi-tenant-enable')
            if isinstance(status, str):
                if status.lower() in ['yes', 'true']:
                    return True, 'PANW: Got Multi-Tenant is enabled. (Status: {0})'.format(status)
                else:
                    # return False if something else. may be wrong here.
                    return False, 'PANW: Got Multi-Tenant is disabled. (Status: {0})'.format(status)
            elif status is True:
                return True, 'PANW: Got Multi-Tenant is disabled. (Status: {0})'.format(status)
            else:
                # got here, something is wrong - return False for now and put status in message.
                return False, 'PANW: Got bad Multi-Tenant status, setting disabled. (Status Detail: {0})' \
                              ''.format(repr(status))

    @staticmethod
    def list_of_matching_names(prisma_api_response, subkey=None, name_header=None, listkey="entry",
                               entrykey="@name", hard_debug=False):
        """
        Given a PanoramaAPIResponse, return a list of names, with optional name header parsing.
        :param prisma_api_response: PanoramaAPIResponse object from a LIST operation.
        :param subkey: Subkey text of the key the list is under
        :param listkey: List containing key. Default "entry"
        :param name_header: if str, use that name header, else no name header.
        :param entrykey: String to return list of objects in item. if None, just return whole item. Default "@name".
        :param hard_debug: Bool, if True raw print debugging to STDERR
        :return:
        """
        if subkey:
            basedict = prisma_api_response.attr_response.get(subkey, {})
        else:
            basedict = prisma_api_response.attr_response

        if isinstance(name_header, str):
            name_header_string = name_header
            use_name_header = True
        else:
            name_header_string = ""
            use_name_header = False

        if basedict is None:
            entry_list = []
        else:
            entry_list = basedict.get(listkey, [])

        if isinstance(entry_list, (dict, collections.OrderedDict, str)):
            # PANORAMA API JSON-IFICATION returns a dict for single entry instead of a list. Catch and fix that.
            # also return list if string.
            temp_dict = entry_list
            entry_list = [temp_dict]

        if hard_debug:
            sys.stderr.write(f"TYPE: {type(entry_list)}\n")
            sys.stderr.write(f"BASE: {json.dumps(entry_list)}\n")
            sys.stderr.write(f"USE_NAME_HEADER: {use_name_header}\n")
            sys.stderr.write(f"NAME_HEADER: {name_header_string}\n")

        # build new list of names that start with the AUTO CGX name header.
        if use_name_header:
            # if use name header is True, entrykey must be set. Default to @name if it is none here.
            if entrykey is None:
                entrykey = "@name"
            return_val = [entry.get(entrykey) for entry in entry_list if isinstance(entry, dict) and
                          entry.get(entrykey) and entry.get(entrykey, "").startswith(name_header_string)]
            if hard_debug:
                sys.stderr.write(f"RETURN: {return_val}\n")
            return return_val
        elif entrykey is None:
            # just return a list of all objects
            if hard_debug:
                sys.stderr.write("RETURN: " + str(entry_list) + "\n")
            return entry_list
        else:
            # return all entrykey objects unfiltered.
            return_val = [entry.get(entrykey) for entry in entry_list if isinstance(entry, dict) and
                          entry.get(entrykey)]
            if hard_debug:
                sys.stderr.write(f"RETURN: {return_val}\n")
            return return_val


class _PRISMAShow(object):
    """
    Show = Running config(applied).
    """

    # placeholder for parent class namespace
    _parent_class = None

    def tenants(self, name=None):

        # Get tenant full config for cloud_services

        xpath = PRISMA_TENANTS_XPATH.format(self._parent_class.root_device,
                                            name)

        # get
        logger.debug("XPATH: %s", xpath)

        self._parent_class.xapi.show(xpath=xpath)

        logger.debug("XAPI:\n===>\n%s\n<===", self._parent_class.xapi)

        return PanoramaAPIResponse(self._parent_class.xapi, xpath, name)

    def cloud_services(self):

        # Full Cloud Services Show

        # xpath
        xpath = PRISMA_CLOUD_SERVICES_XPATH.format(self._parent_class.root_device)

        # get
        logger.debug("XPATH: %s", xpath)

        self._parent_class.xapi.show(xpath=xpath)

        logger.debug("XAPI:\n===>\n%s\n<===", self._parent_class.xapi)

        # temp_resp = PanoramaAPIResponse(self._parent_class.xapi, xpath, None)
        # temp_resp.list = self._parent_class.list_of_matching_names(temp_resp, "templates", name_header=False,
        #                                                            listkey="member", entrykey=None)
        return PanoramaAPIResponse(self._parent_class.xapi, xpath, None)

    def multi_tenant_enable(self):

        # Full Cloud Services Show

        # xpath
        xpath = PRISMA_MULTI_TENANT_ENABLE_XPATH.format(self._parent_class.root_device)

        # get
        logger.debug("XPATH: %s", xpath)

        self._parent_class.xapi.show(xpath=xpath)

        logger.debug("XAPI:\n===>\n%s\n<===", self._parent_class.xapi)

        # temp_resp = PanoramaAPIResponse(self._parent_class.xapi, xpath, None)
        # temp_resp.list = self._parent_class.list_of_matching_names(temp_resp, "templates", name_header=False,
        #                                                            listkey="member", entrykey=None)
        return PanoramaAPIResponse(self._parent_class.xapi, xpath, None)

    def prisma_remotenetworks_aggr_bw(self, tenant=None):

        # Get aggregate bandwidth config used by remote network config

        # xpath
        if tenant is not None:
            xpath = PRISMA_REMOTENETWORKS_AGGR_BW_MULTI_TENANT_XPATH_LIST.format(self._parent_class.root_device,
                                                                                 tenant)
        else:
            xpath = PRISMA_REMOTENETWORKS_AGGR_BW_XPATH_LIST.format(self._parent_class.root_device)

        # get
        logger.debug("XPATH: %s", xpath)

        self._parent_class.xapi.show(xpath=xpath)

        logger.debug("XAPI:\n===>\n%s\n<===", self._parent_class.xapi)

        return PanoramaAPIResponse(self._parent_class.xapi, xpath, None)


class _PRISMAList(object):
    """
    List = Show all objects on Running config(applied).
    """

    # placeholder for parent class namespace
    _parent_class = None

    def tenants(self, name=None):
        # Get tenant full config for cloud_services

        xpath = PRISMA_TENANTS_XPATH_LIST.format(self._parent_class.root_device,
                                                 name)

        # get
        logger.debug("XPATH: %s", xpath)

        self._parent_class.xapi.show(xpath=xpath)

        logger.debug("XAPI:\n===>\n%s\n<===", self._parent_class.xapi)

        temp_resp = PanoramaAPIResponse(self._parent_class.xapi, xpath, None)
        temp_resp.list = self._parent_class.list_of_matching_names(temp_resp, "tenants", name_header=False)
        return temp_resp


class _PRISMAOp(object):
    """
    Op = execute OP command to get value.
    """

    # placeholder for parent class namespace
    _parent_class = None

    def get_region_list(self, tenant=None):
        # Get Region list from PAN XAPI

        if tenant is not None:
            op_cmd = "<request><plugins><cloud_services><prisma-access><multi-tenant><get-region-list/>" \
                     "<tenant-name><entry name='{0}'/></tenant-name></multi-tenant>" \
                     "</prisma-access></cloud_services></plugins></request>".format(tenant)
        else:
            # single tenant
            op_cmd = "<request><plugins><cloud_services><prisma-access><get-region-list></get-region-list>" \
                     "</prisma-access></cloud_services></plugins></request>"

        self._parent_class.xapi.op(cmd=op_cmd)

        logger.debug("XAPI:\n===>\n%s\n<===", self._parent_class.xapi)

        resp = PanoramaAPIResponse(self._parent_class.xapi, None, 'get-region-list')
        return resp

    def get_best_region_list(self, lat, long, no_of_entries=1, tenant=None):
        # Get best region/prisma hub location by lat-long

        multi_tenant_start = ""
        multi_tenant_end = ""
        if tenant:
            multi_tenant_start = f"<multi-tenant><tenant-name><entry name='{tenant}'/></tenant-name>"
            multi_tenant_end = "</multi-tenant>"

        op_cmd = f"<request><plugins><cloud_services><prisma-access>" \
                 f"{multi_tenant_start}<get-best-locations-by-latitude-longitude>" \
                 f"<latitude>{lat}</latitude><longitude>{long}</longitude>" \
                 f"<nr-locations>{no_of_entries}</nr-locations>" \
                 f"</get-best-locations-by-latitude-longitude>{multi_tenant_end}" \
                 f"</prisma-access></cloud_services></plugins></request>"

        self._parent_class.xapi.op(cmd=op_cmd)

        logger.debug(f"XAPI:\n===>\nop_cmd: {op_cmd}\n{self._parent_class.xapi}\n<===")

        resp = PanoramaAPIResponse(self._parent_class.xapi, None, 'get_best_region_list')
        return resp

    def get_job_status(self, job_id=None):
        # Get status of job from Panorama XAPI

        op_cmd = "<show><jobs><id>{0}</id></jobs></show>".format(job_id) if job_id else \
            "<show><jobs><all></all></jobs></show>"

        self._parent_class.xapi.op(cmd=op_cmd)

        logger.debug("XAPI:\n===>\n%s\n<===", self._parent_class.xapi)

        resp = PanoramaAPIResponse(self._parent_class.xapi, None, 'get-job-status')
        return resp

    def get_onboarding_status(self, status_type=None, service_type="remote-networks",
                              no_of_entries=10, job_id=None, tenant=None):
        # Get status of on-boarding of all jobs or specific job from Panorama XAPI,
        # Both job_id and status_type can't be null at same time, it will give error

        job_id_str = f"<jobid>{job_id}</jobid>" if job_id else ""

        status_type_str = ""
        if not job_id:
            if status_type:
                no_of_entries_str = ""
                if status_type != OnboardingStatusType.LATEST and no_of_entries:
                    no_of_entries_str = f"<number-of-entries>{no_of_entries}</number-of-entries>"

                status_type_str = f"<{status_type.value}>{no_of_entries_str}</{status_type.value}>"

        multi_tenant_start = ""
        multi_tenant_end = ""
        if tenant:
            multi_tenant_start = f"<multi-tenant><tenant-name><entry name='{tenant}'/></tenant-name>"
            multi_tenant_end = "</multi-tenant>"

        op_cmd = f"<request><plugins><cloud_services><prisma-access>" \
                 f"{multi_tenant_start}<job-status>" \
                 f"<servicetype>{service_type}</servicetype>" \
                 f"{job_id_str}{status_type_str}</job-status>{multi_tenant_end}" \
                 f"</prisma-access></cloud_services></plugins></request>"

        self._parent_class.xapi.op(cmd=op_cmd)

        logger.debug(f"XAPI:\n===>\nop_cmd: {op_cmd}\n{self._parent_class.xapi}\n<===")

        resp = PanoramaAPIResponse(self._parent_class.xapi, None, 'get_onboarding_status')
        return resp

    def get_prisma_api_key_panorama(self, tenant=None):
        # Get the Prisma Access IP API key directly from Panorama.
        if tenant is None:
            op_cmd = "<request><plugins><cloud_services>" \
                     "<prisma-access><addr-list><get-api-key></get-api-key></addr-list></prisma-access>" \
                     "</cloud_services></plugins></request>"
        else:
            op_cmd = "<request><plugins><cloud_services>" \
                     "<prisma-access><multi-tenant><addr-list><get-api-key/></addr-list>" \
                     "<tenant-name><entry name='{0}'/></tenant-name></multi-tenant></prisma-access>" \
                     "</cloud_services></plugins></request>".format(tenant)

        self._parent_class.xapi.op(cmd=op_cmd)

        logger.debug("XAPI:\n===>\n%s\n<===", self._parent_class.xapi)

        resp = PanoramaAPIResponse(self._parent_class.xapi, None, 'get-prisma-api-key-panorama')
        return resp


class PanoramaAPIResponse(dict):
    """
    Object to contain API responses from Panorama. Convert to Dict/JSON as able.
    """

    def __init__(self, xapi_obj, xpath, name, **kwarg):
        dict.__init__(self, kwarg)
        self.__dict__ = self

        self.xpath = xpath
        self.status = xapi_obj.status
        self.status_code = xapi_obj.status_code
        self.status_detail = xapi_obj.status_detail
        self.xml = xapi_obj.xml_result()
        self.name = name
        self.list = []
        if 'list' in kwarg:
            self.list = kwarg.get('list', [])
        if self.xml is None:
            self.response = {}
            self.attr_response = {}
        else:
            try:
                self.response = xmltodict.parse(self.xml, xml_attribs=False)
                self.attr_response = xmltodict.parse(self.xml)
            except xml.parsers.expat.ExpatError:
                self.response = xmltodict.parse("<root>" + self.xml + "</root>", xml_attribs=False)
                self.attr_response = xmltodict.parse("<root>" + self.xml + "</root>")


class OnboardingStatusType(Enum):
    FAILED = "failed-jobs"
    LATEST = "latest"
    PENDING = "pending-jobs"
    SUCCESS = "success-jobs"


class PanoramaError(Exception):
    """
    Custom exception for errors when not exiting.
    """
    pass


def go():
    global PANORAMA_API_KEY
    global PANORAMA_HOST
    global PANORAMA_USER
    global PANORAMA_PASS
    ############################################################################
    # Begin Script, start login / argument handling.
    ############################################################################

    # Parse arguments
    parser = argparse.ArgumentParser(description="{0}.".format(APP_NAME))

    # Allow Controller modification and debug level sets.
    panorama_group = parser.add_argument_group('API', 'These options change how this program connects to the API.')
    panorama_group.add_argument("--host", help="Panorama hostname or IP (or ENV var PANORAMA_HOST). "
                                               "If not entered, will prompt.", type=str, default=None)
    panorama_group.add_argument("--user", help="Panorama username (or ENV var PANORAMA_USERNAME). "
                                               "If not entered, will prompt.", type=str, default=None)
    panorama_group.add_argument("--pass", help="Panorama password (or ENV var PANORAMA_PASSWORD). "
                                               "If not entered, will prompt.", type=str, default=None)

    panorama_group.add_argument("--panorama-api-key", help="Authenticate with Panorama API KEY instead of "
                                                           "username/password.", type=str, default=None)

    panorama_group.add_argument("--tenant", help="Tenant name (if multi-tenancy is enabled.)", type=str, default=None)

    output_group = parser.add_argument_group('Output', 'These options change how the output is generated.')
    output_group.add_argument("--output-json-file", help="Output as JSON to this specified file name",
                              type=str, default=None)

    args = vars(parser.parse_args())

    # set prisma API key if set from args
    local_panorama_api_key = args['panorama_api_key']
    local_panorama_host = args['host']
    local_panorama_user = args['user']
    local_panorama_pass = args['pass']

    local_tenant = args['tenant']

    # if args passed, override env vars
    if local_panorama_api_key:
        PANORAMA_API_KEY = local_panorama_api_key
    if local_panorama_host:
        PANORAMA_HOST = local_panorama_host
    if local_panorama_user:
        PANORAMA_USER = local_panorama_user
    if local_panorama_pass:
        PANORAMA_PASS = local_panorama_pass

    if PANORAMA_HOST is None:
        PANORAMA_HOST = input("Panorama Hostname: ")

    if PANORAMA_API_KEY is not None:
        # API key, use this instead of user/pass.
        panapi = PanoramaOperations(hostname=PANORAMA_HOST, api_key=PANORAMA_API_KEY)

    else:
        if PANORAMA_USER is None:
            PANORAMA_USER = input("Panorama Username: ")
        if PANORAMA_PASS is None:
            PANORAMA_PASS = getpass.getpass("Panorama Password: ")
        panapi = PanoramaOperations(hostname=PANORAMA_HOST, api_username=PANORAMA_USER, api_password=PANORAMA_PASS)

    # check multi tenant on panorama matches
    try:
        verify_multi_tenant, verify_multi_tenant_message = panapi.is_multi_tenant_enabled()
    except panapi.PanXapiError as panapi_exception:
        # check for "No such node"
        panapi_error_nocase = str(panapi_exception).lower()
        if panapi_error_nocase in ["no such node"]:
            # node does not exist. Assume non-multi tenant.
            verify_multi_tenant = False
        else:
            verify_multi_tenant = None
            print("ERROR: Got fatal error verifying Multi-tenant enable/disable status: {0}"
                  "".format(str(panapi_exception)))
            sys.exit(1)

    # if tenant not set and multi-tenant enabled, exit.
    if verify_multi_tenant and local_tenant is None:
        print("ERROR: Tenant not specified but Multi-tenant is enabled. Exiting.")
        sys.exit(1)

    # OK, now lets get the agg bw
    resp = panapi.show.prisma_remotenetworks_aggr_bw()
    aggbw = resp.attr_response.get("agg-bandwidth")
    if not isinstance(aggbw, (dict, collections.OrderedDict)):
        print(f"ERROR: Panorama response not in right format: {aggbw}")
        sys.exit(1)

    aggbw_enabled = aggbw.get("enabled")

    if aggbw_enabled != "yes":
        print(f"ERROR: Prisma Aggregate Bandwidth (1.8+) not enabled: {aggbw_enabled}")
        sys.exit(1)

    entries = aggbw.get("region", {}).get("entry", [])
    # entries may not be list.
    if not isinstance(entries, list):
        entries = [entries]

    results = {}
    for entry in entries:
        entry_name = entry.get("@name")
        members = entry.get("spn-name-list", {}).get("member", [])
        # ensure list encapsulation
        if not isinstance(members, list):
            members = [members]

        # save results
        results[entry_name] = members

    if args['output_json_file'] is None:
        print(tabulate.tabulate(results, headers="keys"))
    else:
        # write json

        with open(args['output_json_file'], 'wt') as jsonfile:
            json.dump(results, jsonfile, indent=4)
    return


if __name__ == "__main__":
    # Get prisma spn
    go()
