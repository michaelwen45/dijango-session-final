from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING




class Connection():
    #client = MongoClient('mongodb://localhost:27017/taller4')
    #bd = client.taller4
    client = MongoClient('mongodb://mongouser:pemofra@clusterbigdata57.virtual.uniandes.edu.co/grupo14')
    bd = client.grupo14


    def set_client(self, host, port):
        self.client = MongoClient(host, port)

    def set_database(self, database):
        self.db = self.client[database]
