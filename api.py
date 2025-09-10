import requests
from bs4 import BeautifulSoup

URL = "https://www.cinecolombia.com/bogota/cartelera"
response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")

#GET ONLY THE CONTAINERS OF FILMS
all_films = soup.select(".movie-item")
films_map= {}

for film in all_films:
    
    #GET ORIGINAL NAME OF FILM 
    name = film.select_one('.movie-item__title').get_text(strip=True)
    
    #fix name so that can the function time can be searched by name
    name_to_search = name.replace(' ','-')
    name_to_search = name_to_search.replace(':','-')
    name_to_search = name_to_search.replace('--','-')

    films_map[name] = [name_to_search]

search_functions =films_map['Un Poeta']

search_time_functions = f'https://www.cinecolombia.com/bogota/peliculas/{search_functions}'
response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")

#GET ONLY THE CONTAINERS OF FILMS
idk = soup.select(".show-times-collapse__header")
print(idk)