from app.extensions import db
from datetime import datetime

class Notifications(db.Model):
    __tablename__ ="Notifications"
    notif_id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    title=db.Column(db.String(255),nullable=False)
    message=db.Column(db.Text,nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    send_date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("User.user_id"))
    user = db.relationship("User", backref="notifications")