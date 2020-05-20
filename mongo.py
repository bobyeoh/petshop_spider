from pymongo import MongoClient


def get_mongo_db_client(mongo_url, max_pool_size=20):
    return MongoClient(mongo_url, connect=True, maxPoolSize=max_pool_size)
