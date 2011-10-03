from collections import namedtuple
import os
import sqlite3


EnzymeRow = namedtuple('EnzymeRow',
                       ['id', 'name', 'alt_name', 'catalytic_activity',
                       'cofactors', 'comments', 'prosite_ref', 'db_ref'])


bang_join = lambda l: '-!-'.join(l)
db_ref_join = lambda r: ';'.join(','.join(x for x in item) for item in r)
CONVERT_FUNCS = {
    'id':                   lambda x: x,
    'name':                 bang_join,
    'alt_name':             bang_join,
    'catalytic_activity':   bang_join,
    'cofactors':            bang_join,
    'comments':             bang_join,
    'prosite_ref':          lambda l: ';'.join(l),
    'db_ref':               db_ref_join,
}


bang_split = lambda s: s.split('-!-')
db_ref_split = lambda s: [[x for x in item.split(',')] for item in s.split(';')]
UNCONVERT_FUNCS = {
    'id':                   lambda x: x,
    'name':                 bang_split,
    'alt_name':             bang_split,
    'catalytic_activity':   bang_split,
    'cofactors':            bang_split,
    'comments':             bang_split,
    'prosite_ref':          lambda s: s.split(';'),
    'db_ref':               db_ref_split,
}


def sqlize(data, out):
    if os.path.exists(out):
        os.remove(out)

    conn = sqlite3.connect(out)
    c = conn.cursor()
    c.execute('''create table enzymes
              (id text, name text, alt_name text, catalytic_activity text,
              cofactors text, comments text, prosite_ref text, db_ref text)
              ''')

    for enzyme_dict in data.values():
        c.execute('''insert into enzymes values (?,?,?,?,?,?,?,?)''',
                  EnzymeRow(**{k: CONVERT_FUNCS[k](v)
                               for k, v in enzyme_dict.items()}))

    conn.commit()
    c.close()
    return conn


def desqlize_row(row):
    return {k: UNCONVERT_FUNCS[k](v) for k, v in EnzymeRow(*row)._asdict().items()}
