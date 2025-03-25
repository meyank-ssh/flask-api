from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from src.models import db
from src.routes import Register, Login, Referrals, Health
from src.config import Config

app = Flask(__name__)
app.config.from_object(Config)

cors = CORS(app, resources={
    r"/api/*": {    
        "origins": Config.FRONTEND_URL.split(','),
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Range", "X-Content-Range"],
        "supports_credentials": True,
        "max_age": 120
    }
})

db.init_app(app)
api = Api(app)

with app.app_context():
    db.create_all()

api.add_resource(Register, '/api/register')
api.add_resource(Login, '/api/login')
api.add_resource(Referrals, '/api/referrals')
api.add_resource(Health, '/api/health')

if __name__ == '__main__':
    app.run(debug=True)