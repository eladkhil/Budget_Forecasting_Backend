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
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data.get("username")).first_or_404()

    # Handle missing password expiration date
    if not user.password_expires:
        user.password_expires = datetime.utcnow() + timedelta(days=30)
        db.session.commit()

    # Check if password expired
    if user.password_expires < datetime.utcnow():
        abort(403, description="Password expired")

    if not user.check_password(data.get("password")):
        abort(401, description="Invalid credentials")

    # ---------- Connexion OK
    session["user_id"] = user.user_id
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
    # Simulate current user, or get from session/token
    user_id = session.get("user_id")   # or replace with actual logged-in logic
    if not user_id:
        abort(401, "Not logged in")

    user = User.query.get(user_id)
    if not user:
        abort(404, "User not found")

    code = f"{secrets.randbelow(1_000_000):06}"  # 6-digit code
    user.reset_code = code
    user.reset_expires = datetime.utcnow() + timedelta(minutes=15)
    db.session.commit()

    try:
        send_reset_code(user.email, code)
        return "", 200
    except Exception as e:
        print("Email send failed:", e)
        abort(500, "Could not send email")

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
    db.session.commit()
    return "", 204

@bp_auth.post("/change-password")
@login_required
def change_password():
    data = request.json or {}
    user = User.query.get(session["user_id"])

    # verify current password
    if not user.check_password(data.get("current_password", "")):
        abort(401, "Current password incorrect")

    # set new and auto-extend expiry (+1 month by model logic)
    user.set_password(data["new_password"])
    db.session.commit()
    return "", 204
