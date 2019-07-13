"""
Generates the number of papers per year, per venue for a set of search terms.

Usage:
  analysis.hits_per_venue_per_year.py <bibfile>...
"""

import bib_utils


table_str = '''\\begin{{table}}[ht]
\\begin{{tabular}}{{{}}}
{}\\\\
{}
\\hline
\\end{{tabular}}
\\end{{table}}'''


def make_series_dict(bib):
    '''(BibDatabase) -> Dict[str: BibEntry]
    Return a dictionary that maps series to the papers from that series.
    '''
    series_d = {}
    for entry in bib.entries_dict.values():
        series_d.setdefault(bib_utils.get_series_field(entry), []).append(entry)
    return series_d


def gen_venue_occurrence_table(bib):
    '''(BibDatabase) -> None
    Print a latex table that displays the number of occurrences of papers at a venue.
    '''
    format_str = 'llrr'
    header_str = 'Venue & Series & Occurrences & Total'

    venues = bib_utils.get_venues(merged_bib)
    series_d = make_series_dict(bib)

    body_list = []
    for venue in venues:
        venue_list = []
        related_series = sorted([series for series in series_d.keys() if series.startswith(venue)])

        total_occurrences = 0
        for series in related_series[1:]:
            total_occurrences += len(series_d[series])
            venue_list.append('& {} & {} &\\\\'.format(series, len(series_d[series])))

        # Fenceposting -- but inserting at front to allow for rowspan
        series = related_series[0]
        total_occurrences += len(series_d[series])
        venue_list.insert(0, '\\hline\n\\multirow{{{}}}{{*}}{{{}}} & {} & {} & \\multirow{{{}}}{{*}}{{{}}}\\\\'\
          .format(len(related_series), venue, series, len(series_d[series]), len(related_series), total_occurrences))

        body_list.extend(venue_list)

    return table_str.format(format_str, header_str, '\n'.join(body_list))


if __name__ == '__main__':
    from docopt import docopt
    arguments = docopt(__doc__)

    bibfiles = arguments.get('<bibfile>')
    bibs = [bib_utils.get_bib(bibfile) for bibfile in bibfiles]     # Burning space!
    merged_bib = bib_utils.merge_bibs(bibs)
    print(gen_venue_occurrence_table(merged_bib))