from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Fournisseur

fournisseur_bp = Blueprint('fournisseur', __name__, url_prefix='/api/fournisseurs')

# CREATE
@fournisseur_bp.route('/', methods=['POST'])
def create_fournisseur():
    data = request.get_json()
    nom = data.get('nom_fournisseur')
    email = data.get('email_contact')

    if not nom:
        return jsonify({'error': 'Le nom du fournisseur est requis.'}), 400

    fournisseur = Fournisseur(nom_fournisseur=nom, email_contact=email)
    db.session.add(fournisseur)
    db.session.commit()
    return jsonify(fournisseur.to_dict()), 201

# READ ALL
@fournisseur_bp.route('/', methods=['GET'])
def get_fournisseurs():
    fournisseurs = Fournisseur.query.all()
    return jsonify([f.to_dict() for f in fournisseurs]), 200

# READ ONE
@fournisseur_bp.route('/<int:id>', methods=['GET'])
def get_fournisseur(id):
    fournisseur = Fournisseur.query.get_or_404(id)
    return jsonify(fournisseur.to_dict()), 200

# UPDATE
@fournisseur_bp.route('/<int:id>', methods=['PUT'])
def update_fournisseur(id):
    fournisseur = Fournisseur.query.get_or_404(id)
    data = request.get_json()
    fournisseur.nom_fournisseur = data.get('nom_fournisseur', fournisseur.nom_fournisseur)
    fournisseur.email_contact = data.get('email_contact', fournisseur.email_contact)
    db.session.commit()
    return jsonify(fournisseur.to_dict()), 200

# DELETE
@fournisseur_bp.route('/<int:id>', methods=['DELETE'])
def delete_fournisseur(id):
    fournisseur = Fournisseur.query.get_or_404(id)
    db.session.delete(fournisseur)
    db.session.commit()
    return jsonify({'message': 'Fournisseur supprimé'}), 200
