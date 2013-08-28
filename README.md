Wikipedia Infobox Tool
======================

A tool for getting structured data from the infoboxes of Wikipedia articles. When provided with a category, the tool will parse the infoboxes of the pages within it (and within its subcategories) and save them to the datastore.


Tests
-----

This tool has a handful of tests. You should add more! :-)

You can run the existing tests by running:

```shell
cd wikipedia-infobox-tool
specloud test/*
````

You'll need Python and Specloud installed.


TODO
----

* Give feedback progress during scraping
* Handle timeouts and exceptions
