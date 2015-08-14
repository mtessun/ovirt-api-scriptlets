#! /usr/bin/python

from ovirtsdk.api import API
from ovirtsdk.xml import params

VERSION = params.Version(major='3', minor='5')

URL = 'https://rhevm.example.com/ovirt-engine/api'
CA = '/etc/pki/ovirt-engine/ca.pem'
USERNAME = 'admin@internal'
PASSWORD = 'paSSwoRD'

HOST_NAME = 'rhevh1'

try:
        api = API(url=URL, username=USERNAME, password=PASSWORD, ca_file=CA)
        print "Connected to %s successfully!" % api.get_product_info().name

except Exception as err:
        print "Connection failed: %s" % err

try:
    host = api.hosts.get(HOST_NAME)
    for nic in host.nics.list():
        print nic.name
        nic.labels.add(params.Label(id=nic.name))
    host.nics.get('eth1').labels.add(params.Label(id='Test'))

except Exception as err:
        print "Add Label failed: %s" % err
