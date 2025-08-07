from flask import Blueprint, request, abort
from app.extensions import db
from app.models.Role import Role
from app.schemas.role import RoleSchema

bp_role = Blueprint("roles", __name__, url_prefix="/api/roles")
role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)

@bp_role.route("",methods=["POST"])
def create_role():
    name = request.json.get("role_name")
    if not name:
        abort(400, "role_name required")
    role = Role(role_name=name)
    db.session.add(role)
    db.session.commit()
    return role_schema.dump(role), 201

@bp_role.route("",methods=["GET"])
def list_roles():
    return roles_schema.dump(Role.query.all())
@bp_role.get("/<int:role_id>")
def get_rolename(role_id):
    role =Role.query.get_or_404(role_id)
    return role_schema.dump(role), 201
