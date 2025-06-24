from flask import Blueprint, request, session, abort
from app.extensions import db
from app.models.User import User
from app.schemas.user import UserSchema
from datetime import datetime, timedelta
bp_user = Blueprint("users", __name__, url_prefix="/api/users")
user_schema  = UserSchema()
users_schema = UserSchema(many=True)

@bp_user.post("")
def create_user():
    data = request.json or {}
    missing = [k for k in ("username", "name", "surname", "email", "password","phone", "role_id") if k not in data]
    if missing: abort(400, f"Missing {', '.join(missing)}")
    user = User(
    username=data["username"],
    name=data["name"],
    surname=data["surname"],
    email=data["email"],
    role_id=data["role_id"],
    phone=data.get("phone"),
    password_expires=datetime.utcnow() + timedelta(days=30) 
    )
    user.set_password(data["password"])
    db.session.add(user)
    db.session.commit()
    return user_schema.dump(user), 201

@bp_user.get("")
def list_users1():
    return users_schema.dump(User.query.all())

@bp_user.get("/<int:user_id>")
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return user_schema.dump(user)

@bp_user.put("/<int:user_id>")
def update_user(user_id):
    _login_required()
    user = User.query.get_or_404(user_id)

    # ─── Allow only the user themself (or an admin) to edit ───
    requester_id   = session["user_id"]
    requester_role = session.get("role")            # depends on how you store roles

    is_admin  = requester_role == "admin"           # adjust to your role logic
    is_self   = requester_id == user_id

    if not (is_self or is_admin):
        abort(403, "Forbidden")

    data = request.json or {}

    # ─── If the user edits their own account, verify password ───
    if is_self and not is_admin:
        verify_current_password(user, data)

    # ─── Apply changes ───
    for field in ("name", "surname", "email", "role_id"):
        if field in data:
            setattr(user, field, data[field])

    # Optional: allow password change in the same call
    if "password" in data:
        user.set_password(data["password"])

    db.session.commit()
    return user_schema.dump(user)


@bp_user.delete("/<int:user_id>")
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return "", 204

def _login_required():
    if "user_id" not in session:
        abort(401)

@bp_user.get("")
def list_users():
    _login_required()
    users = User.query.all()
    return users_schema.dump(users)

def verify_current_password(user, data: dict):
    """
    Abort(401) unless `current_password` is present and correct.
    """
    cur_pw = data.get("current_password")
    if not cur_pw or not user.check_password(cur_pw):
        abort(401, "Current password is incorrect")