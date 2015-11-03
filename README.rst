=================
Markus Binsteiner
=================

    :Author: Markus Binsteiner

.. contents::
1 Pigshare
----------

Python client library and commandline tool for institutional Figshare.

The commandline options are created dynamically from the available api-method wrapper code, which is why some of them might feel a bit clumsy.

1.1 Requirements
~~~~~~~~~~~~~~~~

- python-dev package (for simplejson compilation I think)

- argparse

- setuptools

- restkit

- booby

- simplejson

- parinx

- pyclist

- argcomplete

1.2 Installation
~~~~~~~~~~~~~~~~

(sudo) pip install `https://github.com/UoA-eResearch/pigshare/archive/master.zip <https://github.com/UoA-eResearch/pigshare/archive/master.zip>`_

1.3 Usage (commandline client)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1.3.1 Connection details
^^^^^^^^^^^^^^^^^^^^^^^^

**pigshare** reads a config file $HOME/.pigshare.conf, in the format:

``[default]
url = https://api.figsh.com/v2
token = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
``

(note, this example uses the staging environment)

**pigshare** supports profiles, so you can have multiple profiles in your config file like for example:

``[default]
url = https://api.figsh.com/v2
token = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
[markus]
url = https://api.figshare.com/v2
token =  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
[not_markus]
url = https://api.figshare.com/v2
token = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
``

Now, when you call **pigshare** with the ****-p**** argument, you can switch between different backends/identities:

``pigshare -p markus blahblahblah
``

the command you chose will be using the selected connection parameters.

1.3.2 General usage
^^^^^^^^^^^^^^^^^^^

For public read access, this is not required.

Basic usage is displayed via:

``pigshare -h
``

Command specific usage can be displayed via:

``pigshare [command] -h
``

1.3.3 Filtering
^^^^^^^^^^^^^^^

(Sub-)commands that display one or more items can be called using an output filter (the ****-o**** argument before the sub-command). Depending on the sub-command called only certain fields of the items are available (e.g. **list\ :sub:`articles`\** has only a subset of fields compared to **read\ :sub:`article`\**).

I'd recommend trying out the command you want to run first, and checking which fields are available, then run the command again with the appropriate filter. A command to list all articles and only display the **doi** and **title** of each article would be:

``pigshare -o doi,title list_articles
``

1.3.4 Commonly used commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.3.4.1 List articles
:::::::::::::::::::::

To list all articles and display the **doi**, (internal) **id**, **title**, **url**, and **published\ :sub:`date`\** for each, issue:

``pigshare list_articles
``

To display a table with all articles, but only display **doi** and **title**, you can use:

``pigshare -o doi,title list_articles
``

1.3.4.2 Read an article
:::::::::::::::::::::::

To display the properties of an article, use:

``pigshare read_article --id [article_id]
``

To display the doi of an article, use:

``pigshare -o doi read_article --id [article_id]
``

1.3.4.3 Search for articles
:::::::::::::::::::::::::::

To list all articles matching a search string, issue:

``pigshare search_articles --search_term [search_term]
``

To display all dois and titles of articles that match a search string:

``pigshare -o doi,title search_articles --search_term [search_term]
``

1.3.5 Other random example calls:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

``pigshare create_article --article '{"title": "Markus test", "custom_fields": {"key1": "value"}}'
``

``pigshare create_collection --collection '{"title": "Collection markus test", "articles": [2009074,2009075,2009084], "custom_fields": {"test1": "value1"}}'
``

``pigshare add_article --collection_id 2761 --article_ids [2009103,2009106]
``

``pigshare -o id -s ',' search_my_articles --search_term markus
``

``for id in `pigshare -o id list_my_articles`; do echo "$id"; pigshare add_article --collection_id 3222 --article_id "$id"; done
``

``pigshare update_collection --id 2761 --collection '{"title": "Collection markus test changed", "articles": [2009074,2009075]}'
``

``pigshare update_article --id 2000077 --article '{"categories": [2]}'
``

``pigshare update_article --id 2000077 --article '{"custom_fields": {"field1":"value1"}}'
``

1.4 Usage (Library)
~~~~~~~~~~~~~~~~~~~

TODO
