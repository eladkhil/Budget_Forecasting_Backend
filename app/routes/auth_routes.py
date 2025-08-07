from flask import Blueprint, request, session, abort, jsonify
from werkzeug.security import check_password_hash
from app.extensions import db
from app.models.User import User
from app.schemas.user import UserSchema
from datetime import datetime, timedelta
import secrets
from app.routes.utils import login_required
from app.utils.email import send_reset_code
from werkzeug.security import generate_password_hash
bp_auth = Blueprint("auth", __name__, url_prefix="/api/auth")
user_schema = UserSchema()   # to serialise the logged-in user
from flask_cors import cross_origin
# ───────── LOGIN ─────────
@bp_auth.post("/login")
@cross_origin(supports_credentials=True)
def login():
    data = request.json or {}
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        abort(400, "Missing credentials")

    user = User.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        abort(403, "Invalid credentials")

    # 🔒 Check for password expiry
    if user.password_expires and user.password_expires < datetime.utcnow():
        session["user_id"] = user.user_id
        session["expired"] = True  # ➕ mark that session is expired
        return jsonify({"message": "PASSWORD_EXPIRED"})


    # Set session
    session["user_id"] = user.user_id
    session["role"] = user.role.role_name if user.role else None

    return jsonify(user.to_dict())


# ───────── LOGOUT ────────
@bp_auth.post("/logout")
def logout():
    session.pop("user_id", None)
    return "", 204

# ───────── HELPER ────────
@bp_auth.get("/me")
def who_am_i():
    uid = session.get("user_id")
    if not uid:
        abort(401)
    user = User.query.get(uid)
    return user_schema.dump(user)

@bp_auth.post("/send-code")
def send_code():
    data = request.get_json() or {}
    name = data.get("name")
    surname = data.get("surname")

    if not name or not surname:
        abort(400, "Nom et prénom requis")

    user = User.query.filter_by(name=name, surname=surname).first()
    if not user:
        abort(404, "Utilisateur introuvable")

    code = f"{secrets.randbelow(1_000_000):06}"
    user.reset_code = code
    user.reset_expires = datetime.utcnow() + timedelta(minutes=15)
    db.session.commit()

    try:
        send_reset_code(user.email, code)
        return "", 200
    except Exception as e:
        print("Email send failed:", e)
        abort(500, "Erreur lors de l’envoi de l’e-mail")

@bp_auth.post("/reset-password")
def reset_password():
    data = request.json or {}
    code = data.get("code")
    new_password = data.get("password")

    if not code or not new_password:
        abort(400, "Code and password required")

    user = User.query.filter_by(reset_code=code).first()
    if not user or user.reset_expires < datetime.utcnow():
        abort(400, "Invalid or expired code")

    user.password_hash = generate_password_hash(new_password)
    user.reset_code = None
    user.reset_expires = None
    user.password_expires = datetime.utcnow() + timedelta(days=30)  # ✅ extend expiry
    db.session.commit()
    return "", 204


@bp_auth.post("/change-password")
@cross_origin(supports_credentials=True)
def change_password():
    user_id = session.get("user_id")
    if not user_id:
        abort(401, "Not logged in")

    user = User.query.get(user_id)

    data = request.json or {}
    current_password = data.get("current_password", "")
    new_password = data.get("new_password")

    if not new_password:
        abort(400, "New password is required")

    if not session.get("expired"):
        # normal login → require current password
        if not user.check_password(current_password):
            abort(401, "Current password incorrect")

    user.set_password(new_password)
    user.password_expires = datetime.utcnow() + timedelta(days=30)
    session.pop("expired", None)  # remove expired marker
    db.session.commit()
    return "", 204

