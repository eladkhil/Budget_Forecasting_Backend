from flask import Blueprint, request, jsonify
from app.models.Rubrique import Rubrique
from app.schemas.rubrique import RubriqueSchema
from app.extensions import db

bp_rubrique = Blueprint("bp_rubrique", __name__, url_prefix="/api/rubriques")

rubrique_schema = RubriqueSchema()
rubriques_schema = RubriqueSchema(many=True)

# ✅ Create
@bp_rubrique.route("", methods=["POST"])
def create_rubrique():
    try:
        data = request.get_json()
        if not data or not all(k in data for k in ("name", "direction_id")):
            return jsonify({"error": "Missing required fields"}), 400

        # Ensure direction exists (foreign key check)
        from app.models.Direction import Direction
        if not Direction.query.get(data["direction_id"]):
            return jsonify({"error": "Invalid direction_id"}), 400

        rubrique = Rubrique(name=data["name"], direction_id=data["direction_id"])
        db.session.add(rubrique)
        db.session.commit()

        return jsonify(rubrique_schema.dump(rubrique)), 201

    except Exception as e:
        print("🔥 Error in create_rubrique:", e)
        return jsonify({"error": str(e)}), 500

# ✅ Read all
@bp_rubrique.route("", methods=["GET"])
def get_rubriques():
    rubriques = Rubrique.query.all()
    return jsonify(rubriques_schema.dump(rubriques)), 200

# ✅ Read one
@bp_rubrique.route("/<int:id>", methods=["GET"])
def get_rubrique(id):
    rubrique = Rubrique.query.get_or_404(id)
    return jsonify(rubrique_schema.dump(rubrique)), 200

# ✅ Update
@bp_rubrique.route("/<int:id>", methods=["PUT"])
def update_rubrique(id):
    rubrique = Rubrique.query.get_or_404(id)
    data = request.get_json()

    rubrique.name = data.get("name", rubrique.name)
    rubrique.direction_id = data.get("direction_id", rubrique.direction_id)

    db.session.commit()
    return jsonify(rubrique_schema.dump(rubrique)), 200

# ✅ Delete
@bp_rubrique.route("/<int:id>", methods=["DELETE"])
def delete_rubrique(id):
    rubrique = Rubrique.query.get_or_404(id)
    db.session.delete(rubrique)
    db.session.commit()
    return jsonify({"message": "Deleted successfully"}), 204
