"""
utils.py - part of miaowware/ae7qparser
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


from types import SimpleNamespace


__all__ = [
    "base_url",
    "ca_pfx",
    "colours",
    "lic_status_colours",
    "availability_colours",
    "ufn_colours",
    "app_status_colours",
    "prediction_colours",
]


base_url = "http://ae7q.com/query/"

ca_pfx = {
    "cf", "cg", "ch", "ci", "cj", "ck",
    "cy", "cz",
    "va", "vb", "vc", "vd", "ve", "vf", "vg",
    "vo",
    "vx", "vy",
    "xj", "xk", "xl", "xm", "xn", "xo",
}

colours = SimpleNamespace(
    green=0x99ff66,
    blue=0x99ccff,
    yellow=0xffff66,
    red=0xff99cc,
    grey=0xcccccc,
)

lic_status_colours = SimpleNamespace(
    active=colours.green,
    pre_uls_active=colours.blue,
    inactive=colours.yellow,
    expired=colours.red,
)

availability_colours = SimpleNamespace(
    available=colours.green,
    available_but_pending=colours.blue,
    inactive=colours.yellow,
    canceled_not_available=colours.red,
    active=colours.grey,
)

ufn_colours = SimpleNamespace(
    predict_grant=colours.green,
    predict_unknown=colours.blue,
    predict_dismissed_unless_action=colours.yellow,
    predict_dismissed=colours.red,
)

app_status_colours = SimpleNamespace(
    granted=colours.green,
    pending=colours.blue,
    withdrawn_amended=colours.yellow,
    dismissed=colours.red,
    other=colours.grey,
)

prediction_colours = SimpleNamespace(
    assignment=colours.green,
    unknown=colours.blue,
    unavailable_unless_action=colours.yellow,
    unavailable=colours.red,
    not_needed=colours.grey,
)
