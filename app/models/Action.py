from app.extensions import db
from .ActionResponsable import action_responsable

class Action(db.Model):
    __tablename__ ="Action"
    action_id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    description=db.Column(db.String(255),nullable=False)
    statut=db.Column(db.String(20),nullable=False)
    date_limite = db.Column(db.Date, nullable=False)
    vul_id = db.Column(db.Integer, db.ForeignKey("Vuln.vul_id"))
    vuln = db.relationship("Vuln", backref="vulns")
    users = db.relationship('User',secondary=action_responsable,back_populates='actions')
