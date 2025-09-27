import requests
from whatsapp.template import *
from api import all_films, search_film
from model.film import Film
from dict_theaters import theaters_by_city

# --------------------------------------------------------------
#                       Send Cities 
# --------------------------------------------------------------
films_by_city = {}

def send_whatsapp_message(sender):
    url, headers,data = list_template()
    data['to'] = sender
    data['interactive']['body']['text'] = 'Please select a city from the following:'
    send_cities = data['interactive']['action']['sections'][0]['rows']
    cities = theaters_by_city.keys()

    for id,city in enumerate(cities,start=1):
        send_cities.append({
                            "id": id,
                            "title": city,
                            })
        if id % 10 == 0:
                requests.post(url, headers=headers, json=data)
                send_cities.clear()
        
    if send_cities:
        requests.post(url, headers=headers, json=data)
                            


    #print(requests.post(url, headers=headers, json=data).text)


#----------------------------------------------------------------------
#               Send Films of the city that was chosen
#----------------------------------------------------------------------
def send_films_theaters(sender,message):

    try:
        
        url, headers,data = list_template()
        data['to'] = sender
        data['interactive']['body']['text'] = 'Please select a film from the following:'
        city = message['interactive']['list_reply']['title']
        #---------------------------------------------------------------------
        #           The goal is to search films once per week 
        #---------------------------------------------------------------------

        if not films_by_city[city]:
            films = films_by_city[city] = all_films(city)
        else:
            films = films_by_city[city]

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
#          Send showtimes of Films in the city that was chosen
#----------------------------------------------------------------------
def send_showtimes(sender,message_sender,city):
    try:
        url, headers,data = text_template()
        data['to'] = sender
        message = data['text']['body']
        film = message_sender['interactive']['list_reply']['description']
        film = films_by_city[city][film]
        #---------------------------------------------------------------------
        #     The goal is to search films showtimes at 00:00 once per day
        #---------------------------------------------------------------------
        
        if not film.showtimes:
            theaters_times =  search_film(films_by_city[city],film,city)
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