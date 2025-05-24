# create_tables.py
from app import db, create_app

app = create_app()
with app.app_context():
    db.create_all()
    print("✅ Tables créées avec succès.")
