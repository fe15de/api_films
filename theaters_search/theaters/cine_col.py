from dict_theaters import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import requests
import re, unicodedata
from theaters_search.theaters.class_theaters import Theater

class CineCol(Theater):
    def __init__(self):
        super().__init__('cine_col')

    def get_films(self, city):
        url = theaters_url[self.name][0].format(city=city)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        all_films = soup.select(".movie-item")


        for film in all_films:
            us_name = film.select_one('.movie-item__title').get_text(strip=True)
            name = film.select_one('.movie-item__meta').get_text(strip=True)

            #---------------------------------------------------------------------------
            #   fixing name so that can the function time can be searched by name
            #--------------------------------------------------------------------------
            
            name = re.sub(r"Título en español:\s*(.+)",r'\1', name)
            name = unicodedata.normalize("NFD", name)
            name = "".join(ch for ch in name if unicodedata.category(ch) != "Mn")
            us_name = us_name.replace("‘", "").replace("’", "").replace("“", '').replace("”", '')
            
            url_name = re.sub(r'[:\s-]+', '-', us_name)
            self.films[name] = url_name
    

    def search_showtimes_film(self,films, film,city):
        url_names = films[film]#.url_name
        url_name = self.verify(url_names)

        if not url_name:
            return False
        
        url = theaters_url[self.name][1].format(city=city,url_name=url_name)
        return url_name

        #---------------------------------------------------------------------
        #       since the show times and locations load with js file, 
        #   it has to wait to the content to load so i had to use selenium 
        #---------------------------------------------------------------------

        firefox_options= Options()
        firefox_options.add_argument("--headless")


        driver = webdriver.Firefox(options=firefox_options)
        driver.get(url)

        try:
            locations = {}
            WebDriverWait(driver,1).until(EC.presence_of_element_located((By.CLASS_NAME,'show-times-collapse__title')))
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



#-------------------------------------------------------------------------------------------------------------
#                                     Filter of the showtimes 
#   <div class="column is-12">
#   date-filter :is-loading="isLoading" @change="dateChanged" first-function-date="2025-09-10"></date-filter>
#   </div>
#
#-------------------------------------------------------------------------------------------------------------
