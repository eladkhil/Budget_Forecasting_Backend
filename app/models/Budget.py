from app.extensions import db

class Budget(db.Model):
    __tablename__ = 'Budgets'

    id = db.Column(db.Integer, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    cloture = db.Column(db.Boolean, default=False)
    total_budget = db.Column(db.Float, nullable=True)
    total_consommation = db.Column(db.Float, nullable=True)
    ecart = db.Column(db.Float, nullable=True)

    def __repr__(self):
        return f"<Budget {self.year} - Cloturé: {self.cloture}>"
