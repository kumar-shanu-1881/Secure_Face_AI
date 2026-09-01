import numpy as np
import cv2
import gc
from flask import Blueprint, request, jsonify
from app.core.face_detector import Detect_face
from app.core.anti_spoofing import LivenessDetector

detector = Detect_face()
anti_spoof = LivenessDetector()
detect_bp = Blueprint("detect", __name__)

@detect_bp.route("/detect", methods=["POST"])
def detect():
    file = None
    frame = None

    try:
         
        file = request.files["frame"]

        image = np.frombuffer(file.read(), np.uint8)

        frame = cv2.imdecode(image, cv2.IMREAD_COLOR)

        
        result = detector.detect(frame)

        # add anti spoofing
        is_live = False
        if result["success"]:
            liveness_data = anti_spoof.check_liveness(frame)
            is_live = liveness_data["is_live"]

        del file,image,frame
        file=None
        image=None
        frame=None

        if result["success"] and is_live:

            # x, y, w, h = result["bbox"]

            return jsonify({

                "success": True,
                
                "face":True,

                "message": result["message"],

                # "bbox": [x, y, w, h]

            })
        if result["success"] and not is_live :
            return jsonify({

                "success": False,
                "face":True,
                "message": "Detected face is not live."

            })

        return jsonify({

            "success": False,
            "face":True,
            "message": result["message"]

        })
    except Exception as e:
        print(f"Detection API Crash: {str(e)}")
        return (
            jsonify({"success": False, "face": False, "message": f"Server Error: {str(e)}"}),
            500,
        )

    finally:

            gc.collect()