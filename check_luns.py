#! /usr/bin/python

from ovirtsdk.api import API
from ovirtsdk.xml import params
import time

VERSION = params.Version(major='3', minor='5')

URL = 'https://rhevm.satellite.local/ovirt-engine/api'
CA = '/etc/pki/ovirt-engine/ca.pem'
USERNAME = 'admin@internal'
PASSWORD = 'paSSwoRD'

DC_NAME = 'Default'
CLUSTER_NAME = 'Default'
#
HOST_NAME = 'rhevh1'
#
KB = 1024
MB = KB * 1024
GB = MB * 1024

try:
        api = API(url=URL, username=USERNAME, password=PASSWORD, ca_file=CA)
        print "Connected to %s successfully!" % api.get_product_info().name

except Exception as err:
        print "Connection failed: %s" % err

try:
    host = api.hosts.get(HOST_NAME)
    for sl in host.storage.list():
        for lun in sl.logical_unit:
            unit_size = int(lun.size)/GB
            print "Found LUN %s with size %s, id %s and status %s" % (lun.id, unit_size, lun.get_disk_id(), lun.status)

except Exception as e:
    print 'Failed to install Host:\n%s' % str(e)
