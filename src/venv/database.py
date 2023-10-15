from pymongo.mongo_client import MongoClient
from dotenv import load_dotenv
import os

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
        
    def insert(self, data: dict)-> dict | None:
        query = {'title': data['title']}
        resultado = self.news.find(query).sort('date', -1)

        if resultado is None:
            self.news.insert_one(data)
            print("O outro")
            return data
        else:
            news = data.copy()
            print("Testando")
            return news
        
if __name__ == "__main__":
    db = DataBase()
    data = {'title': 'Assista ao trailer do filme "Priscilla', 'texto': 'Drama de Sofia Coppola, com Cailee Spaeny, Jacob Elordi, Ari Cohen e Dagmara Dominczyk.'}
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