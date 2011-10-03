enzyme2sqlite
=============

This script parses the ENZYME enzyme nomenclature database from the flat file
format to a SQLite database (in my case, to use in an iPad app).

For more information, see the
[ENZYME project home page](http://enzyme.expasy.org/).

Currently, only the parser works. It returns an `OrderedDict` of dictionaries
that contain all parsed information normalized into a reasonable structure.
