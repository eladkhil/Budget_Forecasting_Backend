# app/__init__.py  (or wherever create_app lives)
from flask import Flask
from flask_cors import CORS               # one import is enough

from app.config import DevConfig
from app.extensions import db, ma, mail   # ← no "cors" here
from app.routes import blueprints

def create_app(config_class=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ── init extensions ─────────────────────────
    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)

    # ── CORS only once ─────────────────────────
    CORS(
        app,
        resources={r"/api/*": {"origins": "http://localhost:4200"}},
        supports_credentials=True,
        allow_headers=["Content-Type"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    # ── register blueprints ─────────────────────
    for bp in blueprints:
        app.register_blueprint(bp)

    return app
