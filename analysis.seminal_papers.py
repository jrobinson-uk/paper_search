"""
Tableizes the data in the seminal papers CSV.

Usage:
  analysis.seminal_paper.py <papers.csv> <citations.csv>
"""

import os
import csv

OUTPUT_FOLDER = 'TABLES'
title_ind = 3
test_ind = 7
venues = ['TOCE', 'CE', 'ICER', 'SIGCSE', 'ITiCSE', 'Koli', 'ACE']
counts_inds = [10, 12, 16, 18, 20, 14, 22]
total_ind = 23

theory_ind = 0
theory_title_ind = 2
citation_ind = 3

table_str = '''\\begin{{table*}}[t]
\\begin{{tabular}}{{{}}}
{}\\\\\\hline
{}
\\end{{tabular}}
\\caption{{References to key papers in selected CS Education venues, as identified through Google Scholar.}}
\\end{{table*}}'''


if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__)

    # Reading theory - paper mappings
    fname = arguments.get('<papers.csv>')
    with open(fname) as f:
        f.readline()   # garbage
        f.readline()   # header
        reader = csv.reader(f, delimiter=',', quotechar='"')

        theory_d = {}
        citations_d = {}
        citation_text = []
        for fields in reader:
            title = fields[theory_title_ind]
            title = title[title.find('{') + 1: title.rfind('}')]
            theory_d[title] = fields[theory_ind]

            citation_field = fields[citation_ind]
            if '@' in citation_field:
                citation_field = citation_field[citation_field.find('@'):].strip()
                citation_text.append(citation_field)
                citation = citation_text[-1].split(',')[0]
                citations_d[title] = citation[citation.find('{') + 1:]
    open(os.sep.join([OUTPUT_FOLDER, 'seminal.bib']), 'w').write('\n'.join(citation_text))


    # Emitting a line for each paper
    fname = arguments.get('<citations.csv>')
    with open(fname) as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')

        alignment = 'p{{3cm}}p{{6cm}}{}l'.format('l' * len(counts_inds))
        header = next(reader)
        header_str = '&'.join(['Theory', 'Paper'] + venues + ['Total'])

        body = []
        for fields in reader:
            if fields[test_ind]:
                counts_str = ' & '.join([fields[ind] for ind in counts_inds])
                title = fields[title_ind]
                body.append('{} & \\textit{{{}}}~\\cite{{{}}} & {} & {}\\\\'.format(theory_d.get(title, '???'), title.strip('.'), citations_d.get(title, '???'), counts_str, fields[total_ind]))
        body_str = '\n'.join(body)


    table = table_str.format(alignment, header_str, body_str)
    open(os.sep.join([OUTPUT_FOLDER, 'SUMMARY.seminal_papers.tex']), 'w').write(table)