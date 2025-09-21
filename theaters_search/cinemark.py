from dict_theaters import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import requests
import re,unicodedata


def films_cinemark(city):

    url = theaters_url['cinemark'][0].format(city=city)
    
    response = requests.get(url)

    soup = BeautifulSoup(response.text, "html.parser")
    #-------------------------------------------------------
    # Get only the films on theaters 
    #-------------------------------------------------------
    firefox_options= Options()
    firefox_options.add_argument("--headless")
    driver = webdriver.Firefox(options=firefox_options)
    driver.get(url)
    element = WebDriverWait(driver,1).until(EC.presence_of_element_located((By.CLASS_NAME,'billboard-movies')))
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    driver.quit()
    section = soup.find("section", class_="billboard-movies")
    films = {}
    cards = section.find_all("div", class_="grid-movie__card")
    for card in cards:
        name = card.find("h3", class_="info-movie__title-movie")
        name = name.text.strip()
        name = unicodedata.normalize("NFD", name)
        name = "".join(ch for ch in name if unicodedata.category(ch) != "Mn")
        name = name.replace("‘", "'").replace("’", "'").replace("“", '"').replace("”", '"')
        
        url_name = re.sub(r'[:\s-]+', '-', name)
        films[name] = url_name
        #duration = card.find("div", class_="rating-movie")

        """ movie_data = {
            "title": name.text.strip(),
            "duration": duration.find_all("span")[0].text.strip() if duration else None,
            "rating": duration.find_all("span")[-1].text.strip() if duration else None,
        } """

    return films

    
    

    


def search_film_cinemark(films_map,film,city):

    url_name = films_map[film].url_name
    url = theaters_url['cine_col'][1].format(city=city,url_name=url_name)

    #---------------------------------------------------------------------
    #    since the show times and locations load with a js file, 
    #   it has to wait to the content to load so i had to use selenium 
    #---------------------------------------------------------------------

    firefox_options= Options()
    firefox_options.add_argument("--headless")


    driver = webdriver.Firefox(options=firefox_options)
    driver.get(url)

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
    
