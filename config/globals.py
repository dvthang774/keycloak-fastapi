from dotenv import load_dotenv
import os

load_dotenv()

DB_URI = os.environ.get("MONGO_URI")
DB_NAME = os.environ.get("MONGO_DB_NAME")
MONGO_USERS_COLLECTION = os.getenv('MONGO_USERS_COLLECTION')

