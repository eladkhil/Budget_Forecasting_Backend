from app.extensions import db

class Famille(db.Model):
    __tablename__ = 'Famille'
    id_famille = db.Column(db.Integer, primary_key=True)
    nom_famille = db.Column(db.String(255), nullable=False)


    def to_dict(self):
        return {
            'id_famille': self.id_famille,
            'nom_famille': self.nom_famille,
        }
