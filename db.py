from pymongo import MongoClient
import redis
from dotenv import load_dotenv
import os

load_dotenv()

mongo_url = os.getenv("MONGO_URL")

mongo_client = MongoClient(mongo_url)
db = mongo_client["Documents"]
users_collection = db["users"]
documents_collection = db["docs"]

cache = redis.StrictRedis(host="localhost", port=6379, db=0)


def increment_user_requests(user_id):
    user = users_collection.find_one({"user_id": user_id})
    if user:
        users_collection.update_one(
            {"user_id": user_id}, {"$inc": {"request_count": 1}}
        )
    else:
        users_collection.insert_one({"user_id": user_id, "request_count": 1})


def get_user_request_count(user_id):
    user = users_collection.find_one({"user_id": user_id})
    return user["request_count"] if user else 0


def add_document_to_cache(doc_id, document):
    cache.set(doc_id, document)


def get_document_from_cache(doc_id):
    return cache.get(doc_id)
