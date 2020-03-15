"""
ae7qparser commandline interface
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


import ae7qparser

call = input("call? ")

calldata = ae7qparser.get_call(call)

for table in calldata.tables:
    print(type(table))
    print(table.csv)

frn = input("frn? ")

frndata = ae7qparser.get_frn(frn)

for table in frndata.tables:
    print(type(table))
    print(table.csv)
