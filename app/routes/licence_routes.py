from flask import Blueprint, current_app, request, jsonify
from datetime import datetime
from app.extensions import db
from app.models import Licence, Equipement
from app.models.association_tables import licence_equipement  # Import association table

licence_bp = Blueprint('licence', __name__, url_prefix='/api/licences')

# 🔧 Utilitaire pour parser les dates
def parse_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ").date()
    except ValueError:
        return datetime.strptime(date_str, "%Y-%m-%d").date()

# 🔹 Créer une licence
@licence_bp.route('/', methods=['POST'])
def create_licence():
    data = request.get_json()
    date_expiration = parse_date(data.get('date_expiration'))

    licence = Licence(
        designation=data.get('designation'),
        cle_licence=data.get('cle_licence'),
        periode=data.get('periode'),
        active=data.get('active', False),
        nombre_siestes=data.get('nombre_siestes'),
        date_expiration=date_expiration,
        id_famille=data.get('id_famille'),
        id_type=data.get('id_type')
    )

    equipement_ids = data.get('equipements', [])
    licence.equipements = [Equipement.query.get(eid) for eid in equipement_ids if Equipement.query.get(eid)]

    db.session.add(licence)
    db.session.commit()

    return jsonify({'message': 'Licence créée avec succès', 'id': licence.id_licence}), 201

# 🔹 Lire toutes les licences
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
            'equipements': [e.to_dict() for e in l.equipements]
        }
        for l in licences
    ])

# 🔹 Lire une licence par ID
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
        'equipements': [e.to_dict() for e in licence.equipements]
    })

@licence_bp.route('/<int:id>', methods=['PUT'])
def update_licence(id):
    licence = Licence.query.get_or_404(id)
    data = request.get_json()

    licence.designation = data.get('designation', licence.designation)
    licence.cle_licence = data.get('cle_licence', licence.cle_licence)
    licence.periode = data.get('periode', licence.periode)
    licence.active = data.get('active', licence.active)
    licence.nombre_siestes = data.get('nombre_siestes', licence.nombre_siestes)

    date_str = data.get('date_expiration')
    if date_str:
        licence.date_expiration = parse_date(date_str)

    licence.id_famille = data.get('id_famille', licence.id_famille)
    licence.id_type = data.get('id_type', licence.id_type)

    equipement_ids = data.get('equipements', [])
    licence.equipements = [Equipement.query.get(eid) for eid in equipement_ids if Equipement.query.get(eid)]

    db.session.commit()
    return jsonify({'message': 'Licence mise à jour'}), 200

# 🔹 Supprimer une licence
@licence_bp.route('/<int:id>', methods=['DELETE'])
def delete_licence(id):
    licence = Licence.query.get_or_404(id)
    db.session.delete(licence)
    db.session.commit()
    return jsonify({'message': 'Licence supprimée'}), 200

@licence_bp.route('/<int:id>/affecter-equipements', methods=['POST'])
def affect_equipement(id):
    licence = Licence.query.get_or_404(id)
    data = request.get_json()
    
    equipement_id = data.get('equipementId')
    if not equipement_id:
        return jsonify({'error': 'equipementId is required'}), 400
    
    equipement = Equipement.query.get(equipement_id)
    if not equipement:
        return jsonify({'error': 'Equipement not found'}), 404
    
    # Check if association already exists
    if equipement in licence.equipements:
        return jsonify({'error': 'This equipment is already associated'}), 400
    
    # Add the equipment
    licence.equipements.append(equipement)
    
    # Update seat count if needed
    if licence.nombre_siestes > 0:
        licence.nombre_siestes -= 1
    
    db.session.commit()
    
    return jsonify({
        'message': 'Equipment associated successfully',
        'licence': {
            'id': licence.id_licence,
            'nombre_siestes': licence.nombre_siestes,
            'equipements': [e.id_equipement for e in licence.equipements]
        }
    }), 200
@licence_bp.route('/by-equipement/<int:equipement_id>', methods=['GET'])
def get_licences_by_equipement(equipement_id):
    """Get all licences associated with a specific equipment"""
    try:
        # Verify equipment exists
        equipement = Equipement.query.get(equipement_id)
        if not equipement:
            return jsonify({'error': 'Equipment not found'}), 404
        
        # Get all licences associated with this equipment
        licences = Licence.query.join(
            licence_equipement,
            Licence.id_licence == licence_equipement.c.licence_id
        ).filter(
            licence_equipement.c.equipement_id == equipement_id
        ).all()
        
        return jsonify([licence.to_dict() for licence in licences]), 200
        
    except Exception as e:
        current_app.logger.error(f"Error fetching licences: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500