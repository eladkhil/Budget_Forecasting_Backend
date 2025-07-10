from app.extensions import db

class Rubrique(db.Model):
    __tablename__ = 'Rubriques'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    direction_id = db.Column(db.Integer, db.ForeignKey('Directions.id'), nullable=False)

    def __repr__(self):
        return f"<Rubrique {self.name}>"
