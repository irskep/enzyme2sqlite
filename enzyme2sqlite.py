#!/usr/bin/python3

import argparse

from parse import parse
from sqlize import sqlize


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
