#!/usr/bin/python3

import argparse
from collections import OrderedDict
import sqlite3


from parse import (parse_string, parse_period_concat, parse_bang_concat,
                   parse_prosite, parse_semicolon)


PARSE_FUNCS = {
    'ID': parse_string,
    'DE': parse_period_concat,
    'AN': parse_period_concat,
    'CA': parse_period_concat,
    'CF': parse_period_concat,
    'CC': parse_bang_concat,
    'PR': parse_prosite,
    'DR': parse_semicolon,
}


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


def sqlize(data, out):
    print(data)


def make_parser():
    parser = argparse.ArgumentParser(description='Convert an enzyme.dat file to'
                                     ' a sqlite3 database')
    parser.add_argument('enzyme_dat')
    parser.add_argument('-o', '--out', default='enzyme.sqlite',
                        help='path to output file')
    return parser


def main():
    args = make_parser().parse_args()
    with open(args.enzyme_dat, 'r') as f:
        sqlize(parse(f), args.out)


if __name__ == '__main__':
    main()
