from pymongo import MongoClient, collection


class Database(object):
    client = MongoClient('localhost', 27018)
    DATABASE = None
    
    @staticmethod
    def initialize():
        Database.DATABASE = Database.client["blog"]
       
    @staticmethod 
    def insert(collection, data):
        Database.DATABASE[collection].insert(data)
        
    @staticmethod 
    def find(collection, query):
        return Database.DATABASE[collection].find(query)
        
    @staticmethod 
    def find_one(collection, query):
        return Database.DATABASE[collection].find_one(query)