import scholarly

#print(next(scholarly.search_author('Steven A. Cholewiak')))
search_query = scholarly.search_pubs_query('Laser cooling of atoms')
print(next(search_query))
