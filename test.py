from app.db.mongodb import users

users.insert_one({
    "name": "Kumar Shanu",
    "email": "kumar@example.com"
})

print("Connected successfully!")