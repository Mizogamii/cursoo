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
    
    def insert(self, date: dict):
        query = {'title': date['title']}
        self.news.find(query).sort('date', -1)