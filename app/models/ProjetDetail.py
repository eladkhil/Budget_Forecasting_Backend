from app.extensions import db

class ProjetDetail(db.Model):
    __tablename__ = 'ProjetDetails'

    id = db.Column(db.Integer, primary_key=True)
    groupement_id = db.Column(db.Integer, db.ForeignKey('Groupements.id'), nullable=False)
    type = db.Column(db.String(100), nullable=False)  # e.g., "Formation", "Services", "Fonctionnement"
    montant = db.Column(db.Float, nullable=False)
    montant_consomme = db.Column(db.Float, nullable=True) 
    # Relationship with Groupement
    groupement = db.relationship('Groupement', backref=db.backref('details', lazy=True, cascade="all, delete-orphan"))

    def __repr__(self):
        return f"<ProjetDetail {self.type} - Montant: {self.montant}>"
