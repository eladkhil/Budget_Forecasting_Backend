from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.HorsBudget import HorsBudget
from app.models.Budget import Budget
from app.models.Direction import Direction

bp_hors_budget = Blueprint("bp_hors_budget", __name__, url_prefix="/api/horsbudget")

# ─── Create ─────────────────────────────────────────────
@bp_hors_budget.route("", methods=["POST"])
def create_hors_budget():
    data = request.get_json()
    required_fields = ["article", "prix_ht", "qte", "budget_id", "direction_id"]

    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    item = HorsBudget(
        article=data["article"],
        prix_ht=data["prix_ht"],
        qte=data.get("qte", 1),
        fournisseur=data.get("fournisseur"),
        budget_id=data["budget_id"],
        direction_id=data["direction_id"]
    )

    db.session.add(item)
    db.session.commit()

    return jsonify({
        "message": "Hors budget item created",
        "id": item.id
    }), 201

# ─── Get all ────────────────────────────────────────────
@bp_hors_budget.route("", methods=["GET"])
def get_all_hors_budget():
    items = HorsBudget.query.all()
    return jsonify([
        {
            "id": i.id,
            "article": i.article,
            "prix_ht": i.prix_ht,
            "qte": i.qte,
            "fournisseur": i.fournisseur,
            "budget_id": i.budget_id,
            "direction_id": i.direction_id
        } for i in items
    ])

# ─── Get by ID ───────────────────────────────────────────
@bp_hors_budget.route("/<int:id>", methods=["GET"])
def get_hors_budget(id):
    item = HorsBudget.query.get_or_404(id)
    return jsonify({
        "id": item.id,
        "article": item.article,
        "prix_ht": item.prix_ht,
        "qte": item.qte,
        "fournisseur": item.fournisseur,
        "budget_id": item.budget_id,
        "direction_id": item.direction_id
    })

# ─── Update ──────────────────────────────────────────────
@bp_hors_budget.route("/<int:id>", methods=["PUT"])
def update_hors_budget(id):
    item = HorsBudget.query.get_or_404(id)
    data = request.get_json()

    item.article = data.get("article", item.article)
    item.prix_ht = data.get("prix_ht", item.prix_ht)
    item.qte = data.get("qte", item.qte)
    item.fournisseur = data.get("fournisseur", item.fournisseur)
    item.budget_id = data.get("budget_id", item.budget_id)
    item.direction_id = data.get("direction_id", item.direction_id)

    db.session.commit()

    return jsonify({"message": "Hors budget item updated"})

# ─── Delete ──────────────────────────────────────────────
@bp_hors_budget.route("/<int:id>", methods=["DELETE"])
def delete_hors_budget(id):
    item = HorsBudget.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Hors budget item deleted"}), 204
