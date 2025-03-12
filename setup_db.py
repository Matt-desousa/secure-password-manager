from app import db, app
from models import User, PasswordEntry

with app.app_context():
    db.create_all()
    print('Database Initialized Successfully!')