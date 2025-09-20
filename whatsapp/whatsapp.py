import requests
from whatsapp.template import *
from api import all_films, search_film


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
        
        for id,film in enumerate(films):
            send_films.append({
                                "id": id,
                                "title": film[:24],
                                })
    
            
        requests.post(url, headers=headers, json=data)
        return city
    
    except Exception as ex:
        print(ex)
    
    

#----------------------------------------------------------------------
# Send showtimes of Films in the city that was chosen
#----------------------------------------------------------------------
def send_showtimes(sender,message,city):

    try:
        url, headers,data = text_template()
        data['to'] = sender
        message = data['text']['body'] = '**Showtimes**\n'
        film = message
        showtimes =  search_film(films_by_city[city],film,city)
        print(showtimes)
        
        """ for id,location in enumerate(showtimes):
            print(location) """
            #message += f'**{id+1} -{location}**'
            
    
            
        requests.post(url, headers=headers, json=data)

    except Exception as ex:
        print(ex)