from dict_theaters import *
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
import re,unicodedata
from  theaters_search.theaters.class_theaters import Theater

class Cinemark(Theater):
    def __init__(self):
        super().__init__('cinemark')

    def get_films(self, city):
        url = theaters_url[self.name][0].format(city=city)
    
        firefox_options= Options()
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(options=firefox_options)
        driver.get(url)

        #-------------------------------------------------------
        #               Wait javascript to load
        #-------------------------------------------------------

        WebDriverWait(driver,1).until(EC.presence_of_element_located((By.CLASS_NAME,'billboard-movies')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        driver.quit()
        section = soup.find("section", class_="billboard-movies")
        
        cards = section.find_all("div", class_="grid-movie__card")
        for card in cards:
            name = card.find("h3", class_="info-movie__title-movie")
            name = name.text.strip()
            name = unicodedata.normalize("NFD", name)
            name = "".join(ch for ch in name if unicodedata.category(ch) != "Mn")
            name = name.replace("‘", "").replace("’", "").replace("“", '').replace("”", '')
            
            url_name = re.sub(r'[:\s-]+', '-', name)
            self.films[name] = url_name
    

    def search_showtimes_film(self, films, film, city):
        url_names = films[film]#.url_name
        url_name = self.verify(url_names)
        
        if not url_name:
            return False
        url = theaters_url[self.name][1].format(city=city,url_name=url_name)

        # TODO : 
        #       - Finish this
        #       - do cinepolis and royal
        #       - integrate all this with whatsapp


    
