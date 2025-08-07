from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.AzureMonthlyTracking import AzureMonthlyTracking
from app.schemas.azureMonthlyTracking import AzureMonthlyTrackingSchema
from app.models.Groupement import Groupement
from app.models.Budget import Budget

bp_azure = Blueprint("bp_azure", __name__, url_prefix="/api/azure-monthly")

# ✅ Define schemas once at the top
schema = AzureMonthlyTrackingSchema()
many_schema = AzureMonthlyTrackingSchema(many=True)

@bp_azure.route('', methods=['POST'])
def create_azure_entry():
    try:
        data = request.get_json()
        print("Received data:", data)

        consommation = float(data['consommation'])
        reservation = float(data['reservation'])
        tva_percent = float(data['tva_percent'])

        # ➕ Calculate montant_ht (monthly)
        montant_ht = consommation + reservation + ((consommation + reservation) * tva_percent / 100)

        # ① Create and insert the AzureMonthlyTracking entry
        new_entry = AzureMonthlyTracking(
            groupement_id=data['groupement_id'],
            mois=data['mois'],
            periode=data['periode'],
            fournisseur=data['fournisseur'],
            numero_facture=data['numero_facture'],
            reservation=reservation,
            consommation=consommation,
            tva_percent=tva_percent,
        )
        db.session.add(new_entry)

        # ② Update Groupement's annual budget_alloue and budget_consomme
        groupement = Groupement.query.get(data['groupement_id'])
        if groupement:
            # Default to 0 if null
            groupement.budget_alloue = (groupement.budget_alloue or 0) + montant_ht
            groupement.budget_consomme = (groupement.budget_consomme or 0) + montant_ht

        db.session.commit()
        return jsonify({"message": "Azure entry added and groupement budget updated"}), 201

    except Exception as e:
        print("❌ ERROR:", str(e))
        return jsonify({"error": str(e)}), 500

# ✅ Read all
@bp_azure.route("", methods=["GET"])
def get_all_azure():
    entries = AzureMonthlyTracking.query.all()
    return jsonify(many_schema.dump(entries)), 200

# ✅ Read one
@bp_azure.route("/<int:id>", methods=["GET"])
def get_azure_by_id(id):
    entry = AzureMonthlyTracking.query.get_or_404(id)
    return jsonify(schema.dump(entry)), 200

# ✅ Update
@bp_azure.route("/<int:id>", methods=["PUT"])
def update_azure(id):
    entry = AzureMonthlyTracking.query.get_or_404(id)
    data = request.get_json()

    for field in [
        "mois", "periode", "fournisseur", "numero_facture",
        "reservation", "consommation", "tva_percent", "groupement_id"
    ]:
        if field in data:
            setattr(entry, field, data[field])

    db.session.commit()
    return jsonify(schema.dump(entry)), 200

# ✅ Delete
@bp_azure.route("/<int:id>", methods=["DELETE"])
def delete_azure(id):
    entry = AzureMonthlyTracking.query.get_or_404(id)
    db.session.delete(entry)
    db.session.commit()
    return jsonify({"message": "Deleted"}), 204

# ✅ Get all AzureMonthlyTracking entries by year
@bp_azure.route("/year/<int:year>", methods=["GET"])
def get_azure_by_year(year):
    budget = Budget.query.filter_by(year=year).first()
    if not budget:
        return jsonify([])

    groupement = Groupement.query.filter_by(
        name="Consommation Azure CSP", budget_id=budget.id
    ).first()

    if not groupement:
        return jsonify([])

    rows = AzureMonthlyTracking.query.filter_by(groupement_id=groupement.id).all()
    return jsonify(many_schema.dump(rows)), 200

# ✅ Get groupement_id for Azure tracking by year
@bp_azure.route("/groupement/<int:year>", methods=["GET"])
def get_azure_groupement_by_year(year):
    budget = Budget.query.filter_by(year=year).first()
    if not budget:
        return jsonify({"error": f"Budget not found for year {year}"}), 404

    groupement = Groupement.query.filter_by(
        name="Consommation Azure CSP", budget_id=budget.id
    ).first()

    if not groupement:
        return jsonify({"error": f"Groupement 'Consommation Azure CSP' not found for {year}"}), 404

    return jsonify({"id": groupement.id, "name": groupement.name}), 200
