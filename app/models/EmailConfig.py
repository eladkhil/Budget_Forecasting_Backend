from app.extensions import db

class EmailConfig(db.Model):
    __tablename__ ="EmailConfig"
    mail_id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    mail_server = db.Column(db.String(100) ,nullable=False)
    mail_port = db.Column(db.Integer, default=587)
    mail_username = db.Column(db.String(120), nullable=False)
    mail_password = db.Column(db.String(200), nullable=False)
    mail_use_tls = db.Column(db.Boolean, default=True)
    mail_default_sender = db.Column(db.String(120))