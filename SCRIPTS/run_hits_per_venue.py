"""
Runs the hits_per_venue_per_year analysis on each search term

Usage:
  run_hits_per_venue.py <terms> <dir>
"""

import os


if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__)

    directory = arguments.get('<dir>')
    terms = [term.strip().strip('"').replace('"', '\\"') for term in open(arguments.get('<terms>')).read().split('\n') if term.strip()]
    for term in terms:
        os.system('python3 analysis.hits_per_venue_per_year.py "{}_{}" "{}.bib"'\
                  .format(directory, term, os.sep.join([directory, term])))
