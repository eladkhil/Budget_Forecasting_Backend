from flask import Blueprint, request, jsonify
from app.models.Groupement import Groupement
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
    if not data or not all(k in data for k in ("groupement_id", "type", "montant", "montant_consomme")):
        return jsonify({"error": "Missing required fields"}), 400

    detail = ProjetDetail(
        groupement_id=data["groupement_id"],
        type=data["type"],
        montant=data["montant"],
        montant_consomme=data["montant_consomme"]
    )
    db.session.add(detail)
    db.session.commit()

    # 🔁 Update budget fields in the related groupement
    from app.routes.groupement_routes import compute_budgets_for_groupement
    groupement = Groupement.query.get(detail.groupement_id)
    groupement.budget_alloue, groupement.budget_consomme = compute_budgets_for_groupement(groupement.id)
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
    if "montant_consomme" in data:
        detail.montant_consomme = data["montant_consomme"]
    if "groupement_id" in data:
        detail.groupement_id = data["groupement_id"]

    db.session.commit()

    # 🔁 Update groupement budget
    from app.routes.groupement_routes import compute_budgets_for_groupement
    groupement = Groupement.query.get(detail.groupement_id)
    groupement.budget_alloue, groupement.budget_consomme = compute_budgets_for_groupement(groupement.id)
    db.session.commit()

    return jsonify(detail_schema.dump(detail)), 200

# ✅ Delete
@bp_projet_detail.route("/<int:id>", methods=["DELETE"])
def delete_detail(id):
    detail = ProjetDetail.query.get_or_404(id)
    groupement_id = detail.groupement_id

    db.session.delete(detail)
    db.session.commit()

    # 🔁 Update budget after deletion
    from app.routes.groupement_routes import compute_budgets_for_groupement
    groupement = Groupement.query.get(groupement_id)
    if groupement:
        groupement.budget_alloue, groupement.budget_consomme = compute_budgets_for_groupement(groupement.id)
        db.session.commit()

    return jsonify({"message": "Deleted successfully"}), 204
