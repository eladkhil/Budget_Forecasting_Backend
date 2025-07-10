from flask import Blueprint, request, jsonify
from app.models.ProjetDetail import ProjetDetail
from app.schemas.projetDetail import ProjetDetailSchema
from app.extensions import db

bp_projet_detail = Blueprint("bp_projet_detail", __name__, url_prefix="/api/projetdetails")

# Schemas
detail_schema = ProjetDetailSchema()
details_schema = ProjetDetailSchema(many=True)

# ✅ Create
@bp_projet_detail.route("", methods=["POST"])
def create_detail():
    data = request.get_json()
    if not data or not all(k in data for k in ("groupement_id", "type", "montant")):
        return jsonify({"error": "Missing required fields"}), 400

    detail = ProjetDetail(
        groupement_id=data["groupement_id"],
        type=data["type"],
        montant=data["montant"]
    )
    db.session.add(detail)
    db.session.commit()
    return jsonify(detail_schema.dump(detail)), 201

# ✅ Get All
@bp_projet_detail.route("", methods=["GET"])
def get_all_details():
    details = ProjetDetail.query.all()
    return jsonify(details_schema.dump(details)), 200

# ✅ Get by ID
@bp_projet_detail.route("/<int:id>", methods=["GET"])
def get_detail(id):
    detail = ProjetDetail.query.get_or_404(id)
    return jsonify(detail_schema.dump(detail)), 200

# ✅ Get by Groupement ID
@bp_projet_detail.route("/groupement/<int:groupement_id>", methods=["GET"])
def get_details_by_groupement(groupement_id):
    details = ProjetDetail.query.filter_by(groupement_id=groupement_id).all()
    return jsonify(details_schema.dump(details)), 200

# ✅ Update
@bp_projet_detail.route("/<int:id>", methods=["PUT"])
def update_detail(id):
    detail = ProjetDetail.query.get_or_404(id)
    data = request.get_json()

    if "type" in data:
        detail.type = data["type"]
    if "montant" in data:
        detail.montant = data["montant"]
    if "groupement_id" in data:
        detail.groupement_id = data["groupement_id"]

    db.session.commit()
    return jsonify(detail_schema.dump(detail)), 200

# ✅ Delete
@bp_projet_detail.route("/<int:id>", methods=["DELETE"])
def delete_detail(id):
    detail = ProjetDetail.query.get_or_404(id)
    db.session.delete(detail)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"}), 204
