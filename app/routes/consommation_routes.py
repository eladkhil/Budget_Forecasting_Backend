from flask import Blueprint, request, jsonify
from app.models.Consommation import Consommation
from app.models.Groupement import Groupement
from app.models.Budget import Budget
from app.schemas.consommation import ConsommationSchema
from app.extensions import db

bp_consommation = Blueprint("bp_consommation", __name__, url_prefix="/api/consommations")

consommation_schema = ConsommationSchema()
consommations_schema = ConsommationSchema(many=True)

# ✅ Create
@bp_consommation.route("", methods=["POST"])
def create_consommation():
    data = request.get_json()
    if not data or not all(k in data for k in ("groupement_id", "montant")):
        return jsonify({"error": "Missing required fields"}), 400

    consommation = Consommation(
        groupement_id=data["groupement_id"],
        montant=data["montant"]
    )
    db.session.add(consommation)
    db.session.commit()

    update_budget_ecart_from_groupement(consommation.groupement_id)

    return jsonify(consommation_schema.dump(consommation)), 201

# ✅ Get all
@bp_consommation.route("", methods=["GET"])
def get_consommations():
    consommations = Consommation.query.all()
    return jsonify(consommations_schema.dump(consommations)), 200

# ✅ Get one
@bp_consommation.route("/<int:id>", methods=["GET"])
def get_consommation(id):
    consommation = Consommation.query.get_or_404(id)
    return jsonify(consommation_schema.dump(consommation)), 200

# ✅ Update
@bp_consommation.route("/<int:id>", methods=["PUT"])
def update_consommation(id):
    consommation = Consommation.query.get_or_404(id)
    old_groupement_id = consommation.groupement_id

    data = request.get_json()
    if not data:
        return jsonify({"error": "No input provided"}), 400

    consommation.groupement_id = data.get("groupement_id", consommation.groupement_id)
    consommation.montant = data.get("montant", consommation.montant)

    db.session.commit()

    # Update both old and new budgets if groupement_id has changed
    update_budget_ecart_from_groupement(old_groupement_id)
    if old_groupement_id != consommation.groupement_id:
        update_budget_ecart_from_groupement(consommation.groupement_id)

    return jsonify(consommation_schema.dump(consommation)), 200

# ✅ Delete
@bp_consommation.route("/<int:id>", methods=["DELETE"])
def delete_consommation(id):
    consommation = Consommation.query.get_or_404(id)
    groupement_id = consommation.groupement_id

    db.session.delete(consommation)
    db.session.commit()

    update_budget_ecart_from_groupement(groupement_id)

    return jsonify({"message": "Deleted successfully"}), 204

# 🔁 Helper: Update ecart and cloture via groupement
def update_budget_ecart_from_groupement(groupement_id):
    groupement = Groupement.query.get(groupement_id)
    if not groupement or not groupement.budget_id:
        return

    # Get all groupements linked to same budget
    groupements = Groupement.query.filter_by(budget_id=groupement.budget_id).all()

    total_alloue = sum(g.budget_alloue or 0 for g in groupements)
    total_consomme = 0

    for g in groupements:
        total_consomme += sum(c.montant or 0 for c in g.consommations)

    budget = Budget.query.get(groupement.budget_id)
    if budget:
        budget.total_consommanation = total_consomme
        budget.ecart = total_alloue - total_consomme
        budget.cloture = budget.ecart <= 0
        db.session.commit()
@bp_consommation.route("/groupements/<int:year>", methods=["GET"])
def get_groupements_by_year(year):
    budgets = Budget.query.filter_by(year=year).all()
    budget_ids = [b.id for b in budgets]

    groupements = Groupement.query.filter(Groupement.budget_id.in_(budget_ids)).all()

    return jsonify([
        {
            "id": g.id,
            "name": g.name,
            "rubrique_id": g.rubrique_id,
            "budget_id": g.budget_id
        } for g in groupements
    ])
