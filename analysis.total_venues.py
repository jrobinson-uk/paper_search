"""
Generates the number of venues in the entire set.

Usage:
  analysis.total_venues.py <bibfile>...
"""

import bib_utils
import os


if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__)

    bibfiles = arguments.get('<bibfile>')
    bibs = [bib_utils.get_bib(bibfile) for bibfile in bibfiles]     # Burning space!
    merged_bib = bib_utils.merge_bibs(bibs)

    venues = bib_utils.get_venues(merged_bib)
    print(venues)
    print('Total venues:', len(venues))
    print('Total papers:', len(merged_bib.entries_dict))
    print('Total searches:', len(bibfiles))