#!/usr/bin/python2
 
import os
import sys
import traceback
 
import hooking
 
'''
Syntax:
highperf=1 (value doesn't matter)

The 1GB hugepages must be already defined during boot-time of the
hypervisor, e.g. like
"default_hugepagesz=1GB hugepagesz=1GB hugepages=[# hugepages needed]"

The VM also needs to have iothreads enabled in the RHV-M Web-UI.
The number of threads need to be set to "1"

As invariant tsc is needed, this flag is explicitely passed through to
the guest. Therefore CPU hostpassthrough needs to be enabled in the
RHV-M Web-UI.
'''
 
 
if 'highperf' in os.environ:
    try:
        domxml = hooking.read_domxml()
        domain = domxml.getElementsByTagName('domain')[0]
        if len(domain.getElementsByTagName('memoryBacking')):
            sys.stderr.write('hugepages: VM already have hugepages\n')
            sys.exit(0)
 
        memoryBacking = domxml.createElement('memoryBacking')
        hugepages = domxml.createElement('hugepages')
        page = domxml.createElement('page')
        page.setAttribute('size', '1048576')
        hugepages.appendChild(page)
        memoryBacking.appendChild(hugepages)
        domain.appendChild(memoryBacking)
 
        sys.stderr.write('hugepages: adding hugepages tag\n')

        if len(domain.getElementsByTagName('iothreads')):
            iothreadids = domxml.createElement('iothreadids')
            ids = domxml.createElement('iothread')
            ids.setAttribute('id', '1')
            iothreadids.appendChild(ids)
            domain.appendChild(iothreadids)

            if len(domain.getElementsByTagName('cputune')):
                cputune = domain.getElementsByTagName('cputune')[0]
            else:
                cputune = domxml.createElement('cputune')

            iothreadpin = domxml.createElement('iothreadpin')
            iothreadpin.setAttribute('iothread', '1')
            iothreadpin.setAttribute('cpuset', '0')
            emulatorpin = domxml.createElement('emulatorpin')
            emulatorpin.setAttribute('cpuset', '0')
            cputune.appendChild(iothreadpin)
            cputune.appendChild(emulatorpin)
            if not len(domain.getElementsByTagName('cputune')):
                domain.appendChild(cputune)

        if len(domain.getElementsByTagName('cpu')):
            cpu = domain.getElementsByTagName('cpu')[0]
            feature_tsc = domxml.createElement('feature')
            feature_tsc.setAttribute('policy', 'require')
            feature_tsc.setAttribute('name', 'invtsc')
            feature_rdt = domxml.createElement('feature')
            feature_rdt.setAttribute('policy', 'require')
            feature_rdt.setAttribute('name', 'rdtscp')
            cpu.appendChild(feature_tsc)
            cpu.appendChild(feature_rdt)

        hooking.write_domxml(domxml)
    except Exception:
        sys.stderr.write('highperf hook: [unexpected error]: %s\n' %
                         traceback.format_exc())
        sys.exit(2)
