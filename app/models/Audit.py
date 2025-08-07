from app.extensions import db

class Audit(db.Model):
    __tablename__ ="Audit"
    audit_id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    titre =db.Column(db.String(100),nullable=False)
    type=db.Column(db.String(50),nullable=False)
    date=db.Column(db.Date,nullable=False)
    description=db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey("User.user_id"))
    user = db.relationship("User", backref="audits")
    vulns = db.relationship("Vuln", back_populates="audit", cascade="all, delete-orphan")
    membres = db.relationship('AuditMembre', back_populates='audit',cascade='all, delete')

    def to_dict(self):
        data = {
            "audit_id": self.audit_id,
            "titre": self.titre,
            "type": self.type,
            "date":  self.date.isoformat(),
            "description": self.description,
            "user_id": self.user_id
        }
        return data
