#Importando bibliotecas
import requests 
from bs4 import BeautifulSoup 

#Link dos sites:
#1 https://g1.globo.com/pop-arte/cinema/
#2 https://www.adorocinema.com/noticias/filmes/cat-23201/

class Crawler:
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
                'texto': texto
            }

            print(data)
            
    #extraindo informações do site Adoro Cinema
    def extract_from_aCinema(self):
        raw_aCinema = self.request_data('https://www.adorocinema.com/noticias/filmes/cat-23201/')
        news = raw_aCinema.find_all('div', {'class':"gd-col-left"})
    
        for newsN in news:
            #Título da notícia
            title = newsN.find('h2', {'class': "meta-title"}).text
            #Texto que acompanha a notícia
            texto = newsN.find('div', {'class': "meta-body"}).text
            
            data = {
                'title': title,
                'texto': texto
            }

            print(data)
                
if __name__ == "__main__":
    crawler = Crawler()
    crawler.extract_from_g1()
    crawler.extract_from_aCinema()