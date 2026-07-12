import numpy as np 
import cv2
from app.core.face_detector import Detect_face
from app.core.get_embedings import get_embedder
from flask import Blueprint, request, jsonify,render_template
from werkzeug.security import check_password_hash
from app.db.user_repo import user_repo
from app.core.check_similarity import compare_faces

login_bp=Blueprint('login',__name__)
@login_bp.route("api/login",methods=["POST"])

def login():
    try:
        email=request.form.get('email')
        user_exist=True
        # check for user exist or not
        existing_user = user_repo.get_user_by_email(email)
        if not existing_user:
            user_exist=False
            return jsonify({
                "success": False,
                "message": "User not exists.\n Please Register user."
            }), 404
        
        userid=request.form.get('userid')
        # get user data from database
        data=user_repo.get_user_by_user_id(userid)
        
        password=request.form.get('password')

        # check hashed password 
        is_match = check_password_hash(data['password'], password)
        # return the response of wrong password 
        if not is_match:
            return jsonify({
                "success": False,
                "message": "wrong password."
            }), 404

        # get image from form and process the image 
        file=request.files['image']
        image = np.frombuffer(file.read(), np.uint8)
        frame = cv2.imdecode(image, cv2.IMREAD_COLOR)
        detector = Detect_face()
        result = detector.detect(frame)

        #convert the captured web  image into face embeddings using the face recognition model
        embedder = get_embedder
        web_embedding = embedder.get_embedding(result['face']).tolist

        # matching person face
        is_matched,cosine_sim,euclidean_dit=compare_faces(web_embedding,data['embedding'])
        if not is_matched:
            return jsonify({
                "success": False,
                "message":"Face not Matched"
            })
        if is_matched and is_match and user_exist:
            return jsonify({
                "success":True,
                "message":"Face matched"
            })
        
        
        

        
    except Exception as e:
        print(f"Login Error: {str(e)}") 
        return jsonify({"success": False, "message": str(e)}), 400 
