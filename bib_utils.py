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


def get_series_field(entry):
    '''(BibEntry) -> str
    Get the series or journal field.
    '''
    if 'series' in entry:
        return entry['series']
    elif 'journal' in entry:
        return entry['journal']
    else:
        print('Entry "{}" lacks a series or a journal field'.format(entry['title']), file=sys.stderr)
        return None


def get_series(bib):
    '''(BibDatabase) -> Set[str]
    Return a set of the series (or journals) present within a bibliographic database.
    '''
    # Would be a set comprehension in 3.7
    # !!!Critical that we look at the values off the entries_dict, since entries (the list) contains duplicates
    series = set([get_series_field(entry) for entry in bib.entries_dict.values()])
    series.discard(None)
    return series


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


    print('''WARNING: It is important that any analysis on this merged database operate on the entries_dict since the entries list
contains duplicates. In addition, merging respects bib key, so duplicate entries with different keys (from different
sources or reprints in different venues) will not be identified.''', file=sys.stderr)
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
