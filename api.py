import requests
from bs4 import BeautifulSoup

URL = "https://www.cinecolombia.com/bogota/cartelera"
response = requests.get(URL)

soup = BeautifulSoup(response.text, "html.parser")

#GET ONLY THE CONTAINERS OF FILMS
all = soup.select(".movie-item")

for film in all:
    #GET ORIGINAL NAME OF FILM 
    print(film.select_one('.movie-item__title').get_text(strip=True))

