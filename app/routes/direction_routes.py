from flask import Blueprint, request, jsonify, abort
from app.models.Direction import Direction
from app.schemas.direction import DirectionSchema
from app.extensions import db

# Add a proper URL prefix
bp_direction = Blueprint("bp_direction", __name__, url_prefix="/api/directions")

# Schemas
direction_schema = DirectionSchema()
directions_schema = DirectionSchema(many=True)

# Create a new direction
@bp_direction.route("", methods=["POST"])
def create_direction():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name' field"}), 400

    direction = Direction(name=data["name"])
    db.session.add(direction)
    db.session.commit()

    return jsonify(direction_schema.dump(direction)), 201

# Get all directions
@bp_direction.route("", methods=["GET"])
def get_directions():
    directions = Direction.query.all()
    return jsonify(directions_schema.dump(directions)), 200

# Get a single direction by ID
@bp_direction.route("/<int:id>", methods=["GET"])
def get_direction(id):
    direction = Direction.query.get_or_404(id)
    return jsonify(direction_schema.dump(direction)), 200

# Update a direction
@bp_direction.route("/<int:id>", methods=["PUT"])
def update_direction(id):
    direction = Direction.query.get_or_404(id)
    data = request.get_json()
    
    if not data or "name" not in data:
        return jsonify({"error": "Missing 'name' field"}), 400

    direction.name = data["name"]
    db.session.commit()

    return jsonify(direction_schema.dump(direction)), 200

# Delete a direction
@bp_direction.route("/<int:id>", methods=["DELETE"])
def delete_direction(id):
    direction = Direction.query.get_or_404(id)
    db.session.delete(direction)
    db.session.commit()

    return jsonify({"message": "Deleted successfully"}), 204
