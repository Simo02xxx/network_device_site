import os

# Configuration Flask
class Config:
    # En prod, Railway injectera DATABASE_URL
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "postgresql://postgres:simokar123@localhost/new_network_site")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret_key")