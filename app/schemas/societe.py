from app.extensions import ma
from app.models.Societe import Societe

class SocieteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=Societe
        load_instance = True