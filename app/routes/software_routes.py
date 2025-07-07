from flask import Blueprint, request, jsonify
from app.extensions import db
from datetime import datetime
from app.models.Software import Software
from sqlalchemy.exc import IntegrityError
bp_software = Blueprint("software", __name__, url_prefix="/api/software")


@bp_software.post("")
def create_software():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Name is required'}), 400
    
    software = Software(
        name=data['name'],
        vendor=data.get('vendor'),
        description=data.get('description'),
        website=data.get('website'),
        current_version=data.get('current_version')
    )
    
    try:
        db.session.add(software)
        db.session.commit()
        return jsonify(software.to_dict()), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({'error': 'Software with this name already exists'}), 409
@bp_software.get("")
def get_all_software():
    software_list = Software.query.all()
    return jsonify([s.to_dict() for s in software_list]), 200

@bp_software.get("/<int:software_id>")
def get_software(id):
    software = Software.query.get_or_404(id)
    return jsonify(software.to_dict()), 200

