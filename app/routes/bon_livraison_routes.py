from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import BonLivraison, Fournisseur, Licence

bon_bp = Blueprint('bon_livraison', __name__, url_prefix='/api/bons')

@bon_bp.route('/', methods=['POST'])
def create_bon():
    data = request.get_json()
    nom_bon_livraison = data.get('nom_bon_livraison')
    date = data.get('date')
    id_fournisseur = data.get('id_fournisseur')
    id_licence = data.get('id_licence')

    if not nom_bon_livraison or not id_fournisseur or not id_licence:
        return jsonify({'error': 'nom_bon_livraison, id_fournisseur et id_licence sont requis'}), 400

    if not Fournisseur.query.get(id_fournisseur):
        return jsonify({'error': 'Fournisseur introuvable'}), 404
    if not Licence.query.get(id_licence):
        return jsonify({'error': 'Licence introuvable'}), 404

    bon = BonLivraison(
        nom_bon_livraison=nom_bon_livraison,
        date=date,
        id_fournisseur=id_fournisseur,
        id_licence=id_licence
    )
    db.session.add(bon)
    db.session.commit()
    return jsonify({'id': bon.id_bon_livraison}), 201

@bon_bp.route('/', methods=['GET'])
def get_bons():
    bons = BonLivraison.query.all()
    return jsonify([
        {
            'id': b.id_bon_livraison,
            'nom_bon_livraison': b.nom_bon_livraison,
            'date': b.date.isoformat() if b.date else None,
            'id_fournisseur': b.id_fournisseur,
            'id_licence': b.id_licence
        } for b in bons
    ]), 200

@bon_bp.route('/<int:id>', methods=['GET'])
def get_bon(id):
    bon = BonLivraison.query.get_or_404(id)
    return jsonify({
        'id': bon.id_bon_livraison,
        'nom_bon_livraison': bon.nom_bon_livraison,
        'date': bon.date.isoformat() if bon.date else None,
        'id_fournisseur': bon.id_fournisseur,
        'id_licence': bon.id_licence
    })

@bon_bp.route('/<int:id>', methods=['PUT'])
def update_bon(id):
    bon = BonLivraison.query.get_or_404(id)
    data = request.get_json()

    bon.nom_bon_livraison = data.get('nom_bon_livraison', bon.nom_bon_livraison)
    bon.date = data.get('date', bon.date)

    if 'id_fournisseur' in data:
        if not Fournisseur.query.get(data['id_fournisseur']):
            return jsonify({'error': 'Fournisseur introuvable'}), 404
        bon.id_fournisseur = data['id_fournisseur']

    if 'id_licence' in data:
        if not Licence.query.get(data['id_licence']):
            return jsonify({'error': 'Licence introuvable'}), 404
        bon.id_licence = data['id_licence']

    db.session.commit()
    return jsonify({'message': 'Bon de livraison mis à jour'}), 200

@bon_bp.route('/<int:id>', methods=['DELETE'])
def delete_bon(id):
    bon = BonLivraison.query.get_or_404(id)
    db.session.delete(bon)
    db.session.commit()
    return jsonify({'message': 'Bon de livraison supprimé'}), 200
