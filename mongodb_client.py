from pymongo import MongoClient

__db = MongoClient(host="localhost")


def get_db():
    return __db['crm']
