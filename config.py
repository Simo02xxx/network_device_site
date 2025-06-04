import os

# Configuration Flask
class Config:
    # En prod, Railway injectera DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://postgres:simokar123@localhost/new_network_site")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key")
    MAIL_SERVER = 'smtp.gmail.com'

    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = ''    # ton email d’envoi
    MAIL_PASSWORD = ''   # mot de passe ou mot de passe d’application
    SECRET_KEY = 'une_clef_secrete_pour_token'  # déjà présent normalement
