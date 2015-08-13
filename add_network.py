#! /usr/bin/python

from ovirtsdk.api import API
from ovirtsdk.xml import params

VERSION = params.Version(major='3', minor='5')

URL =           'https://rhevm.example.com/ovirt-engine/api'
CA =            '/etc/pki/ovirt-engine/ca.pem'
USERNAME =      'admin@internal'
PASSWORD =      'paSSwoRD'

HOST_NAME =     'rhevh1'
IP_ADDRESS =	'192.168.100.11'
NETMASK =	'255.255.255.0'
GATEWAY = 	'192.168.100.1'

try:
        api = API(url=URL, username=USERNAME, password=PASSWORD, ca_file=CA)
        print "Connected to %s successfully!" % api.get_product_info().name

except Exception as err:
        print "Connection failed: %s" % err

nic0 = params.HostNIC(network = params.Network(name = 'rhevm'),
	name = 'eth0',
	boot_protocol = 'static',
	ip = params.IP(address = IP_ADDRESS, netmask = NETMASK, gateway = GATEWAY),
	override_configuration = False)
nic1 = params.HostNIC(name = 'eth1', network =  params.Network(), boot_protocol='none',  ip=params.IP(address=None, netmask=None, gateway=None))
nic2 = params.HostNIC(name = 'eth2', network =  params.Network(), boot_protocol='none',  ip=params.IP(address=None, netmask=None, gateway=None))
 
# bond
bond0 = params.Bonding(
   slaves = params.Slaves(host_nic = [ nic1, nic2 ]),
            options = params.Options(
                        option = [
                          params.Option(name = 'miimon', value = '100'),
                          params.Option(name = 'mode', value = '1'),
                          params.Option(name = 'primary', value = 'eth1')
                        ]
                        )
                      )
 
# management network on top of the bond
backendNetwork = params.HostNIC(name = 'bond0',
                      boot_protocol = 'none',
                      override_configuration = True,
                      bonding = bond0)
 
# Now apply the rhevm network configuration
try:
	host = api.hosts.get(HOST_NAME)
	host.nics.setupnetworks(params.Action(force = False, check_connectivity = True, host_nics = params.HostNics(host_nic = [ nic0, backendNetwork ] )))

except Exception as err:
        print "Setup Network failed: %s" % err


# Finally add the labels
try:
	host.nics.get('bond0').labels.add(params.Label(id='Backend'))

except Exception as err:
        print "Add Label failed: %s" % err

# This only works in case a Virtual Network with VLAN ID 110 gets assigned with the Label 'Backend'.
# This Network is not defined in here.

try:
	nic = host.nics.get(name = 'bond0.110')
	nic.set_boot_protocol('static')
	nic.set_ip(params.IP(address = '192.168.101.11', netmask = '255.255.255.0', gateway = None))
	nic.update()

except Exception as err:
        print "Setting IP failed: %s" % err

