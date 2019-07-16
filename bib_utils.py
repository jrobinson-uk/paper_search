"""
Usage:
  bib_utils.py <command> <bibfile>

Available commands: length, first, series, venues, papers
"""

'''
WARNING: It is important that any analysis on this merged database operate on the entries_dict since the entries list
contains duplicates. In addition, merging respects bib key, so duplicate entries with different keys (from different
sources or reprints in different venues) will not be identified.
'''

import sys
import os
import bibtexparser
from bibtexparser.bparser import BibTexParser


class EmptyBib():
    entries = []
    entries_dict = {}
    strings = []
    preambles = []
    comments = []


def get_bib(fname):
    '''(file) -> BibDatabase
    Convert a bibliography file (in latex format) into a bibliographic database.
    '''
    if os.stat(fname).st_size == 0:    # bibtexparser fails on empty bibs
        return EmptyBib()

    with open(fname) as bibtex_file:
        parser = BibTexParser(common_strings=True)
        bib_database = bibtexparser.load(bibtex_file, parser)

    # !!!Critical that we look at the values off the entries_dict, since entries (the list) contains duplicates
    del_keys = []
    for (k, v) in bib_database.entries_dict.items():
        if 'numpages' not in v:
            if 'pages' in v:
                pages_text = v['pages'].strip('{').strip('}')
                first_number = pages_text.split('--')[0]
                second_number = pages_text.split('--')[-1]
                try:
                    length = float(second_number) - float(first_number)
                except ValueError:    # Usually something like '634--'
                    length = 0
                if length < 0:
                    print('Warning: Page calculation failed with negative', file=sys.stderr)
                else:
                    v['numpages'] = str(length)
        if 'numpages' in v:
            if float(v['numpages']) < 3:    # This gets rid of short papers AND proceedings
                del_keys.append(k)
        else:
            print('Entry "{}" lacks a numpages or pages field.'.format(v.get('title', v.get('id'))), file=sys.stderr)
    for k in del_keys:
        del bib_database.entries_dict[k]

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
    series = set([get_series_field(entry) for entry in bib.entries_dict.values()])
    series.discard(None)
    return series


def generate_venue(series):
    '''(str) -> str
    Converts a series into a venue.
    '''
    return ''.join([ch for ch in series if not(ch == '\'' or ch.isdigit())])


def get_venues(bib):
    '''(BibDatabase) -> Set[str]
    Return a set of venues present within a bibliographic database.
    '''
    series = get_series(bib)
    return set([generate_venue(entry) for entry in series])


def get_venue_counts(bib):
    '''(BibDatabase) -> List[(str, int)]
    Return the list of venues present within the database, with counts of papers from the venue.
    '''
    venue_counts = {}
    for entry in bib.entries_dict.values():
        series = get_series_field(entry)
        if series:
            venue_counts[series] = venue_counts.get(generate_venue(series), 0) + 1
    return sorted(venue_counts.items(), key=lambda x: x[1], reverse=True)


def extract_paper_list(bib):
    '''(BibDatabase) -> Set[(str, int)]
    Return a set of (paper title, pub year) tuples from a bibliographic database.
    '''
    return set([(v['title'], v['year']) for (k, v) in bib.entries_dict.items()])


def merge_bibs(bib_list):
    '''(List[BibDatabase]) -> BibDatabase
    Return a new bibliographic database that combines unique elements from the list of databases.
    '''
    # Horrific hack. Writes the databases into strings, merges them, then reparses.
    bib_string = '\n'.join([bibtexparser.dumps(bib) for bib in bib_list])
    if len(bib_string.strip()) > 0:
        return bibtexparser.loads(bib_string)
    return EmptyBib()


if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__)

    command = arguments.get('<command>')
    bib = get_bib(arguments.get('<bibfile>'))

    if command == 'length':
        print('Total entries:', len(bib.entries_dict))
    elif command == 'first':
        print(bib.entries[0])
    elif command == 'papers':
        print(extract_paper_list(bib))
    elif command == 'series':
        print(get_series(bib))
    elif command == 'venues':
        print(get_venues(bib))
    else:
        print(__doc__.strip(), file=sys.stderr)
