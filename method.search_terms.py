"""
Usage:
  method.search_terms.py <term_file>
"""

import sys
import os


OUTPUT_FOLDER = 'TABLES'

table_str = '''\\begin{{table*}}[t]
\\begin{{tabular}}{{{}}}
{}\\\\\\hline
{}
\\end{{tabular}}
\\caption{{Search terms utilized to find uses of each theory.}}
\\end{{table*}}'''
MAX_LENGTH = 60


if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__)

    with open(arguments.get('<term_file>')) as f:
        theory_d = {}
        for line in f:
            fields = line.strip().split(',')
            if len(fields) != 2:
                print('Incorrect number of fields:', line.strip(), file=sys.stderr)
                continue
            theory_d.setdefault(fields[0], []).append(fields[1])

    alignment = 'll'
    header = 'Theory & Search String(s)'
    body = []
    for (theory, search_strings) in theory_d.items():
        body.append('{} & {}'.format(theory, search_strings[0]))
        for search_str in search_strings[1:]:
            body.append(' & {}'.format(search_str))

    tables = []
    for i in range(0, len(body), MAX_LENGTH):
        tables.append(table_str.format(alignment, header, '\\\\\n'.join(body[i: i + MAX_LENGTH])).replace('_', '\\_'))
    open(os.sep.join([OUTPUT_FOLDER, 'search_terms.tex']), 'w').write('\n\n'.join(tables))