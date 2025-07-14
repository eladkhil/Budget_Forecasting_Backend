from app.extensions import db

class Role(db.Model):
    __tablename__ = "Role"
    role_id   = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    role_name = db.Column(db.String(50), unique=True, nullable=False)
