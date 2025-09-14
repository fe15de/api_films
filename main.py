from fastapi import FastAPI,HTTPException
from pydantic import BaseModel

from api import * 

app = FastAPI()

class Film(BaseModel):
    url_name : str
    showtimes : dict[str, str]

films = {}

@app.get('/')
def get_films(city : str):
    all = all_films(city)
    
    for film in all:
        films[film] = Film(url_name=all[film],showtimes= {'':''})

    return films


@app.get('/showtimes/{film_name}')
def get_showtimes(film_name : str , city : str):

    if film_name not in films:
        HTTPException(status_code=404,detail=f"{film_name} not in theaters")

    theaters_times = search_film(films,film_name,city)
    film = films[film_name]
    film.showtimes = theaters_times

    return film 
