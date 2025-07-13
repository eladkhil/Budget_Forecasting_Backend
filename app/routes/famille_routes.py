from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Famille

famille_bp = Blueprint('famille', __name__, url_prefix='/api/familles')

# CREATE
@famille_bp.route('/', methods=['POST'])
def create_famille():
    data = request.get_json()
    nom = data.get('nom')

    if not nom:
        return jsonify({'error': 'Le nom est requis.'}), 400

    famille = Famille(nom_famille=nom)
    db.session.add(famille)
    db.session.commit()
    return jsonify(famille.to_dict()), 201

# READ ALL
@famille_bp.route('/', methods=['GET'])
def get_familles():
    familles = Famille.query.all()
    return jsonify([f.to_dict() for f in familles]), 200

# READ ONE
@famille_bp.route('/<int:id>', methods=['GET'])
def get_famille(id):
    famille = Famille.query.get_or_404(id)
    return jsonify(famille.to_dict()), 200

# UPDATE
@famille_bp.route('/<int:id>', methods=['PUT'])
def update_famille(id):
    famille = Famille.query.get_or_404(id)
    data = request.get_json()
    famille.nom_famille = data.get('nom', famille.nom_famille)
    db.session.commit()
    return jsonify(famille.to_dict()), 200

# DELETE
@famille_bp.route('/<int:id>', methods=['DELETE'])
def delete_famille(id):
    famille = Famille.query.get_or_404(id)
    db.session.delete(famille)
    db.session.commit()
    return jsonify({'message': 'Famille supprimée'}), 200
