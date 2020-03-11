"""
ae7qparser commandline interface
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


import ae7qparser

call = input("call? ")

calldata = ae7qparser.get_call(call)

print(calldata.tables[-1].csv)
# print(calldata.tables[0])

frn = input("frn? ")

frndata = ae7qparser.get_frn(frn)

print(type(frndata.tables[-1]))
print(frndata.tables[-1].csv)
# print(frndata.tables[0])
