#!/usr/bin/python3

import argparse
from collections import OrderedDict

from parse_funcs import PARSE_FUNCS

ID = 'id'
NAMES = 'names'
ALT_NAMES = 'alt_names'
CATALYTIC_ACTIVITY = 'catalytic_activity'
COFACTORS = 'cofactors'
COMMENTS = 'comments'
PROSITE_REFS = 'prosite_refs'
DB_REFS = 'db_refs'


ABBREV_NAMES = {
    'ID': ID,
    'DE': NAMES,
    'AN': ALT_NAMES,
    'CA': CATALYTIC_ACTIVITY,
    'CF': COFACTORS,
    'CC': COMMENTS,
    'PR': PROSITE_REFS,
    'DR': DB_REFS,
}


def enzyme_stub():
    return {
        ID: None,
        NAMES: [],
        ALT_NAMES: [],
        CATALYTIC_ACTIVITY: [],
        COFACTORS: [],
        COMMENTS: [],
        PROSITE_REFS: [],
        DB_REFS: [],
    }


def interpret_line(enzyme, line_code, line_contents):
    key = ABBREV_NAMES[line_code]
    enzyme[key] = PARSE_FUNCS[line_code](enzyme[key], line_contents)


def parse(f):
    """f should be an iterable of strings.

    Format from ftp://ftp.expasy.org/databases/enzyme/enzuser.txt::

        Characters    Content
        ---------     ----------------------------------------------------------
        1 to 2        Two-character line code. Indicates the type of information
                      contained in the line.
        3 to 5        Blank
        6 up to 78    Data
    """
    all_enzymes = OrderedDict()

    # current_enzyme is a dict and never None.
    current_enzyme = enzyme_stub()

    for line in f:
        line_code = line[0:2]

        if line_code == '//':
            if current_enzyme and current_enzyme['id']:
                all_enzymes[current_enzyme['id']] = current_enzyme
            current_enzyme = enzyme_stub()
        else:
            interpret_line(current_enzyme, line_code, line[5:])

    return all_enzymes
