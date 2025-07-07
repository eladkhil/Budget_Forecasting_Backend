from app.extensions import db
from datetime import datetime

class License(db.Model):
    
    __tablename__ = 'licenses'
    
    # License details
    id = db.Column(db.Integer, primary_key=True)
    license_key = db.Column(db.String(255), nullable=False)
    purchase_date = db.Column(db.Date)
    start_date = db.Column(db.Date)
    expiry_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)
    
    # Relationships
    software_id = db.Column(db.Integer, db.ForeignKey('software.id'), nullable=False)
    software = db.relationship('Software', back_populates='licenses')
    
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id'), nullable=False)
    user = db.relationship('User', back_populates='licenses')
    
    # For license type (perpetual, subscription, etc.)
    license_type = db.Column(db.String(50))
    seats = db.Column(db.Integer, default=1)  # For multi-seat licenses
    def to_dict(self):
        return {
        'id': self.id,
        'license_key': self.license_key,
        'software_id': self.software_id,
        'software_name': self.software.name if self.software else None,
        'user_id': self.user_id,
        'user_name': self.user.name if self.user else None,
        'purchase_date': self.purchase_date.isoformat() if self.purchase_date else None,
        'start_date': self.start_date.isoformat() if self.start_date else None,
        'expiry_date': self.expiry_date.isoformat() if self.expiry_date else None,
        'is_active': self.is_active,
        'notes': self.notes,
        'license_type': self.license_type,
        'seats': self.seats,
        
        
    }
    def __repr__(self):
        return f'<License {self.software.name} ({self.id})>'
    
    @property
    def days_until_expiry(self):
        if self.expiry_date:
            return (self.expiry_date - datetime.date.today()).days
        return None