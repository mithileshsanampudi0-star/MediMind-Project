from database.mongo import MongoDB
from werkzeug.security import generate_password_hash, check_password_hash
from utils.helpers import current_timestamp


class UserModel:

    def create_user(self, username, email, password):

        users = MongoDB.users_collection()

        if users.find_one({"email": email}):
            return {"success": False, "message": "Email already exists"}

        hashed_password = generate_password_hash(password)

        users.insert_one({
            "username": username,
            "email": email,
            "password": hashed_password,
            "created_at": current_timestamp()
        })

        return {"success": True, "message": "User created successfully"}

    def authenticate_user(self, email, password):

        users = MongoDB.users_collection()

        user = users.find_one({"email": email})

        if not user:
            return None

        if check_password_hash(user["password"], password):
            return user

        return None


user_model = UserModel()