from app.extensions import ma
from app.models.EmailConfig import EmailConfig

class EmailConfigSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model=EmailConfig
        load_instance = True