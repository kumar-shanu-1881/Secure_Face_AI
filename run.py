from flask import Flask, render_template ,jsonify
from __init__ import create_app
# import os 

app=create_app()

@app.route('/')
def index():
    return render_template('index.html')

# health-check endpoint
@app.route('/health', methods=['GET'])
def health():
    # Return 200 OK immediately.
    return jsonify({"status": "alive"}), 200

@app.route('/preview',methods=['GET'])
def preview():
    return render_template("preview.html")

@app.route('/checksimilarity')
def checksimilarity():
    return render_template("checksimilarity.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/login")
def login():
    return render_template("login.html")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)
    # port = int(os.environ.get("PORT", 7860))
    # app.run(host='0.0.0.0', port=port)