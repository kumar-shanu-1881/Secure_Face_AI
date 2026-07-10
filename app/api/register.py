# import json
import numpy as np
import cv2
import uuid
from app.core.face_detector import Detect_face
from app.core.get_embedings import get_embedder
from datetime import datetime
from app.db.user_repo import user_repo
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

register_bp = Blueprint("register", __name__)

@register_bp.route("/api/register", methods=["POST"])

def register():

    try:
        
        email=request.form.get('email')
        # check for existing user with the same email
        existing_user = user_repo.get_user_by_email(email)
        if existing_user:
            return jsonify({
                "success": False,
                "message": "Email already exists."
            }), 409 
        
        name=request.form.get('full_name')
        user_id=generate_user_id(name)
        password=request.form.get('password')
        file=request.files['image']

        image = np.frombuffer(file.read(), np.uint8)

        frame = cv2.imdecode(image, cv2.IMREAD_COLOR)

        detector = Detect_face()
        
        result = detector.detect(frame)

        #Hash the password using scrypt for secure storage
        hashed_password = generate_password_hash(password,method="scrypt")

        #Get embeddings of cropped image using the face recognition model
        #convert the image into face embeddings using the face recognition model
        embedder = get_embedder
        # print(type(image))
        embedding = embedder.get_embedding(result['face'])

        user={
            'user_id': user_id,
            'name': name,
            'email': email,
            'password': hashed_password,
            'embedding': embedding.tolist(),  # Convert numpy array to list for JSON serialization
            'created_at': datetime.now().isoformat()  # Store the current timestamp in ISO format
            # 'type is ': type(image)
        }

        # Open a file in write mode ('w') and save the request.form.get(        # with open("output.json", "w", encoding="utf-8") as file:
        #     json.dump(request.form.get( file, indent=4)

        #Save to request.form.get(ase
        user_repo.create_user(user)
        return jsonify({
            "success": True,
            "message": "User registered successfully.",
            "user_id": user_id
        }), 201

    # except Exception as e:
    #     # return jsonify({"error": str(e)}), 400

    #     error_msg = str(e)
    #     print(f"Registration Error: {error_msg}") 
        
    #     # 2. Append the error and timestamp to a physical log file
    #     try:
    #         with open("error_log.txt", "a", encoding="utf-8") as log_file:
    #             timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #             log_file.write(f"[{timestamp}] Registration Crash: {error_msg}\n")
    #     except Exception as log_error:
    #         print(f"Failed to write to log file: {log_error}")

    #     # 3. Send the response back to the JavaScript frontend
    #     return jsonify({"success": False, "message": error_msg}), 400

    
    except Exception as e:
        print(f"Registration Error: {str(e)}") 
        return jsonify({"success": False, "message": str(e)}), 400
    
    

def generate_user_id(name):

    prefix = "".join(name.upper().split())[:4]

    uid = uuid.uuid4().hex[:6].upper()

    return f"{prefix}-{uid}"



