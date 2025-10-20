from app.extensions import db
from .ActionResponsable import action_responsable
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
class Action(db.Model):
    __tablename__ ="Action"
    action_id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    description=db.Column(db.String(255),nullable=False)
    statut=db.Column(db.String(20),nullable=False)
    date_limite = db.Column(db.Date, nullable=False)
    vul_id = db.Column(db.Integer, db.ForeignKey("Vuln.vul_id" ,ondelete="CASCADE"), nullable=False)
    vuln = db.relationship("Vuln", back_populates="actions")
    users = db.relationship('User',secondary=action_responsable,back_populates='actions')
    @hybrid_property
    def is_expired(self):
        today =datetime.utcnow().date()
        return self.date_limite and self.date_limite < today
    def auto_change(self):
        if self.statut == "Validée":
            return
        if self.is_expired:
            self.statut ="Cloturée"
        else:
            self.statut ="En cours"
