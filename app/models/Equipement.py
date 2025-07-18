from app.extensions import db



class Equipement(db.Model):
    __tablename__ = 'Equipement'
    id_equipement = db.Column(db.Integer, primary_key=True)
    type_equipement = db.Column(db.String)
    nom = db.Column(db.String)
    description = db.Column(db.String)
    numero_serie = db.Column(db.String)

    

    
    def to_dict(self, include_licences=False):
        data = {
        'id_equipement': self.id_equipement,
        'nom': self.nom,
        'type_equipement': self.type_equipement,
        'numero_serie': self.numero_serie,
        'description': self.description
    }
    
        if include_licences:
            data['licences'] = [l.to_dict() for l in self.licences]
    
        return data