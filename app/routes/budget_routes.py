from flask import Blueprint, request, jsonify
from app.models.Budget import Budget
from app.models.Groupement import Groupement
from app.schemas.budget import BudgetSchema
from app.extensions import db
from flask import Blueprint, request, jsonify
from sqlalchemy import text
from app.models import Budget, Direction, Rubrique, Groupement, ProjetDetail

bp_budget = Blueprint("bp_budget", __name__, url_prefix="/api/budgets")
budget_schema = BudgetSchema()
budgets_schema = BudgetSchema(many=True)

# ─── Create a new budget ─────────────────────────────
@bp_budget.route("", methods=["POST"])
def create_budget():
    data = request.get_json()
    if not data or "year" not in data:
        return jsonify({"error": "Missing 'year' field"}), 400

    budget = Budget(
        year=data["year"],
        cloture=False,
        total_budget=0,
        total_consommation=0
    )

    db.session.add(budget)
    db.session.commit()

    return jsonify(budget_schema.dump(budget)), 201

# ─── Get all budgets ─────────────────────────────────
@bp_budget.route("", methods=["GET"])
def get_budgets():
    budgets = Budget.query.all()
    for budget in budgets:
        compute_ecart(budget)
    db.session.commit()
    return jsonify(budgets_schema.dump(budgets)), 200

# ─── Get a single budget ─────────────────────────────
@bp_budget.route("/<int:id>", methods=["GET"])
def get_budget(id):
    budget = Budget.query.get_or_404(id)
    compute_ecart(budget)
    db.session.commit()
    return jsonify(budget_schema.dump(budget)), 200

# ─── Update a budget ─────────────────────────────────
@bp_budget.route("/<int:id>", methods=["PUT"])
def update_budget(id):
    budget = Budget.query.get_or_404(id)
    data = request.get_json()

    budget.year = data.get("year", budget.year)

    # Use value sent by frontend
    if "cloture" in data:
        budget.cloture = data["cloture"]

    compute_ecart(budget)

    db.session.commit()
    return jsonify(budget_schema.dump(budget)), 200


# ─── Delete a budget ─────────────────────────────────
@bp_budget.route("/<int:id>", methods=["DELETE"])
def delete_budget(id):
    budget = Budget.query.get_or_404(id)
    db.session.delete(budget)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"}), 204

# ─── Helper: Compute écart automatically ─────────────
def compute_ecart(budget: Budget):
    groupements = Groupement.query.filter_by(budget_id=budget.id).all()
    total_alloue = sum(g.budget_alloue or 0 for g in groupements)
    total_consomme = sum(g.budget_consomme or 0 for g in groupements)


    budget.total_budget = total_alloue
    budget.total_consommation = total_consomme

    # Clôturé = true -> compute écart
    if budget.cloture:
        budget.ecart = total_alloue - total_consomme
    else:
        budget.ecart = None



bp_report = Blueprint("bp_report", __name__, url_prefix="/api/report")

@bp_report.route("/year/<int:year>", methods=["GET"])
def get_consolidated_report(year):
    sql = text("""
        SELECT 
            d.name AS direction,
            r.name AS rubrique,
            g.name AS groupement,
            CONCAT(COALESCE(pd.type, ''), ': ', COALESCE(pd.montant, 0), ' DT') AS projet,
            CONCAT(COALESCE(g.budget_consomme, 0), ' DT') AS consommation,
            b.cloture,
            CASE 
                WHEN b.cloture = 1 THEN CONCAT((g.budget_alloue - COALESCE(g.budget_consomme, 0)), ' DT')
                ELSE '—'
            END AS ecart
        FROM Budgets b
        JOIN Groupements g ON g.budget_id = b.id
        JOIN Rubriques r ON r.id = g.rubrique_id
        JOIN Directions d ON d.id = r.direction_id
        LEFT JOIN ProjetDetails pd ON pd.groupement_id = g.id
        WHERE b.year = :year
        ORDER BY d.name, r.name, g.name
    """)


    results = db.session.execute(sql, {"year": year}).fetchall()
    
    return jsonify([dict(row._mapping) for row in results])
