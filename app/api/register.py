import pandas as pd
import numpy as np
import cv2
from flask import Flask, request, jsonify

app=Flask(__name__)

@app.route("/register",method=["POST"])
def register():

    try:
        data=request.get_json()
        name=data['full_name']
        email=data['email']
        password=data['password']
        image=data['image']

        #convert the image into face embeddings using the face recognition model

        #Save to database

    except Exception as e:
        return jsonify({"error": str(e)}), 400