from pymongo import MongoClient
from flask_bcrypt import Bcrypt
import uuid
from config import MONGO_URI

# Initialize Bcrypt
bcrypt = Bcrypt()

# Connect to MongoDB
client = MongoClient(MONGO_URI)
db = client.get_database()
users_collection = db.users

def add_user(username, password):
    # Generate a unique user_id
    user_id = str(uuid.uuid4())

    # Check if the username already exists
    if users_collection.find_one({"username": username}):
        print("Username already exists!")
        return

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Create the user document
    user_doc = {
        "user_id": user_id,
        "username": username,
        "password": hashed_password
    }

    # Insert the user into the collection
    users_collection.insert_one(user_doc)
    print(f"User {username} added with user_id: {user_id}")

if __name__ == "__main__":
    # Example usage
    username = input("Enter username: ")
    password = input("Enter password: ")
    add_user(username, password)