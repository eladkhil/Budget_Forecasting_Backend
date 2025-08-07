from app.extensions import db


class AuditMembre(db.Model):
    __tablename__ = 'AuditMembre'

    audit_id = db.Column(db.Integer, db.ForeignKey('Audit.audit_id', ondelete='CASCADE'), primary_key=True)
    membre_id = db.Column(db.Integer, db.ForeignKey('Membre.membre_id', ondelete='CASCADE'), primary_key=True)

    audit = db.relationship('Audit', back_populates='membres')
    membre = db.relationship('Membre', back_populates='audits')
