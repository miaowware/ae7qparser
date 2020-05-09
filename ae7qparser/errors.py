"""
errors.py - part of miaowware/ae7qparser
---

Copyright 2020 classabbyamp, 0x5c
Released under the terms of the MIT license.
"""


class Ae7qError(Exception):
    """The base error class for all errors raised by ae7qparser."""
    pass


try:
    import requests
except ImportError:
    pass
else:
    class Ae7qRequestError(Ae7qError):
        """Raised when there's an error related to a synchronous HTTP request."""
        def __init__(self, response: requests.Response):
            msg = f"Request failed: {response.status_code} {response.reason}"
            super().__init__(msg)
            self.response = response
            self.status = response.status_code
            self.reason = response.reason


try:
    import aiohttp
except ImportError:
    pass
else:
    class Ae7qAsyncRequestError(Ae7qError):
        """Raised when there's an error related to an asynchronous HTTP request."""
        def __init__(self, response: aiohttp.ClientResponse):
            msg = f"Request failed: {response.status} {response.reason}"
            super().__init__(msg)
            self.response = response
            self.status = response.status
            self.reason = response.reason


class Ae7qParsingError(Ae7qError):
    """Raised when there's an error related to parsing the AE7Q data."""
    def __init__(self, msg: str):
        super().__init__(msg)


class Ae7qImportError(Ae7qError):
    """Raised when there's an error importing a library."""
    def __init__(self, msg: str):
        super().__init__(msg)
