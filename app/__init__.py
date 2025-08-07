from flask import Flask, jsonify
from flask_cors import CORS
from flask_session import Session
from app.config import DevConfig
from app.extensions import db, ma, mail
from app.routes import blueprints
from werkzeug.exceptions import HTTPException

from sqlalchemy import inspect, text

def ensure_password_expires_column(app):
    """Ensures the 'password_expires' column exists in the SQL Server 'User' table."""
    with app.app_context():
        inspector = inspect(db.engine)
        columns = [col["name"] for col in inspector.get_columns("User")]

        if "password_expires" not in columns:
            print("⚠️ 'password_expires' column missing. Creating it now...")
            db.session.execute(text("ALTER TABLE [User] ADD password_expires DATETIME NULL"))
            db.session.commit()
            print("✅ 'password_expires' column created successfully.")
        else:
            print("✅ 'password_expires' column already exists.")


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
    Session(app)

    # ✅ Ensure password_expires column exists
    ensure_password_expires_column(app)

    # ── CORS only once ─────────────────────────
    CORS(
        app,
        resources={r"/api/*": {"origins": ["http://localhost:4200", "http://127.0.0.1:4200"]}},
        supports_credentials=True,
        allow_headers=["Content-Type"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    )

    # ── register blueprints ─────────────────────
    for bp in blueprints:
        app.register_blueprint(bp)

    # ── global JSON error handler ───────────────
    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        response = e.get_response()
        response.data = jsonify({
            "code": e.code,
            "message": e.description
        }).data
        response.content_type = "application/json"
        return response

    print("\n✅ Registered routes:")
    for rule in app.url_map.iter_rules():
        print(rule)

    return app
