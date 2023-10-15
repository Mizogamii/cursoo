#Importando bibliotecas
import requests 
from bs4 import BeautifulSoup 
import schedule
import time #Não tô usando ainda 
from datetime import datetime
from database import DataBase
from dotenv import load_dotenv


#Link dos sites:
#1 https://g1.globo.com/pop-arte/cinema/
#2 https://www.adorocinema.com/noticias/filmes/cat-23201/

class Crawler:
    
    def __init__(self):
	    load_dotenv()
	    self.db = DataBase()
		
    #Solicitando http 
    def request_data(self, url: str, retry=False) -> BeautifulSoup:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup
        except Exception as e:
            if not retry:
                return self.request_data(url, True)
            else:
                raise e
            
    #Extraindo informações do site g1
    def extract_from_g1(self):
        raw_g1 = self.request_data('https://g1.globo.com/pop-arte/cinema/')
        news = raw_g1.find_all('div', {'class': "feed-post-body"})
    
        for newsN in news:
            #Título da notícia
            title = newsN.find('a', {'class': "feed-post-link gui-color-primary gui-color-hover"}).text
            #Texto que acompanha a notícia
            texto = newsN.find('div', {'class': "feed-post-body-resumo"}).text
            
            data = {
                'title': title,
                'texto': texto,
                'date': datetime.now()
            }
            
            #print("\nG1\n", data)

            response = self.db.insert(data)
            
    #extraindo informações do site Adoro Cinema
    def extract_from_aCinema(self, page: int = 1):
        raw_aCinema = self.request_data(
            f'https://www.adorocinema.com/noticias/filmes/cat-23201/?page={page}'
            )
        news = raw_aCinema.find_all('div', {'class': "card news-card news-card-row mdl cf"})
    
        for newsN in news:
            #Título da notícia
            title = newsN.find('h2', {'class': "meta-title"}).text
            #Texto que acompanha a notícia
            texto = newsN.find('div', {'class': "meta-body"}).text
            
            data = {
                'title': title,
                'texto': texto,
                'date': datetime.now()  
            }

            #print("\nAdoro Cinema\n", data)

            response = self.db.insert(data)

    def execute(self,num_pages: int = 4):
        for page in range(1, num_pages):
            self.extract_from_aCinema(page)
                
if __name__ == "__main__":
    crawler = Crawler()
    crawler.extract_from_g1()
    crawler.execute()

    def job():
        print(f"\nExecute Job. Time{str(datetime.now())}")
        crawler.execute()

    schedule.every(2).minutes.do(job)
    while True:
        schedule.run_pending()