from app.db.mongodb import users


class UserRepository:

    @staticmethod
    def create_user(user):
        return users.insert_one(user)

    @staticmethod
    def get_user_by_email(email):
        return users.find_one({"email": email})
    
    @staticmethod
    def get_user_by_user_id(user_id):
        return users.find_one({"user_id": user_id})
    


user_repo = UserRepository()