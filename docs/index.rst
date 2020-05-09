ae7qparser
==========

An `ae7q.com`_ parser for modern amateur radio programs.

Installation
------------

``ae7qparser`` requires Python 3.6 at minimum. Install by running::

    $ pip install ae7qparser

License
-------

Copyright 2020 classabbyamp, 0x5c

Released under the MIT License. See ``LICENSE`` for the full license text.

Reference
---------

.. toctree::
   :maxdepth: 3
   :glob:

   api
   classes/results
   classes/tables
   classes/rows
   classes/errors
   utils
   parser

CLI Usage
---------

.. note:: CLI is a work in progess!

``ae7qparser`` has a basic command-line interface that querys AE7Q for the data, then prints the parsed results::

    $ python3 -m ae7qparser -h

    usage: ae7qparser [-h] [-c [CALL [CALL ...]]] [-f [FRN [FRN ...]]] [-l [LID [LID ...]]] [-a [UFN [UFN ...]]]

    Retrieve and parse AE7Q data

    optional arguments:
      -h, --help            show this help message and exit
      -c [CALL [CALL ...]], --call [CALL [CALL ...]]
                            Get AE7Q data for a callsign
      -f [FRN [FRN ...]], --frn [FRN [FRN ...]]
                            Get AE7Q data for an FRN
      -l [LID [LID ...]], --lic [LID [LID ...]]
                            Get AE7Q data for a Licensee ID
      -a [UFN [UFN ...]], --app [UFN [UFN ...]]
                            Get AE7Q data for a ULS File Number

.. _ae7q.com: http://www.ae7q.com/
