#
# License: CloudGenix Public License (v.1)
#

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

PRISMA_REMOTENETWORKS_AGGR_BW_XPATH_LIST = "/config/devices/" \
                                           "entry[@name='{0}']/plugins/cloud_services/remote-networks/agg-bandwidth"

PRISMA_REMOTENETWORKS_AGGR_BW_MULTI_TENANT_XPATH_LIST = "/config/devices/" \
                                                        "entry[@name='{0}']/plugins/cloud_services/multi-tenant/" \
                                                        "tenants/" \
                                                        "entry[@name='{1}']/remote-networks/agg-bandwidth"

PRISMA_CLOUD_SERVICES_XPATH = "/config/devices/" \
                              "entry[@name='{0}']" \
                              "/plugins/cloud_services"

PRISMA_MULTI_TENANT_ENABLE_XPATH = "/config/devices/" \
                                   "entry[@name='{0}']" \
                                   "/plugins/cloud_services/multi-tenant-enable"

# Get multi tenant info
PRISMA_TENANTS_XPATH = "/config/devices/" \
                       "entry[@name='{0}']/plugins" \
                       "/cloud_services/multi-tenant/tenants" \
                       "/entry[@name='{1}']"
PRISMA_TENANTS_XPATH_LIST = "/config/devices/" \
                            "entry[@name='{0}']/plugins" \
                            "/cloud_services/multi-tenant/tenants"
