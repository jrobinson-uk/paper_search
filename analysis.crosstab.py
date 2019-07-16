"""
Generates the 2-d matrix of theories and identifies when a paper references both.

Usage:
  analysis.crosstab.py <type>
"""

import bib_utils
import os
import sys
from collections import OrderedDict

OUTPUT_FOLDER = 'TABLES'
TERMS_FILE = 'theories-terms.csv'


table_str = '''\\begin{{table*}}[t]
\\begin{{tabular}}{{{}}}
{}\\\\\\hline
{}
\\end{{tabular}}
\\caption{{Cross-tab of theories, identifying when a paper references two theories.}}
\\end{{table*}}'''


def gen_crosstab(theory_terms_d, typ):
    '''(Dict[str: str], str) -> str
    Return a latex table that represents the crosstab of theories.
    '''

    theory_bibs_d = OrderedDict()
    counter = 1
    for (theory, terms) in theory_terms_d.items():
        try:
            bibs = [bib_utils.get_bib(os.sep.join([typ, '{},{}.bib'.format(theory, term)])) for term in terms]     # Burning space!
            bib = bib_utils.merge_bibs(bibs)
            venues = bib_utils.get_venues(bib)   # Just in case we want venues later
            papers = bib_utils.extract_paper_list(bib)

            theory_bibs_d[theory] = (counter, papers, venues)
            counter += 1
        except FileNotFoundError:
            theory_bibs_d[theory] = None

    format_str = 'l' * counter
    header = 'Theory (id) & {}'.format('&'.join([str(i) for i in range(1, counter)]))

    body = []
    for (theory, data) in theory_bibs_d.items():
        if data:
            row = []
            papers = data[1]
            for (theory_compare, comp_data) in theory_bibs_d.items():
                if comp_data:
                    row.append(len(papers.intersection(comp_data[1])))
            row_no_zero = [str(item) if item > 0 else '' for item in row]
            row_no_zero[data[0] - 1] = '-'
            body.append('{} ({}) & {}\\\\'.format(theory, data[0], '&'.join(row_no_zero)))

    return table_str.format(format_str, header, '\n'.join(body))


if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__)
    typ = arguments.get('<type>')

    with open(TERMS_FILE) as f:
        theory_term_d = {}
        for line in f:
            fields = line.strip().split(',')
            if len(fields) != 2:
                print("WARNING: Too many items in the theories-terms file --", line, file=sys.stderr)
                continue
            theory_term_d.setdefault(fields[0], []).append(fields[1])

    output_fname = os.sep.join([OUTPUT_FOLDER, 'SUMMARY.{}-crosstab.tex'.format(typ)])
    open(output_fname, 'w').write(gen_crosstab(theory_term_d, typ))
