from app.extensions import db


class NotifUser(db.Model):
    __tablename__ = 'NotifUser'

    notif_id = db.Column(db.Integer, db.ForeignKey('Notifications.notif_id', ondelete='CASCADE'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.user_id', ondelete='CASCADE'), primary_key=True)
    is_read = db.Column(db.Boolean, default=False)

    notification = db.relationship('Notifications', back_populates='notif_users')
    users = db.relationship('User', back_populates='notif_users')