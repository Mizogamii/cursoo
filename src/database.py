from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os
from bson import ObjectId


class DataBase:
    def __init__(self):
        load_dotenv()
        self.news = self.connect()
        print("Init")

    def connect(self):
        client = MongoClient(os.getenv('DB_URI'))
        db = client['curso']
        print("Connect")
        return db.news
        
    def insert(self, data: dict) -> dict | None:
        query = {'title': data['title']}
        result = self.news.find_one(query, sort=[('date', -1)])
        print("Teste")
        if result is None:
            print("Inserida com sucesso")
            return self.news.insert_one(data)
        else:
            print("Conteúdo encontrado")
            return None       
    
if __name__ == "__main__":
    db = DataBase()
    data = {'title': 'Assista ao trailer do filme "Priscilla', 'texto': 'Drama de Sofia Coppola, com Cailee Spaeny, Jacob Elordi, Ari Cohen e Dagmara Dominczyk.', 'date' : '13:58'}
    db.insert(data)
    print("name___")

"""if __name__ == "__main__":
    db = DataBase()
    data = {'title': 'Assista ao trailer do filme "Priscilla', 'texto': 'Drama de Sofia Coppola, com Cailee Spaeny, Jacob Elordi, Ari Cohen e Dagmara Dominczyk.'}
    
    inserted_data = db.insert(data)

    if inserted_data:
        print("Inserção bem-sucedida!")
        # Agora, você pode consultar o documento inserido para verificar
        query = {'title': inserted_data['title']}
        result = db.news.find_one(query)
        if result:
            print("Documento encontrado:")
            print(result)
        else:
            print("Documento não encontrado.")
    else:
        print("Inserção falhou.")
"""