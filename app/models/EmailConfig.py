from app.extensions import db

class EmailConfig(db.Model):
    __tablename__ ="EmailConfig"
    MAIL_ID = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    MAIL_SERVER = db.Column(db.String(100) ,nullable=False)
    MAIL_PORT = db.Column(db.Integer, default=587)
    MAIL_USERNAME = db.Column(db.String(120), nullable=False)
    MAIL_PASSWORD = db.Column(db.String(200), nullable=False)
    MAIL_USE_TLS = db.Column(db.Boolean, default=True)
    MAIL_DEFAULT_SENDER = db.Column(db.String(120))