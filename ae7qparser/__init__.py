"""
ae7qparser
---

An ae7q.com parser for modern amateur radio programs.

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


from .__info__ import __version__   # noqa: F401
from .dummy import *                # noqa: F401, F403
try:
    import requests                 # noqa: F401
except ImportError:
    pass
else:
    from .sync import *             # noqa: F401, F403
try:
    import aiohttp                  # noqa: F401
except ImportError:
    pass
else:
    from .asynch import *            # noqa: F401, F403
