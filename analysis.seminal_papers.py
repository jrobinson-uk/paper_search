"""
Tableizes the data in the seminal papers CSV.

Usage:
  analysis.seminal_paper.py <papers.csv> <citations.csv>
"""

import os
import csv

OUTPUT_FOLDER = 'TABLES'
title_ind = 0
test_ind = 6
venues = ['TOCE', 'Koli', 'ICER', 'SIGCSE', 'ITiCSE', 'ACE']
counts_inds = [9, 11, 13, 15, 17, 19]
total_ind = 20

theory_ind = 0
theory_title_ind = 2

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
        for fields in reader:
            title = fields[theory_title_ind]
            title = title[title.find('{') + 1: title.find('}')]
            theory_d[title] = fields[theory_ind]

    # Emitting a line for each paper
    fname = arguments.get('<citations.csv>')
    with open(fname) as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')

        alignment = 'p{{3cm}}p{{7cm}}{}l'.format('l' * len(counts_inds))
        header = next(reader)
        header_str = '&'.join(['Theory', 'Paper'] + venues + ['Total'])

        body = []
        for fields in reader:
            if fields[test_ind]:
                counts_str = ' & '.join([fields[ind] for ind in counts_inds])
                title = fields[title_ind]
                title = title[title.find('{') + 1: title.rfind('}')]
                body.append('{} & \\textit{{{}}} & {} & {}\\\\'.format(theory_d.get(title, '???'), title.strip('.'), counts_str, fields[total_ind]))
        body_str = '\n'.join(body)


    table = table_str.format(alignment, header_str, body_str)
    open(os.sep.join([OUTPUT_FOLDER, 'SUMMARY.seminal_papers.tex']), 'w').write(table)