import gc
import numpy as np
import cv2
from app.core.face_detector import Detect_face
from app.core.get_embedings import get_embedder
from flask import Blueprint, request, jsonify
from app.core.check_similarity import compare_faces



detector = Detect_face()
#Get embeddings of cropped image using the face recognition model
#convert the image into face embeddings using the face recognition model
embedder = get_embedder

similarity_bp = Blueprint("checksimilarity", __name__)

@similarity_bp.route("/api/checksimilarity", methods=["POST"])

def checksimilarity():
    img1=None
    img2=None
    try:
        img1=request.files['imageA']
        img2=request.files['imageB']

        # for image 1 
        img1 = np.frombuffer(img1.read(), np.uint8)
        
        frame1 = cv2.imdecode(img1, cv2.IMREAD_COLOR)

        result1 = detector.detect(frame1)

            # get embeddings
        embedding1 = embedder.get_embedding(result1['face'])

        # for image 2 
        img2 = np.frombuffer(img2.read(), np.uint8)
        
        frame2 = cv2.imdecode(img2, cv2.IMREAD_COLOR)

        result2 = detector.detect(frame2)
            # get embeddings
        embedding2 = embedder.get_embedding(result2['face'])

        matched,cs_sim,ecd_dit=compare_faces(embedding1,embedding2)
        
        del img1,img2,frame1,frame2,result1,result2,embedding1,embedding2
        img1=None
        img2=None
        frame1=None
        frame2=None
        result1=None
        result2=None
        embedding1=None
        embedding2=None

        results=jsonify({
             "matchVal":matched,
             "distanceVal":ecd_dit,
             "thresholdVal":cs_sim,

        })

        return results
    
    except Exception as e:
            print(f"Registration Error: {str(e)}") 
            return jsonify({"success": False, "message": str(e)}), 400
        
    finally:
        # Force Python to clear the system heap right away before handling the next API caller
        gc.collect()