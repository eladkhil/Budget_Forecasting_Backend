from app.extensions import db


class Vuln(db.Model):
    __tablename__ ="Vuln"
    vul_id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    nom = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    preuve = db.Column(db.Text, nullable=False)
    type = db.Column(db.Text, nullable=False)
    senario = db.Column(db.Text, nullable=False)
    processus = db.Column(db.Text, nullable=False)
    impacts = db.Column(db.Text, nullable=False)
    niveau_impact = db.Column(db.String(20), nullable=False)
    complex_exploi = db.Column(db.String(20), nullable=False)
    proba = db.Column(db.String(50), nullable=False)
    criticite = db.Column(db.String(50), nullable=False)
    priorite_mise_oeuvre = db.Column(db.String(20), nullable=False)
    complex_mise_oeuvre = db.Column(db.String(20), nullable=False)
    audit_id = db.Column(db.Integer, db.ForeignKey('Audit.audit_id'), nullable=False) 
    audit = db.relationship('Audit', backref='vulnerabilites')