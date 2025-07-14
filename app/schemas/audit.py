from app.extensions import ma
from app.models.Audit import Audit

class AuditSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=Audit
        load_instance = True
