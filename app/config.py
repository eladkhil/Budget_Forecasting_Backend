import os
import os, secrets

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(16))

class DevConfig(Config):
    # ───── SQL Server (already fine) ─────
    SERVER   = os.getenv("MSSQL_SERVER", "localhost")
    DATABASE = "Budget_forecasting"
    DRIVER   = "ODBC Driver 17 for SQL Server"
    USERNAME = os.getenv("MSSQL_USER", "")
    PASSWORD = os.getenv("MSSQL_PW",  "")
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}"
        f"?driver={DRIVER.replace(' ', '+')}"
    )

    # ───── SMTP settings (NEW) ─────
    # If you use Gmail:
    MAIL_SERVER   = "smtp.gmail.com"
    MAIL_PORT     = 587
    MAIL_USE_TLS  = True
    MAIL_USERNAME = os.getenv("SMTP_USER")      
    MAIL_PASSWORD = os.getenv("SMTP_PASS")      
    MAIL_DEFAULT_SENDER = MAIL_USERNAME

