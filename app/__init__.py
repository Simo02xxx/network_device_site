from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager
from config import Config
from flask_migrate import Migrate

db = SQLAlchemy()
csrf = CSRFProtect()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)  # Charge Config depuis config.py

    db.init_app(app)
    csrf.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    from .routes import main
    app.register_blueprint(main)

    from app.models import User 

    print("Base connectée :", app.config['SQLALCHEMY_DATABASE_URI'])

    return app