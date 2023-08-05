#!/usr/bin/env python3

import os
import sys
import logging
import time
import subprocess
from subprocess import STDOUT
from pathlib import PosixPath

from bthci import HCI
from pyclui import Logger
from bluepy.btle import BTLEException
from bluetooth.btcommon import BluetoothError

from .ui import parse_cmdline
from .helper import find_rfkill_devid, get_microbit_devpaths
from .br_scan import BRScanner
from .le_scan import LEScanner
from .gatt_scan import GATTScanner
from .sdp_scan import SDPScanner
from .stack_scan import StackScanner
from .vuln_scan import VulnScanner


logger = Logger(__name__, logging.INFO)

logger.debug("__name__: {}".format(__name__))


def init_hci(iface='hci0'):
    hci = HCI(iface)

    exitcode, output = subprocess.getstatusoutput(
        'rfkill unblock %d' % find_rfkill_devid(iface))
    if exitcode != 0:
        logger.error('rfkill: ' + output)
        sys.exit(exitcode)

    exitcode, output = subprocess.getstatusoutput(
        "hciconfig up " + iface)
    if exitcode != 0:
        logger.error("Failed to up " + iface)
        sys.exit(exitcode)
    else:
        time.sleep(0.5)

    # hci.reset()
    hci.inquiry_cancel()
    hci.exit_periodic_inquiry_mode()

    hci.write_scan_enable() # No scan enabled

    event_params = hci.le_set_advertising_enable() # Advertising is disabled
    if event_params['Status'] != 0x00:
        #print(WARNING, 'Status of HCI_LE_Set_Advertising_Enable command: 0x%02x'%event_params['Status'])
        pass
    
    try:
        hci.le_set_scan_enable({
            'LE_Scan_Enable': 0x00, # Scanning disabled
            'Filter_Duplicates': 0x01 # Ignored
        })
    except RuntimeError as e:
        #print(WARNING, e)
        pass

    hci.set_event_filter({'Filter_Type': 0x00}) # Clear All Filters

    event_params = hci.read_bdaddr()
    if event_params['Status'] != 0:
        raise RuntimeError
    else:
        local_bd_addr = event_params['BD_ADDR'].upper()

    # Clear bluetoothd cache
    cache_path = PosixPath('/var/lib/bluetooth/') / local_bd_addr / 'cache'
    if cache_path.exists():
        for file in cache_path.iterdir():
            os.remove(file)


def main():
    args = None
    try:
        args = parse_cmdline()
        logger.debug("main(), args: {}".format(args))

        if not args['--adv']:
            if args['-i'] == 'The first HCI device':
                exitcode, output = subprocess.getstatusoutput(
                    'systemctl start bluetooth.service')
                if exitcode != 0:
                    logger.error("Failed to start bluetooth.service")
                    sys.exit(exitcode)
                try:
                    args['-i'] = HCI.get_default_hcistr() # May raise IndexError
                except IndexError:
                    logger.error('There is no available HCI device')
                    exit(-1)

            init_hci(args['-i'])

        if args['-m'] == 'br':
            br_scanner = BRScanner(args['-i'])
            if args['--lmp-feature']:
                br_scanner.scan_lmp_feature(args['BD_ADDR'])
            else:
                br_scanner = BRScanner(args['-i'])
                br_scanner.inquiry(inquiry_len=args['--inquiry-len'])
        elif args['-m'] == 'le':
            if args['--adv']:
                dev_paths = get_microbit_devpaths()
                LEScanner(microbit_devpaths=dev_paths).sniff_adv(args['--channel'])
            elif args['--ll-feature']:
                LEScanner(args['-i']).scan_ll_feature(
                    args['BD_ADDR'], args['--addr-type'], args['--timeout'])
            elif args['--smp-feature']:
                LEScanner(args['-i']).detect_pairing_feature(
                    args['BD_ADDR'], args['--addr-type'], args['--timeout'])
            else:
                LEScanner(args['-i']).scan_devs(args['--timeout'], 
                    args['--scan-type'], args['--sort'])
        elif args['-m'] == 'sdp':
            SDPScanner(args['-i']).scan(args['BD_ADDR'])
        elif args['-m'] == 'gatt':
            GATTScanner(args['-i']).scan(args['BD_ADDR'], args['--addr-type'],
                args['--include-descriptor'])
        elif args['-m'] == 'stack':
            StackScanner(args['-i']).scan(args['BD_ADDR'])
        elif args['-m'] == 'vuln':
            VulnScanner(args['-i']).scan(args['BD_ADDR'], args['--addr-type'])
        else:
            logger.error('Invalid scan mode')
    except ValueError as e:
        logger.error("{}".format(e))
        exit(1)
    except BluetoothError as e:
        logger.error('{}'.format(e))
    except RuntimeError as e:
        logger.error('{}'.format(e))
    except (BTLEException, ValueError) as e:
        logger.error('{}'.format(e))
        if 'le on' in str(e):
            print("        No BLE adapter? or missing sudo ?")
    except KeyboardInterrupt:
        if args != None and args['-i'] != None:
            output = subprocess.check_output(' '.join(['hciconfig', args['-i'], 'reset']), 
                    stderr=STDOUT, timeout=60, shell=True)
        logger.info("Canceled\n")


if __name__ == '__main__':
    main()
