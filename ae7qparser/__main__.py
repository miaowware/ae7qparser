"""
ae7qparser commandline interface
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


import ae7qparser

call = input("call? ")

calldata = ae7qparser.get_call(call)
print(calldata)
print(repr(calldata))
