:Author: Markus Binsteiner

Pigshare
========

Python client library and commandline tool for Figshare.

The commandline options are created dynamically from the available
api-method wrapper code, which is why some of them might feel a bit
clumsy. Also, many of the commands only support values as json-formatted
strings. I might change that in the future, but it'd require more
complex cli-argparse creation code and I'm not sure whether it's worth
it.

Notes
-----

So far, I've only tested this on Linux.

Requirements
------------

-  python-dev package (for simplejson compilation I think)

-  argparse
-  setuptools
-  restkit
-  booby
-  simplejson
-  parinx
-  pyclist
-  argcomplete

Installation
------------

Release
~~~~~~~

.. code:: example

    (sudo) pip install pigshare

Development version from Github
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: example

    (sudo) pip install https://github.com/UoA-eResearch/pigshare/archive/master.zip

Usage (commandline client)
--------------------------

Connection details
~~~~~~~~~~~~~~~~~~

Config file location
^^^^^^^^^^^^^^^^^^^^

*pigshare* reads a config file $HOME/.pigshare.conf, in the format:

.. code:: example

    [default]
    url = https://api.figsh.com/v2
    token = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

(note, this example uses the staging environment)

Config file format
^^^^^^^^^^^^^^^^^^

*pigshare* supports profiles, so you can have multiple profiles in your
config file like for example:

.. code:: example

    [default]
    url = https://api.figsh.com/v2
    token = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    [markus]
    url = https://api.figshare.com/v2
    token =  xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
    [not_markus_but_somebody_else]
    url = https://api.figshare.com/v2
    token = xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx

In addition, if you want to use certain statistics features for the
institutional version of figshare (documented here:
`stats\ :sub:`apidoc` <https://github.com/figshare/user_documentation/blob/master/Stats/index.md>`__),
you'll need to add a base64 encoded *username:password* value under the
*stats\ :sub:`token`* key (for the right profile, of course), e.g.:

.. code:: example

    stats_token = dXNlcm5hbWU6cGFzc3dvcmQK

Profile switching
^^^^^^^^^^^^^^^^^

Now, when you call *pigshare* with the **-p** argument, you can switch
between different backends/identities:

.. code:: example

    pigshare -p markus [command]

The command you chose will be using the selected connection parameters.

Features:
~~~~~~~~~

Supported
^^^^^^^^^

-  creation of articles, via a json string or interactively
-  listing of public and private articles
-  searching for public and private articles
-  updating of articles
-  creation of collections, via a json string or interactively
-  listing of public and private collections
-  searching for public and private collections
-  updating of collections
-  listing of categories and their ids
-  listing of licenses and their ids
-  publishing of articles and collections
-  initial support for getting statistics for
   articles/collections/authors (not 100% yet)

Not (yet) supported
^^^^^^^^^^^^^^^^^^^

-  queries with more than 1000 results, only the first 1000 results are
   displayed
-  automatically deal with the 10 item limits on some methods
-  everything else

General usage
~~~~~~~~~~~~~

Basic usage is displayed via:

.. code:: example

    pigshare -h

Command specific usage can be displayed via:

.. code:: example

    pigshare [command] -h

Interactive input
~~~~~~~~~~~~~~~~~

Some of the commands offer interactive input (e.g.
create\ :sub:`article`, edit\ :sub:`article`, create\ :sub:`collection`,
...). If you choose to use that, you can get help on any particular
field by typing '?' as value. Some fields support a more advanced help
functionality:

-  **categories**: '?' lists all available categories along with their
   internal figshare id (which you need to provide as input), '?
   [search:sub:`term`]' lets you filter this list with the provided
   search term
