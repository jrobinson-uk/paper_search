"""
Usage:
  bib_utils.py <command> <bibfile>

Available commands: length, first, series, venues
"""

import sys
import bibtexparser
from bibtexparser.bparser import BibTexParser


def get_bibs(fname):
    '''file -> List[bibentry]
    Convert a bibliography file (in latex format) into a list of bibliographic entries.
    '''
    with open(fname) as bibtex_file:
        parser = BibTexParser(common_strings=False)
        bib_database = bibtexparser.load(bibtex_file, parser)
    return bib_database


def get_series(bibentry_list):
    '''List[bibentry] -> Set[str]
    Return a set of the series present within a list of bibliographic entries.
    '''
    # Would be a set comprehension in 3.7
    series = [entry['series'] for entry in bibentry_list.entries if 'series' in entry]
    return set(series)


def get_venues(bibentry_list):
    '''List[bibentry] -> Set[str]
    Return a set of venues present within a list of bibliographic entries.
    '''
    series = get_series(bibentry_list)
    return set([entry.split('\'')[0].strip() for entry in series])


if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__)

    command = arguments.get('<command>')
    bibentry_list = get_bibs(arguments.get('<bibfile>'))

    if command == 'length':
        print('Total entries:', len(bibentry_list.entries))
    elif command == 'first':
        print(bibentry_list.entries[0])
    elif command == 'series':
        print(get_series(bibentry_list))
    elif command == 'venues':
        print(get_venues(bibentry_list))
    else:
        print(__doc__.strip(), file=sys.stderr)
