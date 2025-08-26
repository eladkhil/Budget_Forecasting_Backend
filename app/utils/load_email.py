from app.models.EmailConfig import EmailConfig
    
def load_email_config():
    config = EmailConfig.query.first()
    if config:
        return {
            "mail_server": config.mail_server,
            "mail_port": config.mail_port,
            "mail_username": config.mail_username,
            "mail_password": config.mail_password,
            "mail_use_tls": config.mail_use_tls,
            "mail_default_sender": config.mail_default_sender
        }
    return None