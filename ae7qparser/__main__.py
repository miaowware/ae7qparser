"""
ae7qparser commandline interface
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


import ae7qparser

# call = input("call? ")
call = "kn8u"

calldata = ae7qparser.get_call(call)

print(calldata.__dict__)

# frn = input("frn? ")
frn = "0016605636"

frndata = ae7qparser.get_frn(frn)

print(frndata.__dict__)

# lid = input("lid? ")
lid = "L01295086"

liddata = ae7qparser.get_licensee_id(lid)

print(liddata.__dict__)
