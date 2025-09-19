import hashlib, hmac, logging, os, json

from fastapi import FastAPI,HTTPException,Request
from pydantic import BaseModel
from dotenv import load_dotenv
from fastapi.responses import JSONResponse
from security.security import *
from api import * 
from whatsapp import *


load_dotenv()
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
RECIPIENT_WAID = os.getenv("RECIPIENT_WAID")
PHONE_NUMBER_ID = os.getenv("PHONE_NUMBER_ID")
VERSION = os.getenv("VERSION")

APP_ID = os.getenv("APP_ID")
APP_SECRET = os.getenv("APP_SECRET")

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
        raise HTTPException(status_code=404,detail=f"{film_name} not in theaters")

    theaters_times = search_film(films,film_name,city)
    film = films[film_name]
    film.showtimes = theaters_times

    return film 

#-----------------------------------------------------
#  Webhook verification (GET)
# ----------------------------------------------------

@app.get("/webhook")
async def verify(request: Request):
    mode = request.query_params.get("hub.mode")
    token = request.query_params.get("hub.verify_token")
    challenge = request.query_params.get("hub.challenge")

    if mode and token:
        if mode == "subscribe" and token == VERIFY_TOKEN:
            logging.info("WEBHOOK_VERIFIED")
            return int(challenge)#JSONResponse(content=challenge, status_code=200)
        else:
            logging.info("VERIFICATION_FAILED")
            raise HTTPException(status_code=403, detail="Verification failed")
    else:
        logging.info("MISSING_PARAMETER")
        raise HTTPException(status_code=400, detail="Missing parameters")


# ---------------------------------------------------
#  Handle webhook messages (POST)
# ---------------------------------------------------

@app.post("/webhook")
async def webhook_post(request: Request):
    #---------------------------------------------------
    # Catch signature header and validate it  
    #---------------------------------------------------
    signature_header = request.headers.get("X-Hub-Signature-256", "")
    signature = signature_header[7:] if signature_header.startswith("sha256=") else ""
    raw_body = await request.body()
    payload_str = raw_body.decode("utf-8")

    if not validate_signature(payload_str, signature):
        logging.warning("Signature verification failed!")
        raise HTTPException(status_code=403, detail="Invalid signature")

    try:
        body = await request.json()

        value = body.get("entry", [{}])[0].get("changes", [{}])[0].get("value", {})
        
        if "messages" in value:
            message = value["messages"][0]
            sender = message['from']            
            send_whatsapp_message(sender)

    except json.JSONDecodeError:
        logging.error("Failed to decode JSON")
        return JSONResponse(
            {"status": "error", "message": "Invalid JSON provided"}, status_code=400
        )
#.