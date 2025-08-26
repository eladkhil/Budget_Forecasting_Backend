from app.extensions import db


class Vuln(db.Model):
    __tablename__ ="Vuln"
    vul_id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    preuve = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)
    scenario = db.Column(db.Text, nullable=False)
    processus = db.Column(db.Text, nullable=False)
    impacts = db.Column(db.Text, nullable=False)
    niveau_impact = db.Column(db.String(20), nullable=False)
    complex_exploi = db.Column(db.String(20), nullable=False)
    proba = db.Column(db.String(50), nullable=False)
    criticite = db.Column(db.String(50), nullable=False)
    priorite_mise_oeuvre = db.Column(db.String(20), nullable=False)
    complex_mise_oeuvre = db.Column(db.String(20), nullable=False)
    audit_id = db.Column(db.Integer, db.ForeignKey('Audit.audit_id', ondelete="CASCADE"), nullable=False) 
    audit = db.relationship('Audit',  back_populates="vulns")
    actions = db.relationship("Action", back_populates="vuln", cascade="all, delete-orphan")
    def to_dict(self):
        data = {
            "vul_id": self.vul_id,
            "nom": self.nom,
            "description": self.description,
            "preuve": self.preuve,
            "type": self.type,
            "scenario": self.scenario,
            "processus": self.processus,
            "impacts": self.impacts,
            "niveau_impact": self.niveau_impact,
            "complex_exploi": self.complex_exploi,
            "proba": self.proba,
            "criticite": self.criticite,
            "complex_mise_oeuvre": self.complex_mise_oeuvre,
            "priorite_mise_oeuvre": self.priorite_mise_oeuvre
        }
        return data
