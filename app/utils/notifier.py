from flask_socketio import SocketIO
from app.models.Notifications import Notifications
from app.extensions import db
from app.models.NotifUser import NotifUser

socketio=SocketIO(
    cors_allowed_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    logger=True,
    engineio_logger=True
    )
def emit_notification(event,data):
    socketio.emit(event,data)
def save_notification(user_ids,title,message):
    try:
        notification=Notifications(
            title=title,
            message=message,
        )
        db.session.add(notification)
        db.session.flush()
        for user_id in user_ids:
            notif_user=NotifUser(
                notif_id=notification.notif_id,
                user_id=user_id,
                is_read=False
            )
            db.session.add(notif_user)
        db.session.commit()
        return notification
    except Exception as e:
        db.session.rollback()
        return None
