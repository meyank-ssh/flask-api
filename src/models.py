from flask_sqlalchemy import SQLAlchemy
import bcrypt, uuid
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(15), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    referral_code = db.Column(db.String(10), unique=True, nullable=False)
    referred_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    referrals = db.relationship('User', backref=db.backref('referred_by', remote_side=[id]), lazy='dynamic')

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

    @staticmethod
    def generate_referral_code():
        return str(uuid.uuid4())[:8]
