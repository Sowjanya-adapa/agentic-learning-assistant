# database/db.py
import os

USE_DB = os.getenv("USE_DB", "false").lower() == "true"

db = None

if USE_DB:
    from pymongo import MongoClient
    MONGO_URI = os.getenv("MONGO_URI")
    client = MongoClient(MONGO_URI)
    db = client["agentic_learning"]


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
