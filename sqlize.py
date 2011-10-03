from collections import namedtuple
import os
import sqlite3

from parse import (ID, NAMES, ALT_NAMES, CATALYTIC_ACTIVITY, COFACTORS,
                   COMMENTS, PROSITE_REFS, DB_REFS)


EnzymeRow = namedtuple('EnzymeRow',
                       [ID, NAMES, ALT_NAMES, CATALYTIC_ACTIVITY, COFACTORS,
                        COMMENTS, PROSITE_REFS, DB_REFS])


bang_join = lambda l: '-!-'.join(l)
db_ref_join = lambda r: ';'.join(','.join(x for x in item) for item in r)
CONVERT_FUNCS = {
    ID:                     lambda x: x,
    NAMES:                  bang_join,
    ALT_NAMES:              bang_join,
    CATALYTIC_ACTIVITY:     bang_join,
    COFACTORS:              bang_join,
    COMMENTS:               bang_join,
    PROSITE_REFS:           lambda l: ';'.join(l),
    DB_REFS:                db_ref_join,
}


bang_split = lambda s: s.split('-!-')
db_ref_split = lambda s: [[x for x in item.split(',')] for item in s.split(';')]
UNCONVERT_FUNCS = {
    ID:                     lambda x: x,
    NAMES:                  bang_split,
    ALT_NAMES:              bang_split,
    CATALYTIC_ACTIVITY:     bang_split,
    COFACTORS:              bang_split,
    COMMENTS:               bang_split,
    PROSITE_REFS:           lambda s: s.split(';'),
    DB_REFS:                db_ref_split,
}


def sqlize(data, out):
    if os.path.exists(out):
        os.remove(out)

    conn = sqlite3.connect(out)
    c = conn.cursor()
    c.execute('''create table enzymes
              ({ID} text, {NAMES} text, {ALT_NAMES} text, {CATALYTIC_ACTIVITY} text,
              {COFACTORS} text, COMMENTS text, {PROSITE_REFS} text, {DB_REFS} text)
              '''.format(**globals()))

    for enzyme_dict in data.values():
        c.execute('''insert into enzymes values (?,?,?,?,?,?,?,?)''',
                  EnzymeRow(**{k: CONVERT_FUNCS[k](v)
                               for k, v in enzyme_dict.items()}))

    conn.commit()
    c.close()
    return conn


def desqlize_row(row):
    return {k: UNCONVERT_FUNCS[k](v) for k, v in EnzymeRow(*row)._asdict().items()}
