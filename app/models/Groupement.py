from app.extensions import db

class Groupement(db.Model):
    __tablename__ = 'Groupements'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rubrique_id = db.Column(db.Integer, db.ForeignKey('Rubriques.id'), nullable=False)
    budget_alloue = db.Column(db.Float, nullable=True)
    budget_consomme = db.Column(db.Float, nullable=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('Budgets.id'), nullable=True)
    ecart = db.Column(db.Float, default=0)
    def __repr__(self):
        return f"<Groupement {self.name}>"
