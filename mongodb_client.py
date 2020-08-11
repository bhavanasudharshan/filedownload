from pymongo import MongoClient

__db = MongoClient(host="mongodb")


def get_db():
    return __db['crm']
