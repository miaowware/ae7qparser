"""
ae7qparser commandline interface
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""

import argparse
import sys

import ae7qparser


parser = argparse.ArgumentParser(prog="ae7qparser", description="Retrieve and parse AE7Q data")
parser.add_argument("-c", "--call", required=False, metavar="CALL", nargs="*",
                    help="Get AE7Q data for callsigns")
parser.add_argument("-f", "--frn", required=False, metavar="FRN", nargs="*",
                    help="Get AE7Q data for FRNs")
parser.add_argument("-l", "--lic", required=False, metavar="LID", nargs="*",
                    help="Get AE7Q data for Licensee IDs")
parser.add_argument("-a", "--app", required=False, metavar="UFN", nargs="*",
                    help="Get AE7Q data for ULS File Numbers")
if len(sys.argv) == 1:
    parser.print_help(sys.stderr)
    sys.exit(1)
args = parser.parse_args()


if args.call is not None:
    for call in args.call:
        calldata = ae7qparser.get_call(call)
        print(f"==== Callsign: {call} ====")
        for key, val in calldata.__dict__.items():
            if isinstance(val, ae7qparser.tables.Table):
                print(f"{key}:")
                print(val.csv_pretty)
            else:
                print(f"{key}: {val}")
        print("")

if args.frn is not None:
    for frn in args.frn:
        frndata = ae7qparser.get_frn(frn)
        print(f"==== FRN: {frn} ====")
        for key, val in frndata.__dict__.items():
            if isinstance(val, ae7qparser.tables.Table):
                print(f"{key}:")
                print(val.csv_pretty)
            else:
                print(f"{key}: {val}")
        print("")

if args.lic is not None:
    for lid in args.lic:
        liddata = ae7qparser.get_licensee_id(lid)
        print(f"==== Licensee ID: {lid} ====")
        for key, val in liddata.__dict__.items():
            if isinstance(val, ae7qparser.tables.Table):
                print(f"{key}:")
                print(val.csv_pretty)
            else:
                print(f"{key}: {val}")
        print("")

if args.app is not None:
    for app_id in args.app:
        appdata = ae7qparser.get_application(app_id)
        print(f"==== ULS File Number: {app_id} ====")
        for key, val in appdata.__dict__.items():
            if isinstance(val, ae7qparser.tables.Table):
                print(f"{key}:")
                print(val.csv_pretty)
            else:
                print(f"{key}: {val}")
        print("")
