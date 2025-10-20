from flask import Flask
from flask_cors import CORS              
from flask_session import Session
from app.config import DevConfig
from app.extensions import db, ma, mail   
from app.routes import blueprints
from app.utils.notifier import socketio


def create_app(config_class=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.config.update(
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=False,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_DOMAIN=None,
        SECRET_KEY='super-secret-key',
        SESSION_COOKIE_PATH="/",
        SESSION_TYPE='filesystem',

    )
    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)

    Session(app)

    CORS(
            app,
            origins=["http://localhost:4200", "http://127.0.0.1:4200"],
            supports_credentials=True,
            expose_headers=["Authorization"],
            allow_headers=["Content-Type", "Authorization"],
            methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        )
    socketio.init_app(app)

    @app.after_request
    def after_request(response):
        from flask import request
        print("➡️ Origin received:", request.headers.get("Origin"))
        return response

    for bp in blueprints:
        app.register_blueprint(bp)
        
    print(" Registered routes:")
    for rule in app.url_map.iter_rules():
        print(rule)

    return app
