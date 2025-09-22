from abc import ABC, abstractmethod

class Theater(ABC):
    def __init__(self, name):
        self.name = name
        self.films = {}
        self.locations = {}

    @abstractmethod
    def get_films(self, city):
        pass

    @abstractmethod
    def search_showtimes_film(self, films,film, city):
        pass

    def verify(self,url_names):
        #----------------------------------------------
        #   url_names has to be a list
        #----------------------------------------------
        for url_name in url_names:
            if url_name in self.films.values():
                return url_name
            
        return False