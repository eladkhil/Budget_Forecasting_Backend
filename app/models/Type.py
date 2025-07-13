from app.extensions import db

class Type(db.Model):
    __tablename__ = 'Type'
     
    id_type = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(100), nullable=False)

    licences = db.relationship('Licence', back_populates='type_objet', lazy=True)

    def to_dict(self):
        return {
            'id_type': self.id_type,
            'type': self.type
        }
