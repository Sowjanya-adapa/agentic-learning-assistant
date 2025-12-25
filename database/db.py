import os
from typing import Optional

try:
    from pymongo import MongoClient
    from pymongo.errors import ServerSelectionTimeoutError
except ImportError:
    MongoClient = None


class Database:
    def __init__(self):
        self.enabled = False
        self.client = None
        self.db = None
        self.memory_store = []  # fallback

        mongo_uri = os.getenv("MONGO_URI")

        if mongo_uri and MongoClient:
            try:
                self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
                self.client.server_info()  # test connection
                self.db = self.client["agentic_learning"]
                self.enabled = True
                print("✅ MongoDB connected")
            except ServerSelectionTimeoutError:
                print("⚠ MongoDB not reachable, using in-memory store")
        else:
            print("⚠ MongoDB disabled, using in-memory store")

    def save(self, record: dict):
        if self.enabled:
            self.db.history.insert_one(record)
        else:
            self.memory_store.append(record)

    def fetch(self, query: dict):
        if self.enabled:
            return list(self.db.history.find(query, {"_id": 0}))
        return self.memory_store
