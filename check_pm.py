#! /usr/bin/python

from ovirtsdk.api import API
from ovirtsdk.xml import params

VERSION = params.Version(major='3', minor='5')

URL =           'https://rhevm.example.com/ovirt-engine/api'
CA =            '/etc/pki/ovirt-engine/ca.pem'
USERNAME =      'admin@internal'
PASSWORD =      'redhat'

HOST_NAME =     'rhevh1'

try:
        api = API(url=URL, username=USERNAME, password=PASSWORD, ca_file=CA)
        print "Connected to %s successfully!" % api.get_product_info().name

except Exception as err:
        print "Connection failed: %s" % err

try:
	host = api.hosts.get(HOST_NAME)
	pm = host.get_power_management()
	print pm.get_type()

except Exception as err:
        print "Check Powermanagement failed: %s" % err

