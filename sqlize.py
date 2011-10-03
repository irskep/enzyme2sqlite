from collections import namedtuple
import os
import sqlite3


EnzymeRow = namedtuple('EnzymeRow',
                       ['id', 'name', 'alt_name', 'catalytic_activity',
                       'cofactors', 'comments', 'prosite_ref', 'db_ref'])


identity = lambda x: x
string_join = lambda l: '-!-'.join(l)
db_ref_join = lambda r: ';'.join(','.join(x for x in item) for item in r)
CONVERT_FUNCS = {
    'id':                   identity,
    'name':                 string_join,
    'alt_name':             string_join,
    'catalytic_activity':   string_join,
    'cofactors':            string_join,
    'comments':             string_join,
    'prosite_ref':          string_join,
    'db_ref':               db_ref_join,
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
