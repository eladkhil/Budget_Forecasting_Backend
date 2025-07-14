from app.extensions import ma
from app.models.Vuln import Vuln

class VulnSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Vuln
        load_instance = True