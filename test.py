"""
test.py - part of miaowware/ae7qparser
---

An ae7q.com parser for modern amateur radio programs.

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


import ae7qparser


# A set of test queries
test_calls = [
    "W1W",              # special event callsign
    "KN8U",             # restricted with history and trustee
    "VA2SHF",           # Canadian
    "BY4EPL",           # Foreign
]

test_frns = [
    "0016605636",       # has application history with vanity applications
    "1",                # Invalid
]

test_lids = [
    "L01295086",        # has application history with vanity applications
    "L00766846",
    "1",                # Invalid
]

test_apps = [
    "0008963527",       # vanity application
    "1",                # Invalid
]

for call in test_calls:
    print(ae7qparser.get_call(call))

for frn in test_frns:
    print(ae7qparser.get_frn(frn))

for lid in test_lids:
    print(ae7qparser.get_licensee_id(lid))

for app in test_apps:
    print(ae7qparser.get_application(app))
