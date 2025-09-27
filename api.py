from theaters_search.theaters.cinemark import Cinemark
from theaters_search.theaters.cine_col import CineCol
from remove_duplicates.remove_duplicates import group_similar_films

def all_films(city):
    pass

def search_film(films_map,film,city):
    pass


""" cinemark = Cinemark()
cinemark.get_films('bogota') """

cine_col = CineCol()
cine_col.get_films('bogota')

cinemark = Cinemark()
cinemark.get_films('bogota')

films = {**cine_col.films,**cinemark.films}
films = group_similar_films(films)

x = cinemark.search_showtimes_film(films,'Demon Slayer: Kimetsu no Yaiba - Castillo infinito','bogota')
print(x)
cine_col.search_showtimes_film(films,'Demon Slayer: Kimetsu no Yaiba - Castillo infinito','bogota')

""" cinemark = films_cinemark('bogota')
cine_col = films_cine_col('bogota')

films = {**cine_col,**cinemark}
films = group_similar_films(films)

print(search_film_cine_col(films,'Un Poeta','pereira'))
print(search_film_cinemark(films,'Un Poeta','pereira')) """
