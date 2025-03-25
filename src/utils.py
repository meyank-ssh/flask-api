import jwt
from datetime import datetime, timedelta
from src.config import Config

def generate_token(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + timedelta(days=1),
        'iat': datetime.utcnow()
    }
    return jwt.encode(payload, Config.JWT_SECRET_KEY, algorithm='HS256')

def decode_token(token):
    return jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
