import requests
from whatsapp.template import *
from api import all_films, search_film
from model.film import Film


# --------------------------------------------------------------
# GLOBALS
# --------------------------------------------------------------

cities = ['pereira','bogota','cali','medellin']
films_by_city = {}


# --------------------------------------------------------------
# Send a template WhatsApp message
# --------------------------------------------------------------

def send_whatsapp_message(sender):
    url, headers,data = list_template()
    data['to'] = sender
    data['interactive']['body']['text'] = 'Please select a city from the following:'
    send_cities = data['interactive']['action']['sections'][0]['rows']

    for id,city in enumerate(cities):
        send_cities.append({
                            "id": id,
                            "title": city,
                            })
                            


    print(requests.post(url, headers=headers, json=data).text)


#----------------------------------------------------------------------
# Send Films in the city that was chosen
#----------------------------------------------------------------------
def send_films_theaters(sender,message):

    try:
        
        url, headers,data = list_template()
        data['to'] = sender
        data['interactive']['body']['text'] = 'Please select a film from the following:'
        city = message['interactive']['list_reply']['title']
        films = films_by_city[city] = all_films(city)
        
        send_films = data['interactive']['action']['sections'][0]['rows'] 
        print(films)
        for id,film in enumerate(films,start=1):
            
            films_by_city[city][film] = Film(url_name=films[film],showtimes= {'':''})
            send_films.append({
                                "id": id,
                                "title": film[:24],
                                "description" : film,
                                })
            if id % 10 == 0:
                requests.post(url, headers=headers, json=data)
                send_films.clear()
        
        if send_films:
            requests.post(url, headers=headers, json=data)
        
        return city
    
    except Exception as ex:
        print(ex)
    
    

#----------------------------------------------------------------------
# Send showtimes of Films in the city that was chosen
#----------------------------------------------------------------------
def send_showtimes(sender,message_sender,city):
    try:
        url, headers,data = text_template()
        data['to'] = sender
        message = data['text']['body']
        film = message_sender['interactive']['list_reply']['description']
        
        theaters_times =  search_film(films_by_city[city],film,city)
        film = films_by_city[city][film]
        film.showtimes = theaters_times
        locations = film.showtimes
        message = '*SHOWTIMES :*\n'
        
        for id,location in enumerate(locations):
            message += f'*{id+1} - {location}*\n'
            message += f'Times: {locations[location]}\n'
            
        data['text']['body'] = message
            
        requests.post(url, headers=headers, json=data)

    except Exception as ex:
        print(ex)