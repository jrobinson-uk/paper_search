"""
Usage:
  poc.merge_bibs.py <bibfile>...
"""

import bib_utils


if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__)

    bibfiles = arguments.get('<bibfile>')
    bibs = [bib_utils.get_bib(bibfile) for bibfile in bibfiles]     # Burning space!
    merged_bib = bib_utils.merge_bibs(bibs)

    # Proof of concept
    print(len(merged_bib.entries_dict))