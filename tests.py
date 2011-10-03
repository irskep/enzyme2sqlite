from collections import OrderedDict
import tempfile

from enzyme2sqlite import *
from parse import *
from parse_funcs import *
from sqlize import *

# you need this file to run the tests, and probably to run the script as well.
# I got it from here: ftp://ftp.expasy.org/databases/enzyme
DAT_FILE = 'enzyme.dat'

def test_parse_string():
    assert parse_string(None, 'x') == 'x'

def test_period_concat():
    strings = [
        'AAAA     ',
        'AAAAA.   ',
        'BBB.'
    ]
    items = []
    for s in strings:
        items = parse_period_concat(items, s)
    assert items == ['AAAA AAAAA.', 'BBB.']

def test_bang_concat():
    strings = [
        '-!- AAA',
        '    BBB',
        '-!- CCC',
    ]
    items = []
    for s in strings:
        items = parse_bang_concat(items, s)
    assert items == ['AAA BBB', 'CCC']

def test_parse_prosite():
    assert parse_prosite([], 'PROSITE; PDOC00058;') == ['PDOC00058']

def test_parse_semicolon():
    assert (parse_semicolon([], 'P07327, ADH1A_HUMAN;  P28469, ADH1A_MACMU;'
                            '  Q5RBP7, ADH1A_PONAB;')
            == [['P07327', 'ADH1A_HUMAN'],
                ['P28469', 'ADH1A_MACMU'],
                ['Q5RBP7', 'ADH1A_PONAB']])

test_item_1_1_1_2 = {
    'catalytic_activity': ['An alcohol + NADP(+) = an aldehyde + NADPH.'],
    'name': ['Alcohol dehydrogenase (NADP(+)).'],
    'prosite_ref': ['PDOC00061'],
    'db_ref': [['Q6AZW2', 'A1A1A_DANRE'],
               ['Q568L5', 'A1A1B_DANRE'],
               ['P35630', 'ADH1_ENTHI'],
               ['Q24857', 'ADH3_ENTHI'],
               ['Q04894', 'ADH6_YEAST'],
               ['P25377', 'ADH7_YEAST'],
               ['O57380', 'ADH8_RANPE'],
               ['P0CH36', 'ADHC1_MYCS2'],
               ['P0CH37', 'ADHC2_MYCS2'],
               ['P0A4X1', 'ADHC_MYCBO'],
               ['P0A4X0', 'ADHC_MYCTU'],
               ['P25984', 'ADH_CLOBE'],
               ['P75214', 'ADH_MYCPN'],
               ['P14941', 'ADH_THEBR'],
               ['Q3ZCJ2', 'AK1A1_BOVIN'],
               ['Q5ZK84', 'AK1A1_CHICK'],
               ['O70473', 'AK1A1_CRIGR'],
               ['P14550', 'AK1A1_HUMAN'],
               ['Q9JII6', 'AK1A1_MOUSE'],
               ['P50578', 'AK1A1_PIG'],
               ['Q5R5D5', 'AK1A1_PONAB'],
               ['P51635', 'AK1A1_RAT'],
               ['Q6GMC7', 'AK1A1_XENLA'],
               ['Q28FD1', 'AK1A1_XENTR'],
               ['Q9UUN9', 'ALD2_SPOSA'],
               ['P27800', 'ALDX_SPOSA']],
    'cofactors': ['Zinc.'],
    'id': '1.1.1.2',
    'comments': [
        'Some members of this group oxidize only primary alcohols; others act also on secondary alcohols.',
        'May be identical with EC 1.1.1.19, EC 1.1.1.33 and EC 1.1.1.55.',
        'A-specific with respect to NADPH.'],
    'alt_name': ['Aldehyde reductase (NADPH).']
}

def test_all_parsing():
    with open(DAT_FILE, 'r') as f:
        data = parse(f)
        assert data['1.1.1.2'] == test_item_1_1_1_2

def test_sqlize():
    with open(DAT_FILE, 'r') as f:
        data = parse(f)
        conn = sqlize(data, ':memory:')
        c = conn.cursor()
        for row in c.execute('select * from enzymes where id=?', ('1.1.1.2',)):
            assert desqlize_row(row) == test_item_1_1_1_2
