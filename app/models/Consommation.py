from app.extensions import db

class Consommation(db.Model):
    __tablename__ = 'Consommations'

    id = db.Column(db.Integer, primary_key=True)
    groupement_id = db.Column(db.Integer, db.ForeignKey('Groupements.id'), nullable=False)
    montant = db.Column(db.Float, nullable=False)

    groupement = db.relationship('Groupement', backref=db.backref('consommations', lazy=True))

    def __repr__(self):
        return f"<Consommation Groupement {self.groupement_id} : {self.montant}>"
