from theaters_search.cine_col import films_cine_col,search_film_cine_col
from theaters_search.cinemark import films_cinemark, search_film_cinemark
from remove_duplicates.remove_duplicates import group_similar_films

def all_films(city):
    films = films_cine_col(city)

    return films


def search_film(films_map,film,city):
    locations = search_film_cine_col(films_map,film,city)

    return locations

y = films_cinemark('bogota')
x = films_cine_col('bogota')
""" 
print('CINEMARK',y)
print('CINECOLOMBIA',x) """
films = {**x,**y}
print(group_similar_films(films))