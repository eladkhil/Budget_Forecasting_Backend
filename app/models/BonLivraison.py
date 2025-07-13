from app.extensions import db

class BonLivraison(db.Model):
    __tablename__ = 'Bon_livraison'
    __table_args__ = {'schema': 'dbo'}

    id_bon_livraison = db.Column(db.Integer, primary_key=True)
    nom_bon_livraison = db.Column(db.String(100))
    date = db.Column(db.Date)

    # Clés étrangères
    id_fournisseur = db.Column(db.Integer, db.ForeignKey('Fournisseur.id_fournisseur'))
    id_licence = db.Column(db.Integer, db.ForeignKey('Licence.id_licence'))