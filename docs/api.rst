API Reference
=============

.. module:: ae7qparser

Synchronous
-----------

.. warning:: If `requests`_ is not installed, all synchronous functions will raise ``NotImplmentedError``.

.. autofunction:: get_call

.. autofunction:: get_frn

.. autofunction:: get_licensee_id

.. autofunction:: get_application

Asynchronous
------------

.. warning:: If `aiohttp`_ is not installed, all asynchronous functions will raise ``NotImplmentedError``.

.. autofunction:: a_get_call

.. autofunction:: a_get_frn

.. autofunction:: a_get_licensee_id

.. autofunction:: a_get_application

.. _requests: https://pypi.org/project/requests/
.. _aiohttp: https://pypi.org/project/aiohttp/
