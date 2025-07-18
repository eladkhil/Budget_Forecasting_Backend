from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Equipement, Licence

equipement_bp = Blueprint('equipement', __name__, url_prefix='/api/equipements')

# GET all équipements avec licences liées
@equipement_bp.route('/', methods=['GET'])
def get_equipements():
    include_licences = request.args.get('include_licences', 'false').lower() == 'true'
    
    equipements = Equipement.query.all()
    
    return jsonify([
        e.to_dict(include_licences=include_licences)
        for e in equipements
    ])
# GET un équipement par ID avec licences liées
@equipement_bp.route('/<int:id>', methods=['GET'])
def get_equipement(id):
    equipement = Equipement.query.get_or_404(id)
    return jsonify(equipement.to_dict()), 200

# POST créer un équipement avec licences liées optionnelles
@equipement_bp.route('/', methods=['POST'])
def create_equipement():
    data = request.get_json()

    equipement = Equipement(
        nom=data.get('nom_equipement'),
        type_equipement=data.get('type_equipement'),
        description=data.get('description'),
        numero_serie=data.get('numero_serie')
    )

    licences_ids = data.get('licences_ids', [])
    if licences_ids:
        licences = Licence.query.filter(Licence.id_licence.in_(licences_ids)).all()
        equipement.licences = licences

    db.session.add(equipement)
    db.session.commit()

    return jsonify(equipement.to_dict()), 201

# PUT mettre à jour un équipement + licences liées optionnelles
@equipement_bp.route('/<int:id>', methods=['PUT'])
def update_equipement(id):
    equipement = Equipement.query.get_or_404(id)
    data = request.get_json()

    equipement.nom = data.get('nom_equipement', equipement.nom)
    equipement.type_equipement = data.get('type_equipement', equipement.type_equipement)
    equipement.description = data.get('description', equipement.description)
    equipement.numero_serie = data.get('numero_serie', equipement.numero_serie)

    licences_ids = data.get('licences_ids')
    if licences_ids is not None:
        licences = Licence.query.filter(Licence.id_licence.in_(licences_ids)).all()
        equipement.licences = licences

    db.session.commit()
    return jsonify(equipement.to_dict()), 200

# DELETE supprimer un équipement
@equipement_bp.route('/<int:id>', methods=['DELETE'])
def delete_equipement(id):
    equipement = Equipement.query.get_or_404(id)
    db.session.delete(equipement)
    db.session.commit()
    return jsonify({'message': 'Équipement supprimé'}), 200
