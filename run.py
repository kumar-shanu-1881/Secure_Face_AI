from flask import Flask, render_template , Response
from __init__ import create_app

app=create_app()

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)