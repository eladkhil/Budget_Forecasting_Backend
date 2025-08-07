import os, secrets
from urllib.parse import quote_plus

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", secrets.token_hex(16))#essentiel pour chiffrer secret_key

class DevConfig(Config):
    """# ───── SQL Server (already fine) ─────
    SERVER   = os.getenv("MSSQL_SERVER", "localhost\\SQLEXPRESS")
    DATABASE = "Budget_forecasting"
    DRIVER   = "ODBC Driver 17 for SQL Server"
    USERNAME = os.getenv("MSSQL_USER", "")
    PASSWORD = os.getenv("MSSQL_PW",  "")
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}"
        f"?driver={DRIVER.replace(' ', '+')}"
    )"""
    # Chaîne de connexion SQL Server
    SERVER   = os.getenv("MSSQL_SERVER","DESKTOP-10I83NK")
    DATABASE = os.getenv("MSSQL_DATABASE","AuditBase")
    DRIVER   = os.getenv("MSSQL_DRIVER","ODBC Driver 17 for SQL Server")
    TRUSTED = os.getenv("MSSQL_TRUSTED","yes")
    if TRUSTED.lower()=="yes":
        params = quote_plus(
            f"DRIVER={{{DRIVER}}};"
            f"SERVER={SERVER};"   
            f"DATABASE={DATABASE};"
            f"Trusted_Connection=yes"
        )
    SQLALCHEMY_DATABASE_URI = (f"mssql+pyodbc:///?odbc_connect={params}")



