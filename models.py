from app import db
from flask_login import UserMixin
from flask_bcrypt import Bcrypt
from cryptography.fernet import Fernet

bcrypt = Bcrypt()

key = Fernet.generate_key()
cipher = Fernet(key)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    

class PasswordEntry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    website = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    encrypted_password = db.Column(db.String(255), nullable=False)

    def encrypt_password(self, password):
        self.encrypted_password = cipher.encrypt(password.encode()).decode('utf-8')

    def decrypt_password(self):
        return cipher.decrypt(self.encrypted_password.encode()).decode('utf-8')