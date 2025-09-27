from dict_theaters import *
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re,unicodedata,requests,json
from datetime import date
from  theaters_search.theaters.class_theaters import Theater

class Cinemark(Theater):
    def __init__(self):
        super().__init__('cinemark')

    def get_films(self, city):

        url = theaters_url[self.name][0].format(city=city)
        driver = self.get_driver(url)
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
        resp = requests.get(url)
        soup = BeautifulSoup(resp.text, "html.parser")
        #--------------------------------------------------------------------------
        #                   Get id of the film to get showtimes
        # -------------------------------------------------------------------------

        script = soup.find("script", {"id": "__NEXT_DATA__"})
        data = json.loads(script.string)
        movie = data["props"]["pageProps"]["movie"]
        film_id = movie["CorporateFilmId"]
        today_date = date.today().strftime("%Y-%m-%d")
        url = f"https://api.cinemark-core.com/vista/country/co/city/{city}/movie/{film_id}?date={today_date}&companyId=5db771be04daec00076df3f5&midnightSessionStart=22&midnightSessionEnd=02"
        headers = {
            "connectapitoken": "a"
        }
        resp = requests.get(url,headers=headers)
        data = resp.json()

        for theater in data["Theater"]:
            print(f"\n{theater['Name']} - {theater['Address1']}")
            for fmt in theater["Format"]:
                for session in fmt["Sessions"]:
                    if session["IsVisible"]:
                        print(f"  {session['Showtime']} {session['SeatsAvailable']} asientos")


    
