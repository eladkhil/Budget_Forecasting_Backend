from app.extensions import db
class Software(db.Model):
    """Represents a software product that can be licensed"""
    __tablename__ = 'software'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    vendor = db.Column(db.String(100))
    description = db.Column(db.Text)
    website = db.Column(db.String(255))
    current_version = db.Column(db.String(50))
    
    licenses = db.relationship('License', back_populates='software', cascade='all, delete-orphan')
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'vendor': self.vendor,
            'description': self.description,
            'website': self.website,
            'current_version': self.current_version,
        }
    def __repr__(self):
        return f'<Software {self.name} ({self.id})>'
