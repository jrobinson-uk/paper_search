"""
Usage:
  bib_utils.py <command> <bibfile>

Available commands: length, first, series, venues
"""

import sys
import bibtexparser
from bibtexparser.bparser import BibTexParser


def get_bib(fname):
    '''(file) -> BibDatabase
    Convert a bibliography file (in latex format) into a bibliographic database.
    '''
    with open(fname) as bibtex_file:
        parser = BibTexParser(common_strings=False)
        bib_database = bibtexparser.load(bibtex_file, parser)
    return bib_database


def get_series(bib):
    '''(BibDatabase) -> Set[str]
    Return a set of the series present within a bibliographic database.
    '''
    # Would be a set comprehension in 3.7
    series = [entry['series'] for entry in bib.entries_dict.values() if 'series' in entry]
    return set(series)


def get_venues(bib):
    '''(BibDatabase) -> Set[str]
    Return a set of venues present within a bibliographic database.
    '''
    series = get_series(bib)
    return set([entry.split('\'')[0].strip() for entry in series])


def merge_bibs(bib_list):
    '''(List[BibDatabase]) -> BibDatabase
    Return a new bibliographic database that combines unique elements from the list of databases.
    '''
    # Horrific hack. Writes the databases into strings, merges them, then reparses.

    bib_strings = [bibtexparser.dumps(bib) for bib in bib_list]
    return bibtexparser.loads('\n'.join(bib_strings))


if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__)

    command = arguments.get('<command>')
    bib = get_bib(arguments.get('<bibfile>'))

    if command == 'length':
        print('Total entries:', len(bib.entries_dict))
    elif command == 'first':
        print(bib.entries[0])
    elif command == 'series':
        print(get_series(bib))
    elif command == 'venues':
        print(get_venues(bib))
    else:
        print(__doc__.strip(), file=sys.stderr)
