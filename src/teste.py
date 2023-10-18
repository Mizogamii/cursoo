import requests
from bs4 import BeautifulSoup
import json
import time
import schedule
from datetime import datetime
from database import DataBase
from dotenv import load_dotenv
import os
#Refiz tudo pra ver se dava certo

#Link dos sites:
#1 https://g1.globo.com/pop-arte/cinema/
#2 https://www.adorocinema.com/noticias/filmes/cat-23201/

class Crawler:
	def __init__(self):
		load_dotenv()
		self.db = DataBase()
	
	def request_data(self, url: str, retry: bool = False) -> BeautifulSoup:
		try:
			response = requests.get(url)
			soup = BeautifulSoup(response.text, 'html.parser')
			return soup
		except Exception as e:
			if not retry:
				time.sleep(3)
				return self.request_data(url, True)
			else:
				raise e

	
		
	def extract_from_g1(self, page: int = 1,retry: bool = False) -> None:
		request = self.request_data('https://g1.globo.com/pop-arte/cinema/')

		newsN = request.find_all('div', {'class': "feed-post-body"})
		if newsN is None:
			if not retry:
				time.sleep(3)
				self.extract_from_g1(retry=True)
		else:
			for news in newsN:
                #Título da notícia
				title = news.find('a', {'class': "feed-post-link gui-color-primary gui-color-hover"}).text

                #Texto que acompanha a notícia
                
				texto = news.find('div', {'class': "feed-post-body-resumo"}).text
                
				data = {
                    'title': title,
                    'texto': texto,
                    'date': datetime.now()
                }

				response = self.db.insert(data)
				
	def extract_from_aCinema(self, page: int = 1, retry: bool = False) -> None:
		request = self.request_data(
            f'https://www.adorocinema.com/noticias/filmes/cat-23201/?page={page}'
            )
		newsN = request.find_all("div", {"class": "s-card-container"})

		if newsN is None:
			if not retry:
				time.sleep(3)
				self.extract_from_aCinema(retry=True)
		else:
			for news in newsN:
				#Título da notícia
				title = newsN.find('h2', {'class': "meta-title"}).text
                #Texto que acompanha a notícia
				texto = newsN.find('div', {'class': "meta-body"}).text
				
				data = {
                    'title': title,
                    'texto': texto,
                    'date': datetime.now()  
                }

				response = self.db.insert(data)

	def execute(self,num_pages: int = 4):
		for page in range(1, num_pages):
			self.extract_from_aCinema(page)
			exit()

if __name__ == "__main__":
    crawler = Crawler()
    crawler.extract_from_g1()
    crawler.execute()
	
def job():
	print("\n Execute job. Time: {}".format(str(datetime.now())))
	crawler.execute()

schedule.every(1).minutes.do(job)

while True:
	schedule.run_pending()