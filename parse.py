import re


TRANSFER_RE = re.compile(r'\s+Transferred entry: (?P<entry>.+?)\.$')


def parse_string(old, new):
    # old should probably be None
    #
    # these should be unique, so ignore the old values

    return new.strip() if new else None


def parse_period_concat(old, new):
    # old is a list of strings, new is a string
    #
    # if a line does not end with a period, it sould be concatenated with the
    # next line. Otherwise, keep the list intact.
    #
    # e.g.
    # CA   Peptidylglycine + ascorbate + O(2) = peptidyl(2-hydroxyglycine) +
    # CA   dehydroascorbate + H(2)O.

    processed_lines = old
    line = new.strip()
    if processed_lines and not processed_lines[-1].endswith('.'):
        processed_lines[-1] = '{0} {1}'.format(processed_lines[-1], line)
    else:
        processed_lines.append(line)
    return processed_lines


def parse_bang_concat(old, new):
    # old is a list of strings, new is a string
    # if a line does not begin with '-!-', it should be concatenated with the
    # previous line. Otherwise, keep the list intact.
    #
    # e.g.
    # CC   -!- Peptidylglycines with a neutral amino acid residue in the penultimate
    # CC       position are the best substrates for the enzyme.

    processed_lines = old
    line = new.strip()
    if not line.startswith('-!-') and processed_lines:
        processed_lines[-1] = '{0} {1}'.format(processed_lines[-1], line)
    else:
        if line.startswith('-!- '):
            line = line[4:]
        processed_lines.append(line)
    return processed_lines


def parse_prosite(old, new):
    # old is a list of strings, new is a string
    old.append(new.split(';')[1].strip())
    return old


def parse_semicolon(old, new):
    # old is a list of strings, new is a string
    #
    # e.g.
    # DR   P10480, GCAT_AERHY ;  P53760, LCAT_CHICK ;  O35573, LCAT_ELIQU ;

    for item in new.split(';'):
        pair = [x.strip() for x in item.split(',') if x.strip()]
        if pair:
            old.append(pair)
    return old
