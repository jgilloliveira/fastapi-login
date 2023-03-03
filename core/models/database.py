import pymongo

mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")
db = mongo_client["loginTestDb"]
users = db["users"]
tokens = db["tokens"]