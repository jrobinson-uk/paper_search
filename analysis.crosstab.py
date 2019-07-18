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
\\centering
\\tiny
\\setlength\\tabcolsep{{1.5 pt}}
\\begin{{tabular}}{{{}}}
{}\\\\\\hline
{}
\\end{{tabular}}
\\caption{{Cross-tab of theories, identifying when a paper references two theories. Only theories with at least one point of intersection are listed.}}
\\end{{table*}}'''


def gen_crosstab(theory_terms_d, typ):
    '''(Dict[str: str], str) -> str
    Return a latex table that represents the crosstab of theories.
    '''

    theory_bibs_d = OrderedDict()
    for (theory, terms) in theory_terms_d.items():
        bibs = []
        for term in terms:
            try:
                bibs.append(bib_utils.get_bib(os.sep.join([typ, '{},{}.bib'.format(theory, term)])))
            except FileNotFoundError:
                pass
        bib = bib_utils.merge_bibs(bibs)
        venues = bib_utils.get_venues(bib)   # Just in case we want venues later
        papers = bib_utils.extract_paper_list(bib)

        theory_bibs_d[theory] = (papers, venues)

    body = []
    counter = 1
    to_remove = []
    for (theory, data) in theory_bibs_d.items():
        row = [theory]
        papers = data[0]
        any_data = False
        for (theory_compare, comp_data) in theory_bibs_d.items():
            if theory != theory_compare:
                intersection = len(papers.intersection(comp_data[0]))
                if intersection > 0:
                    any_data = True
                    row.append(str(intersection))
                else:
                    row.append('')
            else:
                row.append('-')
        if not any_data:
            to_remove.append(counter)
        counter += 1
        body.append(row)

    # Removing any rows with no data
    for index in to_remove[::-1]:
        for row in body:
            row.pop(index)
        body.pop(index - 1)

    format_str = 'l' * (len(body) + 1)
    header = 'Theory (id) & {}'.format('&'.join([str(i + 1) for i in range(len(body))]))
    body = ['{} ({}) & {}\\\\'.format(row[0], count + 1, '&'.join(row[1:])) for (count, row) in enumerate(body)]
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
