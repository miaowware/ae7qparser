"""
utils.py - part of miaowware/ae7qparser
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


from types import SimpleNamespace


base_url = "http://ae7q.com/query/"

ca_pfx = {
    "cf", "cg", "ch", "ci", "cj", "ck",
    "cy", "cz",
    "va", "vb", "vc", "vd", "ve", "vf", "vg",
    "vo",
    "vx", "vy",
    "xj", "xk", "xl", "xm", "xn", "xo",
}

_colours = SimpleNamespace(
    green=0x99ff66,
    blue=0x99ccff,
    yellow=0xffff66,
    red=0xff99cc,
    grey=0xcccccc,
)

lic_status_colours = SimpleNamespace(
    active=_colours.green,
    pre_uls_active=_colours.blue,
    inactive=_colours.yellow,
    expired=_colours.red,
)

availability_colours = SimpleNamespace(
    available=_colours.green,
    available_but_pending=_colours.blue,
    inactive=_colours.yellow,
    canceled_not_available=_colours.red,
    active=_colours.grey,
)

ufn_colours = SimpleNamespace(
    predict_grant=_colours.green,
    predict_unknown=_colours.blue,
    predict_dismissed_unless_action=_colours.yellow,
    predict_dismissed=_colours.red,
)

app_status_colours = SimpleNamespace(
    granted=_colours.green,
    pending=_colours.blue,
    withdrawn_amended=_colours.yellow,
    dismissed=_colours.red,
    other=_colours.grey,
)

prediction_colours = SimpleNamespace(
    assignment=_colours.green,
    unknown=_colours.blue,
    unavailable_unless_action=_colours.yellow,
    unavailable=_colours.red,
    not_needed=_colours.grey,
)
