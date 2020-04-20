# ae7qparser

An ae7q.com parser for modern amateur radio programs.

[![PyPI](https://img.shields.io/pypi/v/ae7qparser)](https://pypi.org/project/ae7qparser/) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/ae7qparser) ![PyPI - License](https://img.shields.io/pypi/l/ae7qparser)

Support: [![Discord](https://discordapp.com/api/guilds/656888365886734340/widget.png?style=shield)](https://discord.gg/SwyjdDN)

## Installation

`ae7qparser` requires Python 3.6 at minimum.

```none
$ pip install ae7qparser
```


## API Reference

*Coming soon. Refer to docstrings for now.*


## CLI Usage

**CLI is work in progress!**  

Currently, the CLI prints the members of each resulting object, including tables.

```none
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
```


## Copyright

Copyright 2020 classabbyamp, 0x5c  
Released under the MIT License.  
See `LICENSE` for the full license text.
