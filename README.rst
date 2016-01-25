=================
Markus Binsteiner
=================

    :Author: Markus Binsteiner

.. contents::

1 Pigshare
----------

Python client library and commandline tool for institutional Figshare.

The commandline options are created dynamically from the available api-method wrapper code, which is why some of them might feel a bit clumsy. Also, many of the commands only support values as json-formatted strings. I might change that in the future, but it'd require more complex cli-argparse creation code and I'm not sure whether it's worth it.

1.1 Notes
~~~~~~~~~

So far, I've only tested this on Linux.

1.2 Requirements
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

1.3 Installation
~~~~~~~~~~~~~~~~

1.3.1 Release
^^^^^^^^^^^^^

::

    (sudo) pip install pigshare

1.3.2 Development version from Github
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    (sudo) pip install https://github.com/UoA-eResearch/pigshare/archive/master.zip

1.4 Usage (commandline client)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1.4.1 Connection details
^^^^^^^^^^^^^^^^^^^^^^^^

*pigshare* reads a config file $HOME/.pigshare.conf, in the format:

::

    [default]
    url = https://api.figsh.com/v2
    token = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

(note, this example uses the staging environment)

*pigshare* supports profiles, so you can have multiple profiles in your config file like for example:

::

    [default]
    url = https://api.figsh.com/v2
    token = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    [markus]
    url = https://api.figshare.com/v2
    token =  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    [not_markus_but_somebody_else]
    url = https://api.figshare.com/v2
    token = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

Now, when you call *pigshare* with the **-p** argument, you can switch between different backends/identities:

::

    pigshare -p markus [command]

The command you chose will be using the selected connection parameters.

1.4.2 Features:
^^^^^^^^^^^^^^^

1.4.2.1 Supported
:::::::::::::::::

- creation of articles, via a json string or interactively

- listing of public and private articles

- searching for public and private articles

- updating of articles

- creation of collections, via a json string or interactively

- listing of public and private collections

- searching for public and private collections

- updating of collections

- listing of categories and their ids

- listing of licenses and their ids

- publishing of articles and collections

1.4.2.2 Not (yet) supported
:::::::::::::::::::::::::::

- queries with more than 1000 results, only the first 1000 results are displayed

- automatically deal with the 10 item limits on some methods

- everything else

1.4.3 General usage
^^^^^^^^^^^^^^^^^^^

Basic usage is displayed via:

::

    pigshare -h

Command specific usage can be displayed via:

::

    pigshare [command] -h

1.4.4 Interactive input
^^^^^^^^^^^^^^^^^^^^^^^

Some of the commands offer interactive input (e.g. create\ :sub:`article`\, edit\ :sub:`article`\, create\ :sub:`collection`\, ...). If you choose to use that, you can get help on any particular field by typing '?' as value. Some fields support a more advanced help functionality:

- **categories**: '?' lists all available categories along with their internal figshare id (which you need to provide as input), '? [search\ :sub:`term`\]' lets you filter this list with the provided search term

