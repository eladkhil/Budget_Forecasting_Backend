from app.extensions import db
from app.models.association_tables import licence_equipement  # Import instead of redefine

class Licence(db.Model):
    __tablename__ = 'Licence'

    id_licence = db.Column(db.Integer, primary_key=True)
    designation = db.Column(db.String(100), nullable=False)
    cle_licence = db.Column(db.String(100), unique=True)
    periode = db.Column(db.String(50))
    active = db.Column(db.Boolean, default=True)
    nombre_siestes = db.Column(db.Integer)
    date_expiration = db.Column(db.Date)

    id_famille = db.Column(db.Integer, db.ForeignKey('Famille.id_famille'))
    id_type = db.Column(db.Integer, db.ForeignKey('Type.id_type'))

    bons_livraison = db.relationship('BonLivraison', backref='licence', lazy=True)
    famille = db.relationship('Famille', backref='licences', lazy=True)
    type_objet = db.relationship('Type', back_populates='licences')

    # Many-to-many with Equipement
    equipements = db.relationship(
        'Equipement',
        secondary='licence_equipement',
        backref='_licences',
        overlaps="_licences"
    )

    def to_dict(self):
        return {
            'id_licence': self.id_licence,
            'designation': self.designation,
            'cle_licence': self.cle_licence,
            'periode': self.periode,
            'active': self.active,
            'nombre_siestes': self.nombre_siestes,
            'date_expiration': self.date_expiration.isoformat() if self.date_expiration else None,
            'id_famille': self.id_famille,
            'id_type': self.id_type,
            'equipements': [e.to_dict() for e in self.equipements]
        }
