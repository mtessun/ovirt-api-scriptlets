#! /usr/bin/python

from ovirtsdk.api import API
from ovirtsdk.xml import params
import time

VERSION = params.Version(major='3', minor='5')

URL = 'https://rhevm.example.com/ovirt-engine/api'
CA = '/etc/pki/ovirt-engine/ca.pem'
USERNAME = 'admin@internal'
PASSWORD = 'paSSwoRD'

try:
        api = API(url=URL, username=USERNAME, password=PASSWORD, ca_file=CA)
        print "Connected to %s successfully!" % api.get_product_info().name

except Exception as err:
        print "Connection failed: %s" % err

try:
    for cluster in api.clusters.list():
       name = cluster.name
       print ("Found cluster named %s" % name)

except Exception as e:
    print 'Failed to list clusters:\n%s' % str(e)
