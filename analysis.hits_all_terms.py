"""
Generates the number of papers for all search terms.

Usage:
  analysis.hits_all_terms.py
"""

import bib_utils
import os

OUTPUT_FOLDER = 'TABLES'
TERMS_FILE = 'theories-terms.csv'


table_str = '''\\begin{{table*}}[t]
\\begin{{tabular}}{{{}}}
{}\\\\\\hline
{}
\\end{{tabular}}
\\caption{{Occurrences of papers for particular search terms. For each search term, the top 3 venues with at least 5 papers are listed.}}
\\end{{table*}}'''


def gen_term_count_table(theory_terms_d):
    '''(Dict[str: str]) -> None
    Print a latex table that displays the number of occurrences of papers for a specific term.
    '''
    format_str = 'p{2cm}p{7cm}rrp{3cm}'
    header_str = '& & Total & CSEd & \\\\Theory & Search Term & Occurrences & Occurrences & Main venues'

    body_list = []
    for (term, theory) in theory_terms_d.items():
        print("{}...".format(term))
        fname = term.strip('"')     # For compatibility with search.py's output files
        try:
            bib = bib_utils.get_bib(os.sep.join(['ALL', '{}.bib'.format(fname)]))
            occurrences = len(bib.entries_dict)

            venue_counts = bib_utils.get_venue_counts(bib)
            venue_counts = venue_counts[: min(3, len(venue_counts))]
            top_venues = '; '.join(['{} ({})'.format(*venue) for venue in venue_counts if venue[1] > 5])
        except FileNotFoundError:
            occurrences = 'Running'
            top_venues = '...'

        try:
            bib = bib_utils.get_bib(os.sep.join(['CSE', '{}.bib'.format(fname)]))
            cs_occurrences = len(bib.entries_dict)
        except FileNotFoundError:
            cs_occurrences = 'Running'

        body_list.append('{} & {} & {} & {} & {} \\\\'.format(theory, term, occurrences, cs_occurrences, top_venues))

    return table_str.format(format_str, header_str, '\n'.join(body_list)).replace('_', '\\_')


if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__)

    with open(TERMS_FILE) as f:
        theory_term_d = {}
        for line in f:
            line = line.strip().split(',')
            if len(line) != 2:
                print("WARNING: Too many items in the theories-terms file", file=sys.stderr)
                continue
            theory_term_d[line[1].strip()] = line[0].strip()

    output_fname = os.sep.join([OUTPUT_FOLDER, 'SUMMARY.hits_all_terms.tex'])
    open(output_fname, 'w').write(gen_term_count_table(theory_term_d))
