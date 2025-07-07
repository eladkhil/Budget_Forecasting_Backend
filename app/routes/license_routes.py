
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.License import License
from app.models.Software import Software
from app.models.User import User
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from datetime import timedelta
bp_license = Blueprint("licenses", __name__, url_prefix="/api/licenses")
def validate_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str)
    except ValueError:
        return None



@bp_license.post("")
def create_license():
    data = request.get_json()
    
    required_fields = ['license_key', 'software_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    
    license = License(
        license_key=data['license_key'],
        software_id=data['software_id'],
        user_id=data.get('user_id'),
        purchase_date=validate_date(data.get('purchase_date')),
        start_date=validate_date(data.get('start_date')),
        expiry_date=validate_date(data.get('expiry_date')),
        is_active=data.get('is_active', True),
        notes=data.get('notes'),
        license_type=data.get('license_type'),
        seats=data.get('seats', 1)
    )
    
    try:
        db.session.add(license)
        db.session.commit()
        return jsonify(license.to_dict()), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
@bp_license.get("")
def get_all_licenses():
    licenses = License.query.all()
    return jsonify([l.to_dict() for l in licenses]), 200
@bp_license.get("/status/<string:status>")
def get_licenses_by_status(status):
    if status == 'active':
        licenses = License.query.filter_by(is_active=True).all()
    elif status == 'expired':
        licenses = License.query.filter(License.expiry_date < datetime.now().date()).all()
    elif status == 'expiring':
        licenses = License.query.filter(
            License.expiry_date >= datetime.now().date(),
            License.expiry_date <= (datetime.now() + timedelta(days=30)).date()
        ).all()
    else:
        return jsonify({'error': 'Invalid status'}), 400
    
    return jsonify([l.to_dict() for l in licenses]), 200

@bp_license.put("/<int:id>")
def update_license(id):
    license = License.query.get_or_404(id)
    data = request.get_json()
    
    if 'license_key' in data:
        license.license_key = data['license_key']
    if 'software_id' in data:
        license.software_id = data['software_id']
    if 'user_id' in data:
        license.user_id = data['user_id']
    if 'purchase_date' in data:
        license.purchase_date = validate_date(data['purchase_date'])
    if 'expiry_date' in data:
        license.expiry_date = validate_date(data['expiry_date'])
    if 'is_active' in data:
        license.is_active = data['is_active']
    if 'notes' in data:
        license.notes = data['notes']
    if 'license_type' in data:
        license.license_type = data['license_type']
    if 'seats' in data:
        license.seats = data['seats']
    
    try:
        db.session.commit()
        return jsonify(license.to_dict()), 200
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400