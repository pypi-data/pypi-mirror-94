#!/usr/bin/env python3

r"""bluescan v0.5.0

A powerful Bluetooth scanner.

Author: Sourcell Xu from DBAPP Security HatLab.

License: GPL-3.0

Usage:
    bluescan (-h | --help)
    bluescan (-v | --version)
    bluescan [-i <hci>] -m br [--inquiry-len=<n>]
    bluescan [-i <hci>] -m br --lmp-feature BD_ADDR
    bluescan [-i <hci>] -m le [--scan-type=<type>] [--timeout=<sec>] [--sort=<key>]
    bluescan [-i <hci>] -m le [--ll-feature|--smp-feature] [--timeout=<sec>] --addr-type=<type> BD_ADDR
    bluescan -m le --adv [--channel=<num>]
    bluescan [-i <hci>] -m sdp BD_ADDR
    bluescan [-i <hci>] -m gatt [--include-descriptor] --addr-type=<type> BD_ADDR
    bluescan [-i <hci>] -m vuln [--addr-type=<type>] BD_ADDR

Arguments:
    BD_ADDR    Target Bluetooth device address. FF:FF:FF:00:00:00 means local 
               device.

Options:
    -h, --help              Display this help.
    -v, --version           Show the version.
    -i <hci>                HCI device used for subsequent scans. [default: The first HCI device]
    -m <mode>               Scan mode, support BR, LE, SDP, GATT and vuln.
    --inquiry-len=<n>       Inquiry_Length parameter of HCI_Inquiry command. [default: 8]
    --lmp-feature           Scan LMP features of the remote BR/EDR device.
    --scan-type=<type>      Scan type used for scanning LE devices, active or 
                            passive. [default: active]
    --timeout=<sec>         Duration of the LE scanning, but may not be precise. [default: 10]
    --sort=<key>            Sort the discovered devices by key, only support 
                            RSSI now. [default: rssi]
    --adv                   Sniff advertising physical channel PDU. Need at 
                            least one micro:bit.
    --ll-feature            Scan LL features of the remote LE device.
    --smp-feature           Detect pairing features of the remote LE device.
    --channel=<num>         LE advertising physical channel, 37, 38 or 39). [default: 37,38,39]
    --include-descriptor    Fetch descriptor information.
    --addr-type=<type>      Type of the LE address, public or random.
"""


import logging

from pyclui import red
from pyclui import Logger

from docopt import docopt
from .helper import valid_bdaddr


logger = Logger(__name__, logging.INFO)


def parse_cmdline() -> dict:
    args = docopt(__doc__, version='v0.5.0', options_first=True)
    logger.debug("ui.parse_cmdline, args: {}".format(args))

    args['-m'] = args['-m'].lower()
    args['--inquiry-len'] = int(args['--inquiry-len'])
    args['--timeout'] = int(args['--timeout'])
    args['--sort'] = args['--sort'].lower()

    if args['--channel'] is not None:
        args['--channel'] =  [int(n) for n in args['--channel'].split(',')]
        args['--channel'] = set(args['--channel'])
        if args['--channel'].issubset({37, 38, 39}):
            args['--channel'] = list(args['--channel'])
        else:
            raise ValueError("Invalid channel {}, ".format(args['--channel']) \
                + "must a subset of {37, 38, 39}")

    if args['BD_ADDR'] is not None:
        args['BD_ADDR'] = args['BD_ADDR'].lower()
        if not valid_bdaddr(args['BD_ADDR']):
            raise ValueError("Invalid BD_ADDR: " + red(args['BD_ADDR']))
    
    if args['--scan-type'] is not None:
        args['--scan-type'] = args['--scan-type'].lower()
        if args['--scan-type'] not in ('active', 'passive'):
            raise ValueError("Invalid scan type %s, " % \
                red(args['--scan-type']) + "must be active or passive.")

    if args['--addr-type'] is not None:
        args['--addr-type'] = args['--addr-type'].lower()
        if args['--addr-type'] not in ('public', 'random'):
            raise ValueError("Invalid address type %s, " % \
                args['--addr-type'] + "must be public or random.")

    return args


def __test():
    pass


if __name__ == '__main__':
    __test()
