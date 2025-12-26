from pymongo import MongoClient
import os

MONGO_URI = os.getenv("MONGO_URI")

client = None
db = None

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command("ping")
    db = client["agentic_learning"]
except Exception as e:
    print("MongoDB connection failed:", e)

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
