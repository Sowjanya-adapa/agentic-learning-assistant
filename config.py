import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DATABASE_NAME = "agentic_learning_db"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", None)
