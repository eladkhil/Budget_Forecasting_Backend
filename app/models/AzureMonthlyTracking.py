from app.extensions import db

class AzureMonthlyTracking(db.Model):
    __tablename__ = 'AzureMonthlyTracking'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    groupement_id = db.Column(db.Integer, db.ForeignKey('Groupements.id', ondelete="CASCADE"), nullable=False)
    mois = db.Column(db.String(20))
    periode = db.Column(db.String(50))
    fournisseur = db.Column(db.String(100))
    numero_facture = db.Column(db.String(50))

    reservation = db.Column(db.Numeric(12, 2), nullable=False)
    consommation = db.Column(db.Numeric(12, 2), nullable=False)

    # Computed columns in SQL Server, but calculated in Python/Flask ORM level
    tva_percent = db.Column(db.Numeric(5, 2), nullable=False)

    # These fields are normally calculated in SQL Server with PERSISTED columns,
    # but we will calculate them dynamically if needed (see below)
    montant_ht = db.column_property(reservation + consommation)
    montant_tva = db.column_property((reservation + consommation) * (tva_percent / 100))

    # Relationship (optional, if you want to use it in joins)
    groupement = db.relationship("Groupement", backref="azure_monthly_entries")

    def __repr__(self):
        return f"<AzureMonth {self.mois} | HT: {self.montant_ht} | TVA: {self.montant_tva}>"