- **authors**: '?' lists all authors and their internal ids (always use the latter if you know it) that *pigshare* knows about (authors that came up in past queries, so this is not a comprehensible list, if you can't find the author you want, try to find it via the web-interface)

- **licenses**: '?' lists all licenses and their id, '? search\ :sub:`term`\' filters the result

- **defined\ :sub:`type`\**: '?' lists the available and valid article types

Some fields support multiple values (list input). If that's the case, *pigshare* will tell you about it, and let you input the single items one after another. Once you are finished, just press 'enter' on an empty field.

1.4.5 Filtering of output fields
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

(Sub-)commands that display one or more items can be called using an output filter (the **-o** argument before the sub-command). Depending on the sub-command called only certain fields of the items are available (e.g. **list\ :sub:`articles`\** has only a subset of fields compared to **read\ :sub:`article`\**).

I'd recommend trying out the command you want to run first, and checking which fields are available, then run the command again with the appropriate filter. A command to list all articles and only display the **doi** and **title** of each article would be:

::

    pigshare -o doi,title list_articles

For more advanced filtering, consider piping in the 'full' output of *pigshare* into a tool like jq ( `https://stedolan.github.io/jq/ <https://stedolan.github.io/jq/>`_ ).

1.4.6 Commonly used commands
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

1.4.6.1 Articles
::::::::::::::::

1.4.6.1.1 List articles
'''''''''''''''''''''''

To list all articles and display the **doi**, (internal) **id**, **title**, **url**, and **published\ :sub:`date`\** for each, issue:

::

    pigshare list_articles

To display a table with all articles, but only display **doi** and **title**, you can use:

::

    pigshare -o doi,title list_articles

1.4.6.1.2 Read an article
'''''''''''''''''''''''''

To display the properties of an article, use:

::

    pigshare read_article [article_id]

To display the doi and all tags of a number of articles, use (tags are not part of the 'short' article format that the **list\ :sub:`articles`\** command returns):

::

    pigshare -o doi,tags read_article [article_id] [article_id] [article_id]

1.4.6.1.3 Search for articles
'''''''''''''''''''''''''''''

To list all articles matching a search string, issue:

::

    pigshare search_articles --search_term [search_term]

To display all dois and titles of articles that match a search string:

::

    pigshare -o doi,title search_articles --search_term [search_term]

1.4.6.1.4 List my articles
''''''''''''''''''''''''''

To list all of your own articles:

::

    pigshare list_my_articles

1.4.6.1.5 To create a new article
'''''''''''''''''''''''''''''''''

::

    pigshare create_article --article '{"title": "Markus test", "custom_fields": {"key1": "value"}}'

Or, if you want *pigshare* to ask your input for every one of the fields:

::

    pigshare create_article

1.4.6.1.6 Upload one (or more files) for an article
'''''''''''''''''''''''''''''''''''''''''''''''''''

::

    pigshare upload_new_file --id [article_id] file1 [file2 ... ...]

1.4.6.2 Collections
:::::::::::::::::::

Very similar to articles.

1.4.7 Workflows
^^^^^^^^^^^^^^^

1.4.7.1 Reorder articles in collections
:::::::::::::::::::::::::::::::::::::::

Because of how Figshare works at the moment (collections are sorted by timestamp), the easiest way to change the order of articles within a collection is to 're-publish' an already published article. Usually that doesn't result in a new DOI for that article (which would be bad).

So, if you want to order the articles alphabetically for example, you could do it this way:

- first, find the list of article ids

  ::

      $ pigshare -o title,id -p martin search_my_articles --search_term ISSP
      ISSP1991: Religion I  2000910
      ISSP1992: Social Inequality II  2000913
      ISSP1993: Environment I 2000916
      ISSP1994: Family and Changing Gender Roles II 2000919
      ISSP1995: National Identity I 2000922
      ISSP1996: Role of Government III  2000925
      ISSP1997: Work Orientations II  2000928
      ISSP1998: Religion II 2000934
      ISSP1999: Social Inequality III 2000937
      ISSP2000: Environment II  2000940
      ISSP2001: Social Networks II  2000943
      ISSP2002: Family and Changing Gender Roles III  2000946
      ISSP2003: National Identity II  2000949
      ISSP2004: Citizenship I 2000952
      ISSP2005: Work Orientations III 2000955
      ISSP2006: Role of Government IV 2000958
      ISSP2007: Leisure Time and Sports I 2000961
      ISSP2008: Religion III  2000964
      ISSP2009: Social Inequality IV  2000967
      ISSP2010: Environment III 2000970

- then, 'touch' (publish) the articles in the right (reverse) order

  ::

      pigshare -p martin publish_article 2000970 2000967 2000964 2000961 2000958 2000955 2000952 2000949 2000946 2000943 2000940 2000937 2000934 2000928 2000925 2000922 2000919 2000916 2000913 2000910

- check the webfrontend whether it worked by refreshing the collections page

Be aware that if an article got a new version since it was added to a collection, the old version of the article is included in it. If you want the new version, you need to manually remove and re-add the article before you do anything else.

1.4.8 Other random example calls:
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

::

    # create new collection
    pigshare create_collection --collection '{"title": "Collection markus test", "articles": [2009074,2009075,2009084], "custom_fields": {"test1": "value1"}}'

::

    # add articles to a collection
    pigshare add_article --id 2761 --article_ids [2009103,2009106]

::

    # search all my articles that contain a search_term, display only ids, separated by ',' (useful to copy and paste into 'add_article' command)
    pigshare -o id -s ',' search_my_articles --search_term [search_term]

::

    # list all of your personal articles, and add all of them to a collection
    for id in `pigshare -o id list_my_articles`; do echo "$id"; pigshare add_article --collection_id 3222 --article_id "$id"; done

::

    # update/overwrite the title and articles connected to a collection
    pigshare update_collection --id 2761 --collection '{"title": "Collection markus test changed", "articles": [2009074,2009075]}'

::

    # update/overwrite the categories field in a collection
    pigshare update_article --id 2000077 --article '{"categories": [2]}'

::

    # update/overwrite the custom_fields of a collection
    pigshare update_article --id 2000077 --article '{"custom_fields": {"field1":"value1"}}'

1.5 Usage (Library)
~~~~~~~~~~~~~~~~~~~

TODO
