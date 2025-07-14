from app.extensions import db

class HorsBudget(db.Model):
    __tablename__ = 'HorsBudget'

    id = db.Column(db.Integer, primary_key=True)
    article = db.Column(db.String(255), nullable=False)
    prix_ht = db.Column(db.Float, nullable=False)
    qte = db.Column(db.Integer, nullable=False, default=1)
    fournisseur = db.Column(db.String(255))

    # Foreign keys
    budget_id = db.Column(db.Integer, db.ForeignKey('Budgets.id'), nullable=False)
    direction_id = db.Column(db.Integer, db.ForeignKey('Directions.id'), nullable=False)

    # Relationships
    budget = db.relationship('Budget', backref=db.backref('hors_budget_items', cascade="all, delete-orphan", lazy=True))
    direction = db.relationship('Direction', backref=db.backref('hors_budget_items', cascade="all, delete-orphan", lazy=True))

    def __repr__(self):
        return f"<HorsBudget article={self.article} prix_ht={self.prix_ht} qte={self.qte}>"
