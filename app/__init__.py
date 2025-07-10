# app/__init__.py  (or wherever create_app lives)
from flask import Flask
from flask_cors import CORS               # one import is enough
from flask_session import Session
from app.config import DevConfig
from app.extensions import db, ma, mail   # ← no "cors" here
from app.routes import blueprints

def create_app(config_class=DevConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # ── session cookie settings ─────────────────────────
    app.config.update(
        SESSION_COOKIE_SAMESITE='Lax',
        SESSION_COOKIE_SECURE=False,
        SESSION_COOKIE_HTTPONLY=True,
        SECRET_KEY='super-secret-key',
        SESSION_TYPE='filesystem'
    )

    # ── init extensions ─────────────────────────
    db.init_app(app)
    ma.init_app(app)
    mail.init_app(app)

    # ── initialize server-side session after config ─────
    Session(app)

     # ── CORS only once ─────────────────────────
    CORS(
        app,
        resources={r"/api/*": {"origins": ["http://localhost:4200", "http://127.0.0.1:4200"]}},
        supports_credentials=True,
        allow_headers=["Content-Type"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    # 🔍 Log incoming Origin to debug CORS issues
    @app.after_request
    def after_request(response):
        from flask import request
        origin = request.headers.get("Origin")
        print("➡️ Origin received:", origin)
        if origin in ["http://localhost:4200", "http://127.0.0.1:4200"]:
            response.headers.add("Access-Control-Allow-Origin", origin)
            response.headers.add("Access-Control-Allow-Credentials", "true")
            response.headers.add("Access-Control-Allow-Headers", "Content-Type")
            response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        return response

    # ── register blueprints ─────────────────────
    for bp in blueprints:
        app.register_blueprint(bp)
        
    print("\n✅ Registered routes:")
    for rule in app.url_map.iter_rules():
        print(rule)

    return app
