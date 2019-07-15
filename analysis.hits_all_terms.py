"""
Generates the number of papers for all search terms.

Usage:
  analysis.hits_all_terms.py [--merge]
"""

import bib_utils
import os
import sys

OUTPUT_FOLDER = 'TABLES'
TERMS_FILE = 'theories-terms.csv'


table_str = '''\\begin{{table*}}[t]
\\begin{{tabular}}{{{}}}
{}\\\\\\hline
{}
\\end{{tabular}}
\\caption{{Occurrences of papers for particular search terms. For each search term, the top 3 venues with at least 5 papers are listed.}}
\\end{{table*}}'''


def line_per_search(theory, terms):
    '''(str, List[str]) -> List[str]
    Generate a row of data for each term in the list of search strings terms. Return a list containing the rows generated.
    '''
    body_list = []
    for term in terms:
        try:
            bib = bib_utils.get_bib(os.sep.join(['ALL', '{},{}.bib'.format(theory, term)]))
            occurrences = len(bib.entries_dict)

            venue_counts = bib_utils.get_venue_counts(bib)
            venue_counts = venue_counts[: min(3, len(venue_counts))]
            top_venues = '; '.join(['{} ({})'.format(*venue) for venue in venue_counts if venue[1] > 5])
        except FileNotFoundError:
            occurrences = 'Running'
            top_venues = '...'

        try:
            bib = bib_utils.get_bib(os.sep.join(['CSE', '{},{}.bib'.format(theory, term)]))
            cs_occurrences = len(bib.entries_dict)
        except FileNotFoundError:
            cs_occurrences = 'Running'

        body_list.append('{} & {} & {} & {} & {} \\\\'.format(theory, term, occurrences, cs_occurrences, top_venues))
    return body_list


def line_per_theory(theory, terms):
    '''(str, List[str]) -> str
    Generate a row of data for the theory. Return a string containing that data.
    '''
    try:
        bibs = [bib_utils.get_bib(os.sep.join(['ALL', '{},{}.bib'.format(theory, term)])) for term in terms]     # Burning space!
        bib = bib_utils.merge_bibs(bibs)
        occurrences = len(bib.entries_dict)

        venue_counts = bib_utils.get_venue_counts(bib)
        venue_counts = venue_counts[: min(3, len(venue_counts))]
        top_venues = '; '.join(['{} ({})'.format(*venue) for venue in venue_counts if venue[1] > 5])
    except FileNotFoundError:
        occurrences = 'Running'
        top_venues = '...'

    try:
        bibs = [bib_utils.get_bib(os.sep.join(['CSE', '{},{}.bib'.format(theory, term)])) for term in terms]
        bib = bib_utils.merge_bibs(bibs)
        cs_occurrences = len(bib.entries_dict)
    except FileNotFoundError:
        cs_occurrences = 'Running'

    return '{} & {} & {} & {} \\\\'.format(theory, occurrences, cs_occurrences, top_venues)


def gen_term_count_table(theory_terms_d, merge):
    '''(Dict[str: str], bool) -> None
    Return a latex table that displays the number of occurrences of papers for a specific term. Rows with the same
    theory are merged.
    '''
    if merge:
        format_str = 'lrrp{6cm}'
        header_str = '& Total & CSEd & \\\\Theory & Occurrences & Occurrences & Main venues'
    else: # Not merged ...
        format_str = 'lp{6cm}rrp{3cm}'
        header_str = '& & Total & CSEd & \\\\Theory & Search Term & Occurrences & Occurrences & Main venues'

    body_list = []
    for (theory, terms) in theory_terms_d.items():
        print("{}...".format(theory))
        if merge:
            body_list.append(line_per_theory(theory, terms))
        else: # not merged ...
            body_list.extend(line_per_search(theory, terms))

    return table_str.format(format_str, header_str, '\n'.join(body_list)).replace('_', '\\_')


if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__)
    merge = arguments.get('--merge', False)

    with open(TERMS_FILE) as f:
        theory_term_d = {}
        for line in f:
            fields = line.strip().split(',')
            if len(fields) != 2:
                print("WARNING: Too many items in the theories-terms file --", line, file=sys.stderr)
                continue
            theory_term_d.setdefault(fields[0], []).append(fields[1])

    output_fname = os.sep.join([OUTPUT_FOLDER, 'SUMMARY.hits_all_terms.tex'])
    open(output_fname, 'w').write(gen_term_count_table(theory_term_d, merge))
