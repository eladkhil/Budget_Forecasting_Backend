from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from .ActionResponsable import action_responsable
class User(db.Model):
    __tablename__ = "User"
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    name      = db.Column(db.String(64))
    surname   = db.Column(db.String(64))
    email     = db.Column(db.String(120), unique=True, nullable=False)
    phone     = db.Column(db.String(32))
    role_id = db.Column(db.Integer, db.ForeignKey("Role.role_id"))
    role = db.relationship("Role", backref="users")
    password_hash     = db.Column(db.String(256), nullable=False)
    password_expires  = db.Column(db.DateTime)
    reset_code = db.Column(db.String(6), nullable=True)
    reset_expires = db.Column(db.DateTime, nullable=True)
    actions = db.relationship('Action',secondary=action_responsable,back_populates='users')
    notif_users = db.relationship("NotifUser", back_populates="users", cascade="all, delete-orphan")

    def to_dict(self, include_email=True):
        """Return a serialisable dict WITHOUT the password hash."""
        data = {
            "user_id":  self.user_id,
            "username": self.username,
            "name":     self.name,
            "surname":  self.surname,
            "phone":    self.phone,
            "role_id":  self.role_id,
            "role_name": self.role.role_name if self.role else None,
            "password_expires": (
                self.password_expires.isoformat() if self.password_expires else None
            ),
        }
        if include_email:
            data["email"] = self.email
        return data

    # helpers
    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password_hash, raw)
