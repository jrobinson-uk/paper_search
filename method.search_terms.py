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
    for (theory, search_strings) in theory_d:
        body.append('{} & {}'.format(theory, search_strings[0]))
        for search_str in v[1:]:
            body.append(' & {}'.format(search_str))
    body = '\\\\\n'.join(body)

    open(os.sep.join([OUTPUT_FOLDER, 'search_terms.tex']), 'w')\
      .write(table_str.format(alignment, header, body))