from app.extensions import db
from app.models.Notifications import Notifications
from app.schemas.notification import NotificationsSchema
from flask import Blueprint,request,jsonify,abort
from sqlalchemy import func,collate
bp_notif = Blueprint("notifs", __name__, url_prefix="/api/notifs")
notifs_schema=NotificationsSchema(many=True)
notif_schema  = NotificationsSchema()

"""@bp_notif.route("/<int:user_id>",methods=["GET"])
def get_notifications():
    notifications="""
