import pandas as pd
import numpy as np
import cv2
from flask import Flask, request, jsonify
from face_detector import detector

app=Flask(__name__)

@app.route("/detect", methods=["POST"])
def detect():

    file = request.files["frame"]

    image = np.frombuffer(file.read(), np.uint8)

    frame = cv2.imdecode(image, cv2.IMREAD_COLOR)

    result = detector.detect(frame)

    if result["success"]:

        x, y, w, h = result["bbox"]

        return jsonify({

            "success": True,

            "message": result["message"],

            "bbox": [x, y, w, h]

        })

    return jsonify({

        "success": False,

        "message": result["message"]

    })