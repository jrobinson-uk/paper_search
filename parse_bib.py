"""
Usage:
  parse_bib.py <bibfile>
"""


import bibtexparser


if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__)

    with open(arguments.get('<bibfile>')) as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)
    print(bib_database.entries)