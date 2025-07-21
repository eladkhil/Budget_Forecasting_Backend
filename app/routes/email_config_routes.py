from app.extensions import db
from app.models.EmailConfig import EmailConfig
from flask import Blueprint, jsonify,request,abort
from app.schemas.email_config import EmailConfigSchema


bp_email_config = Blueprint('email_config', __name__, url_prefix='/api/email-config')
email_schema =EmailConfigSchema()
@bp_email_config.get("")
def get_config():
    config=db.session.query(EmailConfig).first()
    if config:
        return email_schema.dump(config)
    return jsonify({"message": "Aucune configuration trouvée"}), 404

@bp_email_config.post("")
def create_update_config():
    ajout=False
    data = request.json or {}
    if not data:
        abort(400,"donnée json manquantes")
    try:
        config=db.session.query(EmailConfig).first()
        if not config:
            config = EmailConfig()
            ajout=True
        
        if "MAIL_SERVER" in data and data["MAIL_SERVER"]:
            config.MAIL_SERVER = data["MAIL_SERVER"]

        if "MAIL_PORT" in data and data["MAIL_PORT"]:
            config.MAIL_PORT = data["MAIL_PORT"]

        if "MAIL_USERNAME" in data and data["MAIL_USERNAME"]:
            config.MAIL_USERNAME = data["MAIL_USERNAME"]

        if "MAIL_PASSWORD" in data and data["MAIL_PASSWORD"]:
            config.MAIL_PASSWORD = data["MAIL_PASSWORD"]

        if "MAIL_USE_TLS" in data:
            mail_use_tls_val = data["MAIL_USE_TLS"]
        if isinstance(mail_use_tls_val, str):
            mail_use_tls_val = mail_use_tls_val.lower() in ('true', '1', 'yes')
        config.MAIL_USE_TLS = bool(mail_use_tls_val)
        if "MAIL_DEFAULT_SENDER" in data and data["MAIL_DEFAULT_SENDER"]:
            config.MAIL_DEFAULT_SENDER = data["MAIL_DEFAULT_SENDER"]
        if (ajout):
            db.session.add(config)
        db.session.commit()
        return jsonify({"message": "Configuré avec succès."})

    except Exception as e:
            db.session.rollback()
            print("Erreur:", e)
            abort(500, "Erreur") 
    


