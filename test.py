from app.db.mongodb import users

users.insert_one({
    "name": "Kumar Shanu",
    "email": "kumar@examhai.com"
})

print("Connected successfully!")