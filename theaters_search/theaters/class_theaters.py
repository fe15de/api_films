from selenium.webdriver.firefox.options import Options
from selenium import webdriver
from abc import ABC, abstractmethod

class Theater(ABC):
    def __init__(self, name):
        self.name = name
        self.films = {}
        self.locations = {}

    #-------------------------------------------------------
    #          Get only the films on theaters 
    #-------------------------------------------------------
    @abstractmethod
    def get_films(self, city):
        pass

    #-------------------------------------------------------
    #           Get locations and showtimes 
    #-------------------------------------------------------
    @abstractmethod
    def search_showtimes_film(self, films,film, city):
        pass

    def verify(self,url_names):
        #----------------------------------------------
        #       url_names has to be a list
        #----------------------------------------------
        for url_name in url_names:
            if url_name in self.films.values():
                return url_name
            
        return False
    
    def get_driver(self,url):
        firefox_options= Options()
        firefox_options.add_argument("--headless")
        driver = webdriver.Firefox(options=firefox_options)
        driver.get(url)

        return driver