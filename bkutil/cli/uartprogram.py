#!/usr/bin/env python3
# encoding: utf8
#
# HID Download Tool
#
# Copyright (c) BekenCorp. (chunjian.tian@bekencorp.com).  All rights reserved.
#
# This software may be distributed under the terms of the BSD license.
# See README for more details.

import sys
import os
import argparse
from bkutil import UartDownloader
from bkutil.bin_parser import BIN_TYPE, format_bin_info, load_bin_file, select_partitions


def parse_args():
    description = '''Beken Uart Downloader.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-d', '--device',
                        default='/dev/ttyUSB0',
                        help="Uart device, default to /dev/ttyUSB0")
    parser.add_argument('-s', '--startaddr', type=lambda  x: int(x, 16),
                        default=0x11000,
                        help="burn flash address for normal bin, defaults to 0x11000")
    parser.add_argument('-b', '--baudrate', type=int,
                        default=2000000,
                        help="burn uart baudrate, defaults to 2000000")
    parser.add_argument('-u', '--unprotect', action="store_true",
                        help="unprotect flash first, used by BK7231N")
    parser.add_argument('-e', '--erase', action='store_true',
                        help="Erase chip")
    parser.add_argument('-i', '--info', action='store_true',
                        help="Show partition info for composite bin such as all-app.bin")
    parser.add_argument('-p', '--partition',
                        help="Flash selected partitions only, e.g. 0,2,4")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Print partition info while flashing")
    parser.add_argument('filename', nargs='?',
                        help='specify file_crc.bin or all-app.bin if -e is not provided')
    args = parser.parse_args()

    return args


def check_bin_file(args):
    if not args.filename:
        print(f"filename must be specified, use -h for help")
        sys.exit(-1)
    if not os.path.exists(args.filename):
        print(f"File {args.filename} doesn't exist")
        sys.exit(-1)


def main():
    args = parse_args()

    # only parse the bin file, no device needed
    if args.info:
        check_bin_file(args)
        bin_type, bin_list = load_bin_file(args.filename, args.startaddr)
        for line in format_bin_info(bin_type, select_partitions(bin_list, args.partition)):
            print(line)
        return

    if not os.path.exists(args.device):
        print(f"Device {args.device} doesn't exist")
        sys.exit(-1)

    if not args.erase:
        check_bin_file(args)

    downloader = UartDownloader(args.device, args.baudrate, args.unprotect,
                                verbose=args.verbose)

    if args.erase:
        downloader.chip_erase()
        return

    bin_type, bin_list = load_bin_file(args.filename, args.startaddr)
    if bin_type == BIN_TYPE.TYPE_NORMAL:
        if args.partition:
            print("--partition only applies to composite bin such as all-app.bin")
            sys.exit(-1)
        # a normal bin is flashed at the address given by -s
        downloader.programm(args.filename, args.startaddr)
    else:
        # a composite bin carries its own partition addresses, -s is ignored
        downloader.program_bin_list(select_partitions(bin_list, args.partition))


if __name__ == '__main__':
    main()
