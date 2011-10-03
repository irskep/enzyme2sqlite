#!/usr/bin/python3

import argparse
from collections import OrderedDict

from parse_funcs import PARSE_FUNCS


ABBREV_NAMES = {
    'ID': 'id',
    'DE': 'name',
    'AN': 'alt_name',
    'CA': 'catalytic_activity',
    'CF': 'cofactors',
    'CC': 'comments',
    'PR': 'prosite_ref',
    'DR': 'db_ref',
}


def enzyme_stub():
    return {
        'id': None,
        'name': [],
        'alt_name': [],
        'catalytic_activity': [],
        'cofactors': [],
        'comments': [],
        'prosite_ref': [],
        'db_ref': [],
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
