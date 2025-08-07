from app.extensions import ma
from app.models.Membre import Membre
from app.schemas.societe import SocieteSchema

class MemberSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=Membre
        load_instance = True
        include_fk = True
    societe = ma.Nested(SocieteSchema, many=False)