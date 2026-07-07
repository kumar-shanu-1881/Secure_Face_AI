import numpy as np
import cv2
from flask import Blueprint, request, jsonify
from app.core.face_detector import Detect_face

detect_bp = Blueprint("detect", __name__)

@detect_bp.route("/detect", methods=["POST"])
def detect():

    file = request.files["frame"]

    image = np.frombuffer(file.read(), np.uint8)

    frame = cv2.imdecode(image, cv2.IMREAD_COLOR)

    detector = Detect_face()
    
    result = detector.detect(frame)

    if result["success"]:

        x, y, w, h = result["bbox"]

        return jsonify({

            "success": True,
            
            "face":True,

            "message": result["message"],

            "bbox": [x, y, w, h]

        })

    return jsonify({

        "success": False,
        "face":True,
        "message": result["message"]

    })

