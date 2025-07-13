from app.extensions import db

class Fournisseur(db.Model):
    __tablename__ = 'Fournisseur'

    id_fournisseur = db.Column(db.Integer, primary_key=True)
    nom_fournisseur = db.Column(db.String(100), nullable=False)
    email_contact = db.Column(db.String(100))

    bons = db.relationship('BonLivraison', backref='fournisseur', lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id_fournisseur,
            'nom': self.nom_fournisseur,
            'email': self.email_contact
        }