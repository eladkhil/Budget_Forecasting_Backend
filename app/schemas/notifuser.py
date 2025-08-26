from app.extensions import ma
from app.models.NotifUser import NotifUser

class NotifUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=NotifUser
        load_instance = True
        include_fk = True