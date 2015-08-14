#! /usr/bin/python

from ovirtsdk.api import API
from ovirtsdk.xml import params
import time

VERSION = params.Version(major='3', minor='5')

URL = 'https://rhevm.example.com/ovirt-engine/api'
CA = '/etc/pki/ovirt-engine/ca.pem'
USERNAME = 'admin@internal'
PASSWORD = 'paSSwoRD'

DC_NAME = 'Default'
CLUSTER_NAME = 'Default'
HOST_NAME = 'rhevh1'
#
HOST_NAME = 'rhevh1'
HOST_ADDRESS = '192.168.100.11'
ROOT_PASSWORD = 'superSecret'
#
PM_ADDRESS = '192.168.101.11'

try:
        api = API(url=URL, username=USERNAME, password=PASSWORD, ca_file=CA)
        print "Connected to %s successfully!" % api.get_product_info().name

except Exception as err:
        print "Connection failed: %s" % err

try:
    pm = params.PowerManagement()
    pm.set_type('xvm')
    # Note: Fencing type xvm is for nested HV
    # Note: And this needs to be added to RHEV first
    pm.set_enabled(True)
    pm.set_address(PM_ADDRESS)
    pm.set_username('root')
    pm.set_password('Secret')
    pm.set_options(params.Option(name='Domain', value='rhev-h-3'))
    pm.set_kdump_detection(True)

    if api.hosts.add(params.Host(name=HOST_NAME,
                     address=HOST_ADDRESS,
                     cluster=api.clusters.get(CLUSTER_NAME),
                     root_password=ROOT_PASSWORD,
                     power_management=pm)):
        print 'Host was added successfully'
        print 'Waiting for host to install and reach the Up status'
        while api.hosts.get(HOST_NAME).status.state != 'up':
            time.sleep(1)
        print "Host is up"
    if api.hosts.get(HOST_NAME).deactivate():
        print 'Setting Host to maintenance'
        print 'Waiting for host to reach maintenance status'
        while api.hosts.get(HOST_NAME).status.state != 'maintenance':
            time.sleep(1)
        print 'Host is in maintenance mode'

except Exception as e:
    print 'Failed to install Host:\n%s' % str(e)
