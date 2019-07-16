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

    alignment = 'll'
    header = 'Venue & Search Terms'
    venues = [venue for venue in open(arguments.get('<venue_file>')).read().split('\n') if venue.strip()]

    body = []
    for venue in venues:
        fields = venue.split(',')
        fields[0].strip('"')
        body.append('{} & {}'.format(fields[0], fields[1]))
        for search_str in fields[2:]:
            body.append('& {}'.format(search_str))
    body = '\\\\\n'.join(body)

    open(os.sep.join([OUTPUT_FOLDER, 'search_venues.tex']), 'w')\
      .write(table_str.format(alignment, header, body))