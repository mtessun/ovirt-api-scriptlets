#! /usr/bin/python

from ovirtsdk.api import API
from ovirtsdk.xml import params

VERSION = params.Version(major='3', minor='6')

URL = 'https://rhevm.example.com/ovirt-engine/api'
CA = '/etc/pki/ovirt-engine/ca.pem'
USERNAME = 'admin@internal'
PASSWORD = 'paSSwoRD'

AFFINITY_GROUP = 'my-affinity'
VM1            = 'my-vm1'
VM2            = 'my-vm2'
CLUSTER        = 'my-cluster'

try:
        api = API(url=URL, username=USERNAME, password=PASSWORD, ca_file=CA)
        print "Connected to %s successfully!" % api.get_product_info().name

except Exception as err:
        print "Connection failed: %s" % err

try:
    cluster = api.clusters.get(CLUSTER)
    cluster.affinitygroups.add(params.AffinityGroup(name=AFFINITY_GROUP,positive=False,enforcing=True))

except Exception as err:
        print "Add affinitygroup failed: %s" % err

try:
    affinitygroup = api.clusters.get(CLUSTER).affinitygroups.get(AFFINITY_GROUP)
    affinitygroup.vms.add(api.vms.get(VM1))
    affinitygroup.vms.add(api.vms.get(VM2))

except Exception as err:
        print "Add VM to affinitygroup failed: %s" % err

