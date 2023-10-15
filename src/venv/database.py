from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
class DataBase:
    def __init__(self):
        load_dotenv()
        self.news = self.connect()

    def connect(self):
        client = MongoClient(os.getenv('DB_URI'))
        dB = client['news']
        return dB.news
    
    def insert(self, data: dict):
        query = {'title': data['title']}
        resultado = self.news.find(query).sort('date', -1)
        if resultado == None:
            self.news.insert_one(data)
            return data
        else:
            return None
        
if __name__ == "__main__":
    db = DataBase()
    data = {'title': 'Assista ao trailer do filme "Priscilla', 'texto': 'Drama de Sofia Coppola, com Cailee Spaeny, Jacob Elordi, Ari Cohen e Dagmara Dominczyk.', 'date': '14/10/2023'}
    db.insert(data)