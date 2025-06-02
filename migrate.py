# migrate.py
from app import create_app, db
from app.models import User  # importe ici tous les modèles nécessaires

app = create_app()

# Flask-Migrate veut que `app` soit dans ce fichier
