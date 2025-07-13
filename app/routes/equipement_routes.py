from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Equipement, Famille

equipement_bp = Blueprint('equipement', __name__, url_prefix='/api/equipements')

# CREATE
@equipement_bp.route('/', methods=['POST'])
def create_equipement():
    data = request.get_json()
    nom = data.get('nom_equipement')
    type_equipement = data.get('type_equipement')
    description = data.get('description')
    numero_serie = data.get('numero_serie')

    equipement = Equipement(
        nom=nom,
        type_equipement=type_equipement,
        description=description,
        numero_serie=numero_serie
    )
    db.session.add(equipement)
    db.session.commit()
    return jsonify(equipement.to_dict()), 201

# READ ALL
@equipement_bp.route('/', methods=['GET'])
def get_equipements():
    equipements = Equipement.query.all()
    return jsonify([e.to_dict() for e in equipements]), 200

# READ ONE
@equipement_bp.route('/<int:id>', methods=['GET'])
def get_equipement(id):
    equipement = Equipement.query.get_or_404(id)
    return jsonify(equipement.to_dict()), 200

# UPDATE
@equipement_bp.route('/<int:id>', methods=['PUT'])
def update_equipement(id):
    equipement = Equipement.query.get_or_404(id)
    data = request.get_json()
    equipement.nom = data.get('nom_equipement', equipement.nom)
    equipement.type_equipement = data.get('type_equipement', equipement.type_equipement)
    equipement.description = data.get('description', equipement.description)
    equipement.numero_serie = data.get('numero_serie', equipement.numero_serie)
    db.session.commit()
    return jsonify(equipement.to_dict()), 200

# DELETE
@equipement_bp.route('/<int:id>', methods=['DELETE'])
def delete_equipement(id):
    equipement = Equipement.query.get_or_404(id)
    db.session.delete(equipement)
    db.session.commit()
    return jsonify({'message': 'Équipement supprimé'}), 200
