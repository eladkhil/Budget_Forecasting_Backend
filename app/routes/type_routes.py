from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Type


type_bp = Blueprint('type_bp', __name__)

@type_bp.route('/api/types', methods=['GET'])
def get_types():
    types = Type.query.all()
    return jsonify([{'id_type': t.id_type, 'type': t.type} for t in types]), 200

@type_bp.route('/api/types', methods=['POST'])
def create_type():
    data = request.get_json()
    type = data.get('type')
    if not type:
        return jsonify({'error': 'type is required'}), 400

    new_type = Type(type=type)
    db.session.add(new_type)
    db.session.commit()
    return jsonify({'message': 'Type created', 'id_type': new_type.id_type}), 201
@type_bp.route('/api/types/<int:id_type>', methods=['GET'])
def get_type(id_type):
    type = Type.query.get_or_404(id_type)
    return jsonify({'id_type': type.id_type, 'nom_type': type.nom_type}), 200
@type_bp.route('/api/types/<int:id_type>', methods=['PUT'])
def update_type(id_type):
    data = request.get_json()
    type = data.get('type')
    if not type:
        return jsonify({'error': 'type is required'}), 400

    type = Type.query.get_or_404(id_type)
    type.type = type
    db.session.commit()
    return jsonify({'message': 'Type updated', 'id_type': type.id_type}), 200   
@type_bp.route('/api/types/<int:id_type>', methods=['DELETE'])
def delete_type(id_type):
    type = Type.query.get_or_404(id_type)
    db.session.delete(type)
    db.session.commit()
    return jsonify({'message': 'Type deleted'}), 200
