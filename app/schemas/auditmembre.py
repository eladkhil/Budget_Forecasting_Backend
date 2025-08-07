from app.extensions import ma
from app.models.AuditMembre import AuditMembre

class AuditMembreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=AuditMembre
        load_instance = True
        include_fk = True
