from flask import Flask


def create_app():

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    from app.api.detect import detect_bp
    from app.api.register import register_bp
    from app.api.login import login_bp


    app.register_blueprint(detect_bp)
    app.register_blueprint(register_bp)
    app.register_blueprint(login_bp)

    return app