from flask_socketio import SocketIO
from app.models import Notifications
from app.extensions import db

socketio=SocketIO(cors_allowed_origins="*")
def emit_notification(event,data):
    socketio.emit(event,data)
def save_notification(user_id,title,message):
    notification=Notifications(
        user_id=user_id,
        title=title,
        message=message,
        is_read=False
    )
    db.session.add(notification)
    db.session.commit()