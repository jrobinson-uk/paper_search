"""
Tableizes the data in the seminal papers CSV.

Usage:
  analysis.seminal_paper.py <seminal.csv>
"""

import os
import csv

OUTPUT_FOLDER = 'TABLES'
title_ind = 6
counts_inds = [9, 11, 13, 15, 17, 19]
total_ind = 20

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

    fname = arguments.get('<seminal.csv>')
    with open(fname) as f:
        reader = csv.reader(f, delimiter=',', quotechar='"')

        alignment = 'l{}r'.format('p{2cm}' * len(counts_inds))
        header = next(reader)
        header_str = '&'.join(['Paper'] + [venue for (ind, venue) in enumerate(header) if ind - 1 in counts_inds] + ['Total'])

        body = []
        for fields in reader:
            if fields[title_ind]:
                counts_str = ' & '.join([fields[ind] for ind in counts_inds])
                body.append('{} & {} & {}\\\\'.format(fields[title_ind], counts_str, fields[total_ind]))
        body_str = '\n'.join(body)


    table = table_str.format(alignment, header_str, body_str)
    open(os.sep.join([OUTPUT_FOLDER, 'SUMMARY.seminal_papers.tex']), 'w').write(table)