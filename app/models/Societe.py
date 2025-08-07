from app.extensions import db

class Societe(db.Model):
    __tablename__ = 'Societe'

    societe_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    adresse = db.Column(db.String(255), nullable=False)
    telephone_contact = db.Column(db.String(20), nullable=False)
    email_contact = db.Column(db.String(100), nullable=False)

    membres = db.relationship('Membre', back_populates='societe', cascade='all, delete')