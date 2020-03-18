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
parser.add_argument("-a" "--application", nargs="*", required=False,
                    help="Get AE7Q data for a ULS File Number")
args = parser.parse_args()


if args.c__call is not None:
    for call in args.c__call:
        calldata = ae7qparser.get_call(call)
        print(f"==== Callsign: {call} ====")
        for key, val in calldata.__dict__.items():
            if isinstance(val, ae7qparser.base.Table):
                print(f"{key}:")
                print(val.csv_pretty)
            else:
                print(f"{key}: {val}")
        print("")

if args.f__frn is not None:
    for frn in args.f__frn:
        frndata = ae7qparser.get_frn(frn)
        print(f"==== FRN: {frn} ====")
        for key, val in frndata.__dict__.items():
            if isinstance(val, ae7qparser.base.Table):
                print(f"{key}:")
                print(val.csv_pretty)
            else:
                print(f"{key}: {val}")
        print("")

if args.l__licensee is not None:
    for lid in args.l__licensee:
        liddata = ae7qparser.get_licensee_id(lid)
        print(f"==== Licensee ID: {lid} ====")
        for key, val in liddata.__dict__.items():
            if isinstance(val, ae7qparser.base.Table):
                print(f"{key}:")
                print(val.csv_pretty)
            else:
                print(f"{key}: {val}")
        print("")

if args.a__application is not None:
    for app_id in args.a__application:
        appdata = ae7qparser.get_application(app_id)
        print(f"==== ULS File Number: {app_id} ====")
        for key, val in appdata.__dict__.items():
            if isinstance(val, ae7qparser.base.Table):
                print(f"{key}:")
                print(val.csv_pretty)
            else:
                print(f"{key}: {val}")
        print("")
