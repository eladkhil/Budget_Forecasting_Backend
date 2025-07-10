from flask import Blueprint, request, jsonify
from app.models.Groupement import Groupement
from app.schemas.groupement import GroupementSchema
from app.extensions import db

# ✅ Consistent URL prefix
bp_groupement = Blueprint("bp_groupement", __name__, url_prefix="/api/groupements")

# Schemas
groupement_schema = GroupementSchema()
groupements_schema = GroupementSchema(many=True)

# ✅ Create
@bp_groupement.route("", methods=["POST"])
def create_groupement():
    data = request.get_json()
    if not data or "name" not in data or "rubrique_id" not in data:
        return jsonify({"error": "Missing required fields"}), 400

    groupement = Groupement(
        name=data["name"],
        rubrique_id=data["rubrique_id"],
        budget_alloue=data.get("budget_alloue"),
        budget_id=data.get("budget_id")
    )
    db.session.add(groupement)
    db.session.commit()
    return jsonify(groupement_schema.dump(groupement)), 201

# ✅ Read all
@bp_groupement.route("", methods=["GET"])
def get_groupements():
    groupements = Groupement.query.all()
    return jsonify(groupements_schema.dump(groupements)), 200

# ✅ Read one
@bp_groupement.route("/<int:id>", methods=["GET"])
def get_groupement(id):
    groupement = Groupement.query.get_or_404(id)
    return jsonify(groupement_schema.dump(groupement)), 200

# ✅ Update
@bp_groupement.route("/<int:id>", methods=["PUT"])
def update_groupement(id):
    groupement = Groupement.query.get_or_404(id)
    data = request.get_json()

    if not data:
        return jsonify({"error": "No input provided"}), 400

    if "name" in data:
        groupement.name = data["name"]
    if "rubrique_id" in data:
        groupement.rubrique_id = data["rubrique_id"]
    if "budget_alloue" in data:
        groupement.budget_alloue = data["budget_alloue"]
    if "budget_id" in data:
        groupement.budget_id = data["budget_id"]

    db.session.commit()
    return jsonify(groupement_schema.dump(groupement)), 200

# ✅ Delete
@bp_groupement.route("/<int:id>", methods=["DELETE"])
def delete_groupement(id):
    groupement = Groupement.query.get_or_404(id)
    db.session.delete(groupement)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"}), 204
