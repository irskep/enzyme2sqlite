from collections import namedtuple
import os
import sqlite3


EnzymeRow = namedtuple('EnzymeRow',
                       ['id', 'name', 'alt_name', 'catalytic_activity',
                       'cofactors', 'comments', 'prosite_ref', 'db_ref'])


identity = lambda x: x
string_join = lambda l: '-!-'.join(l)
CONVERT_FUNCS = {
    'ID': identity,
    'DE': string_join,
    'AN': string_join,
    'CA': string_join,
    'CF': string_join,
    'CC': string_join,
    'PR': string_join,
    'DR': string_join,
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
        c.execute('''insert into enzymes values (?,?,?,?,?,?,?,?)''', EnzymeRow(**enzyme_dict))

    conn.commit()
    c.close()