-  **authors**: '?' lists all authors and their internal ids (always use
   the latter if you know it) that *pigshare* knows about (authors that
   came up in past queries, so this is not a comprehensible list, if you
   can't find the author you want, try to find it via the web-interface)
-  **licenses**: '?' lists all licenses and their id, '?
   search\ :sub:`term`' filters the result
-  **defined\ :sub:`type`**: '?' lists the available and valid article
   types

Some fields support multiple values (list input). If that's the case,
*pigshare* will tell you about it, and let you input the single items
one after another. Once you are finished, just press 'enter' on an empty
field.

Filtering of output fields
~~~~~~~~~~~~~~~~~~~~~~~~~~

(Sub-)commands that display one or more items can be called using an
output filter (the **-o** argument before the sub-command). Depending on
the sub-command called only certain fields of the items are available
(e.g. **list\ :sub:`articles`** has only a subset of fields compared to
**read\ :sub:`article`**).

I'd recommend trying out the command you want to run first, and checking
which fields are available, then run the command again with the
appropriate filter. A command to list all articles and only display the
**doi** and **title** of each article would be:

.. code:: example

    pigshare -o doi,title list_articles

For more advanced filtering, consider piping in the 'full' output of
*pigshare* into a tool like jq ( https://stedolan.github.io/jq/ ).

Commonly used commands
~~~~~~~~~~~~~~~~~~~~~~

Articles
^^^^^^^^

List articles
'''''''''''''

To list all articles and display the **doi**, (internal) **id**,
**title**, **url**, and **published\ :sub:`date`** for each, issue:

.. code:: example

    pigshare list_articles

To display a table with all articles, but only display **doi** and
**title**, you can use:

.. code:: example

    pigshare -o doi,title list_articles

Read an article
'''''''''''''''

To display the properties of an article, use:

.. code:: example

    pigshare read_article [article_id]

To display the doi and all tags of a number of articles, use (tags are
not part of the 'short' article format that the
**list\ :sub:`articles`** command returns):

.. code:: example

    pigshare -o doi,tags read_article [article_id] [article_id] [article_id]

Search for articles
'''''''''''''''''''

To list all articles matching a search string, issue:

.. code:: example

    pigshare search_articles --search_term [search_term]

To display all dois and titles of articles that match a search string:

.. code:: example

    pigshare -o doi,title search_articles --search_term [search_term]

List my articles
''''''''''''''''

To list all of your own articles:

.. code:: example

    pigshare list_my_articles

To create a new article
'''''''''''''''''''''''

.. code:: example

    pigshare create_article --article '{"title": "Markus test", "custom_fields": {"key1": "value"}}'

Or, if you want *pigshare* to ask your input for every one of the
fields:

.. code:: example

    pigshare create_article

Upload one (or more files) for an article
'''''''''''''''''''''''''''''''''''''''''

.. code:: example

    pigshare upload_new_file --id [article_id] file1 [file2 ... ...]

Collections
^^^^^^^^^^^

Very similar to articles.

Statistics
^^^^^^^^^^

Statistics can be queried as totals, timeline, or breakdown.
Documentation can be found here:
`stats\ :sub:`apidoc` <https://github.com/figshare/user_documentation/blob/master/Stats/index.md>`__

Pigshare follows the api methods pretty closely, so you should be able
to figure out how it works yourself fairly easily.

An example call to get the total number of views for an article (that
was published in an institutional figshare, omit the *-i* parameter if
that was not the case):

.. code:: example

    pigshare -i auckland get_total_article_views 2075410
    {
        "2075410": {
        "totals": 204
      }
    }

Total views for an author:

.. code:: example

    pigshare get_total_author_views 117523
    {
        "1175235": {
        "totals": 481
      }
    }

Breakdown of downloads for an institutional article, by day:

.. code:: example

    pigshare -i auckland get_breakdown_article_downloads --granularity day 2075410
    {
      "2075410": {
        "breakdown": {
          "2016-05-06": {
            "United States": {
              "Mountain View": 1,
              "total": 1
            }
          },
          "2016-05-10": {
            "New Zealand": {
              "Auckland": 1,
              "total": 1
            }
          },
          "2016-05-16": {
            "New Zealand": {
              "Auckland": 1,
              "total": 1
            }
          }
        }
      }
    }

A pipeline to get the total downloads of all your own articles:

.. code:: example

     pigshare -o id list_my_articles | xargs pigshare get_total_article_downloads

And so on.

Workflows
~~~~~~~~~

Reorder articles in collections
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Because of how Figshare works (collections are sorted by the order they
were added to the collection), the easiest way to change the order of
articles within a collection is to remove all articles from a
collection, then add them in the right order, and re-publish the
collection again.

So, if you want to order the articles alphabetically for example, you
could do it this way:

-  first, find the list of article ids

   .. code:: example

       $ pigshare -o title,id search_my_articles --search_term ISSP
       ISSP1991: Religion I    2000910
       ISSP1992: Social Inequality II  2000913
       ISSP1993: Environment I 2000916
       ISSP1994: Family and Changing Gender Roles II   2000919
       ISSP1995: National Identity I   2000922
       ISSP1996: Role of Government III    2000925
       ISSP1997: Work Orientations II  2000928
       ISSP1998: Religion II   2000934
       ISSP1999: Social Inequality III 2000937
       ISSP2000: Environment II    2000940
       ISSP2001: Social Networks II    2000943
       ISSP2002: Family and Changing Gender Roles III  2000946
       ISSP2003: National Identity II  2000949
       ISSP2004: Citizenship I 2000952
       ISSP2005: Work Orientations III 2000955
       ISSP2006: Role of Government IV 2000958
       ISSP2007: Leisure Time and Sports I 2000961
       ISSP2008: Religion III  2000964
       ISSP2009: Social Inequality IV  2000967
       ISSP2010: Environment III   2000970

-  then, remove and re-add all articles (at the moment, adding more than
   10 elements doesn't work, so you'll have to do that in batches)

   .. code:: example

       pigshare remove_article --collection 2118 2000970 2000967 2000964 2000961 2000958 2000955 2000952 2000949 2000946 2000943 2000940 2000937 2000934 2000928 2000925 2000922 2000919 2000916 2000913 2000910
       for id in 2000910 2000913 2000916 2000919 2000922 2000925 2000928 2000934 2000937 2000940 2000943 2000946 2000949 2000952 2000955 2000958 2000961 2000964 2000967 2000970 2001483; do pigshare add_article --id 2118 "$id"; done

-  the, publish the collection

   .. code:: example

       pigshare publish_collection 2118

-  check the webfrontend whether it worked by refreshing the collections
   page

Be aware that if an article got a new version since it was added to a
collection, the old version of the article is included in it. If you
want the new version, you need to manually remove and re-add the article
before you do anything else.

Other random example calls:
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: example

    # create new collection
    pigshare create_collection --collection '{"title": "Collection markus test", "articles": [2009074,2009075,2009084], "custom_fields": {"test1": "value1"}}'

.. code:: example

    # add articles to a collection
    pigshare add_article --id 2761 --article_ids [2009103,2009106]

.. code:: example

    # search all my articles that contain a search_term, display only ids, separated by ',' (useful to copy and paste into 'add_article' command)
    pigshare -o id -s ',' search_my_articles --search_term [search_term]

.. code:: example

    # list all of your personal articles, and add all of them to a collection
    for id in `pigshare -o id list_my_articles`; do echo "$id"; pigshare add_article --collection_id 3222 --article_id "$id"; done

.. code:: example

    # update/overwrite the title and articles connected to a collection
    pigshare update_collection --id 2761 --collection '{"title": "Collection markus test changed", "articles": [2009074,2009075]}'

.. code:: example

    # update/overwrite the categories field in a collection
    pigshare update_article --id 2000077 --article '{"categories": [2]}'

.. code:: example

    # update/overwrite the custom_fields of a collection
    pigshare update_article --id 2000077 --article '{"custom_fields": {"field1":"value1"}}'

Usage (Library)
---------------

Create your python project, e.g. using
`cookiecutter <https://github.com/audreyr/cookiecutter>`__:

.. code:: example

    cookiecutter https://github.com/audreyr/cookiecutter-pypackage

Create a virtualenv:

.. code:: example

    cd <project_dir>
    mkvirtualenv pigshare_example

Edit *setup.py* to include pigshare requirement:

.. code:: example

    requirements = [
        "pigshare"
    ]

Setup dev environment:

.. code:: example

    python setup.py develop

Write your code (depending on which methods you intend to use you'll
have to include auth token or not), e.g.:

.. code:: example

    # -*- coding: utf-8 -*-
    from pigshare.api import figshare_api
    api = figshare_api(url="https://api.figshare.com/v2", token="xxx")
    result = api.call_list_my_articles()
    print result

Run your code

.. code:: example

    python pigshare_example/pigshare_example.py
