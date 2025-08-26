from app.extensions import db
from app.models.Notifications import Notifications
from app.models.NotifUser import NotifUser
from app.schemas.notification import NotificationsSchema
from flask import Blueprint,jsonify,abort,request
bp_notif = Blueprint("notifs", __name__, url_prefix="/api/notifs")
notifs_schema=NotificationsSchema(many=True)
notif_schema  = NotificationsSchema()

@bp_notif.route("/<int:user_id>",methods=["GET"])
def get_notifications(user_id):
    notifications=Notifications.query.join(NotifUser).filter(NotifUser.user_id==user_id).order_by(Notifications.send_date.desc()).all()
    return jsonify([
        {
            "notif_id": n.notif_id,
            "title": n.title,
            "message": n.message,
            "send_date": n.send_date.isoformat(),
            "is_read":next((nu.is_read for nu in n.notif_users if nu.user_id==user_id),False)
        }
        for n in notifications]
    )
@bp_notif.put("read/<int:notif_id>")
def is_read(notif_id):
    user_id=request.args.get("user_id")
    if not user_id:
        abort(400,"not user_id")
    notif=NotifUser.query.filter_by(notif_id=notif_id,user_id=user_id).first()
    if not notif_id:
        abort(400,"not notification")
    try:
        notif.is_read=True
        db.session.commit()
        return jsonify({'message':'notifation est lue'}),200
    except Exception as e:
        db.session.rollback()
        abort(500,"erreur de lire la notification")
