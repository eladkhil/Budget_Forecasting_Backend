from app.extensions import db

class Equipement(db.Model):
    __tablename__ = 'Equipement'
    id_equipement = db.Column(db.Integer, primary_key=True)
    type_equipement = db.Column(db.String)
    nom = db.Column(db.String)  # matches DB column 'nom'
    description = db.Column(db.String)
    numero_serie = db.Column(db.String)

    licences = db.relationship('Licence', backref='equipement', lazy=True)
    def to_dict(self):
        return {
            'id_equipement': self.id_equipement,
            'type_equipement': self.type_equipement,
            'nom': self.nom,
            'description': self.description,
            'numero_serie': self.numero_serie,
        }
