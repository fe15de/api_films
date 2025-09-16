import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

import re

#-------------------------------------------------------------------------------------------------------------
#   Filter of the showtimes by date 
#   <div class="column is-12">
#   date-filter :is-loading="isLoading" @change="dateChanged" first-function-date="2025-09-10"></date-filter>
#   </div>
#-------------------------------------------------------------------------------------------------------------
def all_films(city):
    #city = input('City to search films in Cine Colombia: ')
    URL = f"https://www.cinecolombia.com/{city}/cartelera"
    response = requests.get(URL)


    soup = BeautifulSoup(response.text, "html.parser")

    #-------------------------------------------------------
    # Get only the films on theaters 
    #-------------------------------------------------------
    all_films = soup.select(".movie-item")
    films_map= {}


    for film in all_films:
        name = film.select_one('.movie-item__title').get_text(strip=True)
    #---------------------------------------------------------------------
    #   fix name so that can the function time can be searched by name
    #---------------------------------------------------------------------
        url_name = re.sub(r'[:\s-]+', '-', name)
        films_map[name] = url_name

    return films_map


def search_film(films_map,film,city):
    #film_name = input('Name of the Film you want to know show times: ')
    url_name = films_map[film].url_name
    search_time_functions = f'https://www.cinecolombia.com/{city}/peliculas/{url_name}'

    #---------------------------------------------------------------------
    #    since the show times and locations load with a js file, 
    #   it has to wait to the content to load so i had to use selenium 
    #---------------------------------------------------------------------

    firefox_options= Options()
    firefox_options.add_argument("--headless")


    driver = webdriver.Firefox(options=firefox_options)
    driver.get(search_time_functions)

    try:
        locations = {}
        element = WebDriverWait(driver,1).until(EC.presence_of_element_located((By.CLASS_NAME,'show-times-collapse__title')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        malls = soup.select('.show-times-collapse__title')
        times = soup.select('.show-times-group__times')
    
        for idx,place in enumerate(malls):
            place = place.get_text(strip=True)
            time = re.sub(r'(AM|PM)(?!\s)', r'\1 ', times[idx].get_text(strip=True))
            print(f'{place}\nHorarios: {time}')
            locations[place] = time


    finally:
        driver.quit()
        return locations