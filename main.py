from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os

from api import * 

load_dotenv()

VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")

app = FastAPI()

class Film(BaseModel):
    url_name : str
    showtimes : dict[str, str]

films = {}
@app.get('/')
def home():
    return ['pereira','bogota','cali']

@app.get('/films')
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

#------------------------------
#  setup whebhook 
#------------------------------

@app.get("/webhook")
def verify_webhook(
    hub_mode: str = None,
    hub_challenge: str = None,
    hub_verify_token: str = None,
):
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:
        return int(hub_challenge)
    raise HTTPException(status_code=403, detail="Invalid verification")
