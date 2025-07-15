from flask import Blueprint, request, jsonify
from app.models.Groupement import Groupement
from app.schemas.groupement import GroupementSchema
from app.extensions import db
import traceback
# ✅ Consistent URL prefix
bp_groupement = Blueprint("bp_groupement", __name__, url_prefix="/api/groupements")

# Schemas
groupement_schema = GroupementSchema()
groupements_schema = GroupementSchema(many=True)

def compute_budgets_for_groupement(groupement_id):
    from app.models.ProjetDetail import ProjetDetail

    details = ProjetDetail.query.filter_by(groupement_id=groupement_id).all()
    budget_alloue = sum(d.montant for d in details)
    budget_consomme = sum(d.montant_consomme or 0 for d in details)

    return budget_alloue, budget_consomme

# ✅ Create
@bp_groupement.route("", methods=["POST"])
def create_groupement():
    try:
        data = request.get_json()

        # Cast numeric fields properly
        budget_alloue = float(data.get("budget_alloue", 0))  # default to 0
        budget_consomme = float(data.get("budget_consomme", 0))

        ecart = budget_alloue - budget_consomme  # 💥 Automatically calculate

        groupement = Groupement(
            name=data["name"],
            rubrique_id=int(data["rubrique_id"]),
            budget_id=int(data["budget_id"]),
            budget_alloue=budget_alloue,
            budget_consomme=budget_consomme,
            ecart=ecart
        )

        db.session.add(groupement)
        db.session.commit()

        return jsonify(groupement_schema.dump(groupement)), 201

    except Exception as e:
        print("[FLASK ERROR] Failed to create groupement")
        print("[Exception]:", e)
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


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
    if "budget_id" in data:
        groupement.budget_id = data["budget_id"]

    # Recompute budgets and ecart based on current ProjetDetails
    budget_alloue, budget_consomme = compute_budgets_for_groupement(groupement.id)
    groupement.budget_alloue = budget_alloue
    groupement.budget_consomme = budget_consomme
    groupement.ecart = budget_alloue - budget_consomme  # 💥 Recalculate ecart

    db.session.commit()
    return jsonify(groupement_schema.dump(groupement)), 200

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


# ✅ Delete
@bp_groupement.route("/<int:id>", methods=["DELETE"])
def delete_groupement(id):
    groupement = Groupement.query.get_or_404(id)
    db.session.delete(groupement)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"}), 204


# ✅ Filter groupements by year from Budget
@bp_groupement.route("/year/<int:year>", methods=["GET"])
def get_groupements_by_year(year):
    from app.models.Budget import Budget

    # Get budgets for that year
    budgets = Budget.query.filter_by(year=year).all()
    budget_ids = [b.id for b in budgets]

    # Get groupements related to these budgets
    groupements = Groupement.query.filter(Groupement.budget_id.in_(budget_ids)).all()

    return jsonify(groupements_schema.dump(groupements)), 200
