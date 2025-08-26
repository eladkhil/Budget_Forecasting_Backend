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
        
        if "mail_server" in data and data["mail_server"]:
            config.mail_server = data["mail_server"]

        if "mail_port" in data and data["mail_port"]:
            config.mail_port = data["mail_port"]

        if "mail_username" in data and data["mail_username"]:
            config.mail_username = data["mail_username"]

        if "mail_password" in data and data["mail_password"]:
            config.mail_password = data["mail_password"]

        if "mail_use_tls" in data:
            mail_use_tls_val = data["mail_use_tls"]
        if isinstance(mail_use_tls_val, str):
            mail_use_tls_val = mail_use_tls_val.lower() in ('true', '1', 'yes')
        config.mail_use_tls = bool(mail_use_tls_val)
        if "mail_default_sender" in data and data["mail_default_sender"]:
            config.mail_default_sender = data["mail_default_sender"]
        if (ajout):
            db.session.add(config)
        db.session.commit()
        return jsonify({"message": "Configuré avec succès."})

    except Exception as e:
            db.session.rollback()
            print("Erreur:", e)
            abort(500, "Erreur") 
    


