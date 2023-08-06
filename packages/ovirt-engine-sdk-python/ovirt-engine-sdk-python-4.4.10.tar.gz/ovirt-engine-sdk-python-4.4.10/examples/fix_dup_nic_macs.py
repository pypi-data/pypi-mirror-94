#!/usr/bin/env python
#
# Copyright 2017 Red Hat, Inc.
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301 USA
#
# Refer to the README and COPYING files for full details of the license
#
# fix_dup_nic_macs.py
# In ovirt-engine-4.1.6 and lower there was a possibility of vms vnics being
# assigned the same mac address. The bug (https://bugzilla.redhat.com/1435485)
# was fixed but nics with duplicate macs may still exist. This script helps
# identifying such vms and vnics and also can fix them in certain situations.
#

import argparse
import contextlib
import getpass
import logging
import sys

from collections import defaultdict

import ovirtsdk4 as sdk
import ovirtsdk4.types as types


class VmEntry(object):
    def __init__(self, vm, nic):
        self.vm_id = vm.id
        self.vm_name = vm.name
        self.vm_status = vm.status
        self.vm_cluster = vm.cluster.id
        self.nic_id = nic.id
        self.nic_name = nic.name
        self.nic_plugged = nic.plugged


def main():
    args = _parse_args()
    _setup_logging()
    log = logging.getLogger()
    connection = sdk.Connection(
        url=args.url,
        username=args.user,
        password=getpass.getpass('Please enter user password: '),
        ca_file=args.ca if args.ca else None,
        insecure=False if args.ca else True,
        debug=args.debug,
        log=log
    )
    vms_service = connection.system_service().vms_service()
    allowed_clusters = _get_allowed_clusters(connection, args.data_center)
    if not allowed_clusters:
        log.error("No clusters found, check data-center argument.")

    with contextlib.closing(connection):
        for loop in range(0, args.loop):
            log.info("Starting iteration %d", loop)
            mac_vms = _find_show_duplicates(vms_service, allowed_clusters)
            if mac_vms and not args.dryrun:
                _fix_duplicates(vms_service, allowed_clusters, mac_vms)


def _setup_logging():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M',
                        filename='macs.log',
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)-8s : %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


def _build_mac_vms(vms_service, allowed_clusters):
    mac_vms = defaultdict(set)
    for vm in vms_service.list():
        if vm.cluster.id not in allowed_clusters:
            continue
        for nic in vms_service.vm_service(vm.id).nics_service().list():
            entry = VmEntry(vm, nic)
            mac_vms[nic.mac.address].add(entry)
    return {mac: vm for mac, vm in mac_vms.iteritems() if len(vm) > 1}


def _can_fix_duplicate(mac, vms, allowed_clusters):
    log = logging.getLogger()
    _CANTFIX_MSG = 'Cannot fix MAC %s automatically,'
    _REASON_PLUG = 'more than 1 VM with NIC plugged is not DOWN'
    CANTFIX_PLUG = '{} {}'.format(_CANTFIX_MSG, _REASON_PLUG)
    if sum(not _down_or_unplugged(vm) for vm in vms) > 1:
        log.warning(CANTFIX_PLUG, mac)
        return False
    return True


def _down_or_unplugged(vm):
    return (vm.vm_status == types.VmStatus.DOWN or not vm.nic_plugged)


def _find_show_duplicates(vms_service, allowed_clusters):
    log = logging.getLogger()
    mac_vms = _build_mac_vms(vms_service, allowed_clusters)
    if not mac_vms:
        log.info("No duplicate MACs found")
    else:
        log.info("Duplicate MACs found:")
        _show_duplicate(mac_vms)
    return mac_vms


def _fix_duplicates(vms_service, allowed_clusters, mac_vms):
    log = logging.getLogger()
    for mac in mac_vms:
        if not _can_fix_duplicate(mac, mac_vms[mac], allowed_clusters):
            continue
        log.info("Fixing duplicate MAC %s automatically:", mac)
        for vm in mac_vms[mac]:
            if _down_or_unplugged(vm):
                log.info("  Refreshing %s %s", vm.vm_name, vm.nic_name)
                _refresh_nic(vms_service, vm)


def _get_allowed_clusters(connection, data_centers):
    dcs_service = connection.system_service().data_centers_service()
    clusters_service = connection.system_service().clusters_service()
    return {c.id for c in clusters_service.list()
            if dcs_service.data_center_service(c.data_center.id).get().name
            in data_centers}


def _parse_args():
    parser = argparse.ArgumentParser(description='Fix duplicate MACs')
    parser.add_argument('--url', type=str, required=True,
                        help='API URL (https://example/ovirt-engine/api)')
    parser.add_argument('--dry-run', dest='dryrun', action='store_true',
                        help='Do not attempt to fix, just test')
    parser.add_argument('--debug', dest='debug', action='store_true',
                        help='Log all API interaction')
    parser.add_argument('--loop', type=int, default=1,
                        help='LOOP find and fix iterations')
    parser.add_argument('--data-center', type=str, default="Default",
                        help='DATA-CENTER(s) to run (Default)', nargs='+')
    parser.add_argument('--user', type=str, default="admin@internal",
                        help='USER to login to RHV-M, (admin@internal)')
    parser.add_argument('--ca', type=str, default="",
                        help='PATH to the RHV HTTP CA Certificate (insecure)')
    return parser.parse_args()


def _refresh_nic(vms_service, vm):
    nics_service = vms_service.vm_service(vm.vm_id).nics_service()
    nic = nics_service.nic_service(vm.nic_id).get()
    nics_service.nic_service(nic.id).remove()
    nics_service.add(
        types.Nic(
            name=nic.name,
            description=nic.description,
            vnic_profile=nic.vnic_profile
        ),
    )


def _show_duplicate(mac_vms):
    log = logging.getLogger()
    for mac in mac_vms:
        log.info("MAC %s is in use by following VMs", mac)
        for vm in mac_vms[mac]:
            log.info("  VM %s is %s, nic %s is %s", vm.vm_name, vm.vm_status,
                     vm.nic_name, "plugged" if vm.nic_plugged else "unplugged")


if __name__ == '__main__':
    sys.exit(main() or 0)
