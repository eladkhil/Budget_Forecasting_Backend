from app.extensions import ma
from app.models.Action import Action
from app.schemas.user import UserSchema

class ActionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Action
        load_instance = True
    users = ma.Nested(UserSchema, many=True)