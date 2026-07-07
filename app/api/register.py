import uuid
from datetime import datetime
from app.db.user_repo import user_repo
from flask import Blueprint, request, jsonify
from app.core.get_embedings import get_embedder
from werkzeug.security import generate_password_hash

register_bp = Blueprint("register", __name__)

register_bp.route("/api/register", methods=["POST"])

def register():

    try:
        data=request.get_json()
        
        email=data['email']
        # check for existing user with the same email
        existing_user = user_repo.get_user_by_email(email)
        if existing_user:
            return jsonify({
                "success": False,
                "message": "Email already exists."
            }), 409 
        
        name=data['full_name']
        user_id=generate_user_id(name)
        password=data['password']
        image=data['image']

        #Hash the password using scrypt for secure storage
        hashed_password = generate_password_hash(password,method="scrypt")

        #Get embeddings of cropped image using the face recognition model
        #convert the image into face embeddings using the face recognition model
        embedder = get_embedder()
        embedding = embedder.get_embedding(image)

        user={
            'user_id': user_id,
            'name': name,
            'email': email,
            'password': hashed_password,
            'embedding': embedding.tolist(),  # Convert numpy array to list for JSON serialization
            'created_at': datetime.now().isoformat()  # Store the current timestamp in ISO format
        }

        #Save to database
        user_repo.create_user(user)
        return jsonify({
            "success": True,
            "message": "User registered successfully.",
            "user_id": user_id
        }), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 400
    

def generate_user_id(name):

    prefix = "".join(name.upper().split())[:4]

    uid = uuid.uuid4().hex[:6].upper()

    return f"{prefix}-{uid}"
