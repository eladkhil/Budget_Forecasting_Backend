from app.models.EmailConfig import EmailConfig
    
def load_email_config():
    config = EmailConfig.query.first()
    if config:
        return {
            "MAIL_SERVER": config.MAIL_SERVER,
            "MAIL_PORT": config.MAIL_PORT,
            "MAIL_USERNAME": config.MAIL_USERNAME,
            "MAIL_PASSWORD": config.MAIL_PASSWORD,
            "MAIL_USE_TLS": config.MAIL_USE_TLS,
            "MAIL_DEFAULT_SENDER": config.MAIL_DEFAULT_SENDER
        }
    return None