from app.extensions import db

class Direction(db.Model):
    __tablename__ = 'Directions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Direction {self.name}>"
