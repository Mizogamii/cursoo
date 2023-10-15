from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
class DataBase:
    def __init__():
        load_dotenv()

    def connect(self):
        client = MongoClient(os.getenv('DB_URI'))
        dB = client['news']
        return dB.news
    