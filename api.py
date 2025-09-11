import requests
from bs4 import BeautifulSoup


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

import re

""" 
FILTER DATE SEARCH
<div class="column is-12">
<date-filter :is-loading="isLoading" @change="dateChanged" first-function-date="2025-09-10"></date-filter>
</div>
 """

city = 'bogota'
URL = f"https://www.cinecolombia.com/{city}/cartelera"
response = requests.get(URL)


soup = BeautifulSoup(response.text, "html.parser")


#GET ONLY THE CONTAINERS OF FILMS
all_films = soup.select(".movie-item")
films_map= {}


for film in all_films:
   
    #GET ORIGINAL NAME OF FILM
    name = film.select_one('.movie-item__title').get_text(strip=True)
   
    #fix name so that can the function time can be searched by name
    name_to_search = re.sub(r'[:\s-]+', '-', name)


    films_map[name] = [name_to_search]

for name in films_map.keys():
    print(name)

film_name = input('Name of the Film you want to know show times: ')
search_functions =films_map[film_name][0]


search_time_functions = f'https://www.cinecolombia.com/{city}/peliculas/{search_functions}'

#ads
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