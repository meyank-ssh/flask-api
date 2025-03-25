from flask import request, g
from functools import wraps
from src.utils import decode_token
from src.models import User

def jwt_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'error': 'Token missing'}, 401
        try:
            token = token.split(" ")[1]
            data = decode_token(token)
            user = User.query.get(data['user_id'])
            if not user:
                raise Exception('User not found')
            g.user = user
        except Exception as e:
            return {'error': f'Invalid or expired token: {str(e)}'}, 401
        return f(*args, **kwargs)
    return decorated
