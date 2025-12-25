from pymongo import MongoClient
from config import MONGO_URI, DATABASE_NAME

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# Collections
students_collection = db["students"]
attempts_collection = db["attempts"]
problems_collection = db["problems"]
# BKT collections
bkt_states_collection = db["bkt_states"]
bkt_attempts_collection = db["bkt_attempts"]
# Learning history collection
learning_history_collection = db["learning_history"]

def check_db_connection():
    try:
        client.admin.command("ping")
        return True
    except Exception as e:
        print("DB connection failed:", e)
        return False
