from app.extensions import db
from datetime import datetime
class Notifications(db.Model):
    __tablename__ ="Notifications"
    notif_id = db.Column(db.Integer, primary_key=True, index=True, autoincrement=True)
    title=db.Column(db.String(255),nullable=False)
    message=db.Column(db.Text,nullable=False)
    send_date = db.Column(db.DateTime, default=datetime.utcnow)
    notif_users = db.relationship("NotifUser", back_populates="notification", cascade="all, delete-orphan")

