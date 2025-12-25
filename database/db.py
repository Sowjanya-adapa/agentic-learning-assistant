from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = MongoClient(MONGO_URI)
db = client["agentic_learning"]

# Collections
learning_history_collection = db["learning_history"]
bkt_states_collection = db["bkt_states"]
analytics_collection = db["analytics"]

def check_db_connection():
    try:
        client.admin.command("ping")
        return True
    except Exception:
        return False
