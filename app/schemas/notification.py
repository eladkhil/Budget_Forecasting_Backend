from app.extensions import ma
from app.models.Notifications import Notifications

class NotificationsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=Notifications
        load_instance = True