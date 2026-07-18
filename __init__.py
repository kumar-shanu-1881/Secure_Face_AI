from flask import Flask
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )
    app.secret_key = os.getenv("SECRET_KEY")
    app.permanent_session_lifetime = timedelta(days=2)

    from app.api.detect import detect_bp
    from app.api.register import register_bp
    from app.api.login import login_bp
    from app.api.dashboard import dashboard_bp
    from app.api.logout import logout_bp


    app.register_blueprint(detect_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(login_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(logout_bp)

    return app