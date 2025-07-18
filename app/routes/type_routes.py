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
    return jsonify({'id_type': type.id_type, 'nom_type': type.type}), 200
@type_bp.route('/api/types/<int:id_type>', methods=['PUT'])
def update_type(id_type):
    data = request.get_json()
    new_type_name = data.get('type') 
    
    if not new_type_name:
        return jsonify({'error': 'Le champ "type" est requis.'}), 400

    type_obj = Type.query.get_or_404(id_type)
    type_obj.type = new_type_name  
    db.session.commit()
    
    return jsonify({'message': 'Type mis à jour', 'id_type': type_obj.id_type}), 200 
@type_bp.route('/api/types/<int:id_type>', methods=['DELETE'])
def delete_type(id_type):
    type = Type.query.get_or_404(id_type)
    db.session.delete(type)
    db.session.commit()
    return jsonify({'message': 'Type deleted'}), 200
