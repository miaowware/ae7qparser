"""
ae7qparser commandline interface
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""

import argparse

import ae7qparser


parser = argparse.ArgumentParser(description="Retrieve and parse AE7Q data")
parser.add_argument("-c" "--call", nargs="*", required=False,
                    help="Get AE7Q data for a callsign")
parser.add_argument("-f" "--frn", nargs="*", required=False,
                    help="Get AE7Q data for an FRN")
parser.add_argument("-l" "--licensee", nargs="*", required=False,
                    help="Get AE7Q data for a Licensee ID")
args = parser.parse_args()


if args.c__call is not None:
    for call in args.c__call:
        calldata = ae7qparser.get_call(call)
        print(calldata.__dict__)

if args.f__frn is not None:
    for frn in args.f__frn:
        frndata = ae7qparser.get_frn(frn)
        print(frndata.__dict__)

if args.l__licensee is not None:
    for lid in args.l__licensee:
        liddata = ae7qparser.get_licensee_id(lid)
        print(liddata.__dict__)
