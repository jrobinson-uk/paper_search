"""
Usage:
  method.search_venues.py <venue_file>
"""

import sys
import os


OUTPUT_FOLDER = 'TABLES'

table_str = '''\\begin{{table*}}[t]
\\begin{{tabular}}{{{}}}
{}\\\\\\hline
{}
\\end{{tabular}}
\\caption{{Venues searched to identify citations of important papers.}}
\\end{{table*}}'''


if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__)

    alignment = 'l'
    header = 'Venues'
    venues = [venue.strip('"') for venue in open(arguments.get('<venue_file>')).read().split('\n')]
    body = '\\\\\n'.join(venues)

    open(os.sep.join([OUTPUT_FOLDER, 'search_venues.tex']), 'w')\
      .write(table_str.format(alignment, header, body))