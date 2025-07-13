from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models import Licence, Famille, Equipement

licence_bp = Blueprint('licence', __name__, url_prefix='/api/licences')

# CREATE
@licence_bp.route('/', methods=['POST'])
def create_licence():
    data = request.get_json()
    designation = data.get('designation')
    cle_licence = data.get('cle_licence')
    periode = data.get('periode')
    active = data.get('active', True)
    nombre_siestes = data.get('nombre_siestes')
    date_expiration = data.get('date_expiration')
    id_famille = data.get('id_famille')
    id_type = data.get('id_type')
    id_equipements = data.get('id_equipements')

    # Vérification des champs obligatoires
    if not designation or not cle_licence:
        return jsonify({'error': 'Designation et clé de licence sont requis.'}), 400

    licence = Licence(
        designation=designation,
        cle_licence=cle_licence,
        periode=periode,
        active=active,
        nombre_siestes=nombre_siestes,
        date_expiration=date_expiration,
        id_famille=id_famille,
        id_type=id_type,
        id_equipements=id_equipements
    )

    db.session.add(licence)
    db.session.commit()
    return jsonify({'id': licence.id_licence}), 201

# READ ALL
@licence_bp.route('/', methods=['GET'])
def get_licences():
    licences = Licence.query.all()
    return jsonify([
        {
            'id': l.id_licence,
            'designation': l.designation,
            'cle_licence': l.cle_licence,
            'periode': l.periode,
            'active': l.active,
            'nombre_siestes': l.nombre_siestes,
            'date_expiration': l.date_expiration.isoformat() if l.date_expiration else None,
            'id_famille': l.id_famille,
            'id_type': l.id_type,
            'id_equipements': l.id_equipements
        } for l in licences
    ])

# READ ONE
@licence_bp.route('/<int:id>', methods=['GET'])
def get_licence(id):
    licence = Licence.query.get_or_404(id)
    return jsonify({
        'id': licence.id_licence,
        'designation': licence.designation,
        'cle_licence': licence.cle_licence,
        'periode': licence.periode,
        'active': licence.active,
        'nombre_siestes': licence.nombre_siestes,
        'date_expiration': licence.date_expiration.isoformat() if licence.date_expiration else None,
        'id_famille': licence.id_famille,
        'id_type': licence.id_type,
        'id_equipements': licence.id_equipements
    })

# UPDATE
@licence_bp.route('/<int:id>', methods=['PUT'])
def update_licence(id):
    licence = Licence.query.get_or_404(id)
    data = request.get_json()

    licence.designation = data.get('designation', licence.designation)
    licence.cle_licence = data.get('cle_licence', licence.cle_licence)
    licence.periode = data.get('periode', licence.periode)
    licence.active = data.get('active', licence.active)
    licence.nombre_siestes = data.get('nombre_siestes', licence.nombre_siestes)
    licence.date_expiration = data.get('date_expiration', licence.date_expiration)
    licence.id_famille = data.get('id_famille', licence.id_famille)
    licence.id_type = data.get('id_type', licence.id_type)
    licence.id_equipements = data.get('id_equipements', licence.id_equipements)

    db.session.commit()
    return jsonify({'message': 'Licence mise à jour'}), 200

# DELETE
@licence_bp.route('/<int:id>', methods=['DELETE'])
def delete_licence(id):
    licence = Licence.query.get_or_404(id)
    db.session.delete(licence)
    db.session.commit()
    return jsonify({'message': 'Licence supprimée'}), 200
