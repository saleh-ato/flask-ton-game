from app import app,db
from datetime import datetime
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    login_required,
    logout_user,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
import re
from sqlalchemy.orm import validates

def is_valid_ton_address(wallet_address):
    pattern = r"^[A-Za-z0-9+/=]{48}$"  # Base64 TON format (approximate)
    return re.match(pattern, wallet_address)

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    wallet_address = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    @validates("wallet_address")
    def validate_wallet(self, key, wallet_address):
        if not is_valid_ton_address(wallet_address):  # Ensure function is defined!
            raise ValueError("Invalid TON wallet address!")
        return wallet_address

# Balance
class Balance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    coins = db.Column(db.Integer, default=0, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), unique=True, nullable=False)