enzyme2sqlite
=============

This script parses the ENZYME enzyme nomenclature database from the flat file
format to a SQLite database (in my case, to use in an iPad app).

Example usage:

    python3 enzyme2sqlite.py enzyme.dat -o enzyme.sqlite

For more information, see the
[ENZYME project home page](http://enzyme.expasy.org/).

Parser Output
-------------

The `parse()` function returns a dictionary in this format:

    {
        'id': str,
        'names': [str],
        'alt_names': [str],
        'catalytic_activity': [str],
        'cofactors': [str],
        'comments': [str],
        'prosite_refs': [str],
        'db_refs': [[str, str], [str, str], ...],
    }

The name mappings should be obvious, but you can reference `parse.ABBREV_NAMES`
to be sure.

Table Format
------------

Most of the multi-item columns use strings separated by `-!-`. This is because
creating a "proper schema" seemed like overkill for my particular project, and
that is a safe delimiter for their data. So `['A', 'B']` becomes `A-!-B`.

    table enzymes

    id:                     unchanged string
    names:                  strings separated by '-!-'
    alt_names:              strings separated by '-!-'
    catalytic_activity:     strings separated by '-!-'
    cofactors:              strings separated by '-!-'
    comments:               strings separated by '-!-'
    prosite_refs:           strings separated by ';'
    db_refs                 string pairs like 'a,b;c,d;e,f'

Example
-------

This is straight from the tests, where `test_item_1_1_1_2` is alcohol
dehydrogenase (NADP(+)) parsed from `enzyme.dat`:

    from parse import parse
    from sqlize import sqlize, desqlize_row
    with open('enzyme.dat', 'r') as f:
        data = parse(f)
        conn = sqlize(data, ':memory:')
        c = conn.cursor()
        for row in c.execute('select * from enzymes where id=?', ('1.1.1.2',)):
            assert desqlize_row(row) == test_item_1_1_1_2
