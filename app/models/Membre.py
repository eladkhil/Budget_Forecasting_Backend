from app.extensions import db


class Membre(db.Model):
    __tablename__ = 'Membre'

    membre_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nom = db.Column(db.String(100), nullable=False)
    prenom = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    titre = db.Column(db.String(100),nullable=False)
    telephone = db.Column(db.String(20), nullable=False)
    typeMembre = db.Column(db.String(10), nullable=False)
    societe_id = db.Column(db.Integer, db.ForeignKey('Societe.societe_id', ondelete='CASCADE'))

    societe = db.relationship('Societe', back_populates='membres')
    audits = db.relationship('AuditMembre', back_populates='membre',cascade='all, delete')