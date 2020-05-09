Dev Note: Parser
================

This page documents the internal parsing process for ``ae7qparser``. Reading and understanding this is not required to
use ``ae7qparser``, but it may be helpful for future developers, current developers in the future, or curious cats.

TODO: explain how the parser works here

Finding Tables
--------------

Once the HTML of the requested page has been retrieved, it is parsed using `Beautiful Soup`_. All relevant ``<table>``
elements on AE7Q will have ``class="Database"``, which gives an easy-to-use identifier for finding the tables to parse.
Unfortunately there is no further identification of which table is which in the HTML.

This is done within the ``get_`` functions.

Parsing Tables
--------------

Once a list of ``<table>`` elements has been found with Beautiful Soup, it is passed to ``_parse_tables()``.

For each table in that list, all ``<tr>`` elements are found. Those row elements are parsed in ``_parse_table_rows()``.

**TODO: explain _parse_table_rows**

Getting Cell Text
^^^^^^^^^^^^^^^^^

In ``_get_cell_text()``, the conversion from Beautiful Soup to meaningful data happens. By default, the Beautiful Soup
generator `stripped_strings`_ leaves a lot of internal whitespace because of the way AE7Q's HTML is written. This is
solved using:

.. code-block:: python

    text = " ".join([" ".join(x.split()) for x in cell.stripped_strings])

    # which is equivalent to the psuedocode:

    for each item in cell.stripped_strings:
        split it at whitespace into words
        join those words, separated by spaces
    join each item, separated by spaces

Assigning Tables
----------------

Once the tables are parsed, some basic observations are used to assign the tables to different classes in the ``_assign``
functions. Most use the number of columns and/or the column headers that are known to be in the structure of that kind
of table. This is one of the more finicky parts of the parser, because a change in those could cause a failure to parse
the tables correctly. If no special table class can be assigned, then the base class :class:`ae7qparser.tables.Table` is used.

.. _Beautiful Soup: https://pypi.org/project/beautifulsoup4/

.. _stripped_strings: https://www.crummy.com/software/BeautifulSoup/bs4/doc/#strings-and-stripped-strings
