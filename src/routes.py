from flask_restful import Resource
from flask import request, g
from src.models import db, User
from src.utils import generate_token
from src.middleware import jwt_required

class Register(Resource):
    def post(self):
        data = request.json
        required_fields = ["email", "name", "mobile_number", "city", "password"]
        for field in required_fields:
            if not data.get(field):
                return {"error": f"{field} required"}, 400

        if User.query.filter_by(email=data['email']).first():
            return {"error": "Email already registered."}, 400

        referral_code = User.generate_referral_code()

        user = User(
            email=data['email'],
            name=data['name'],
            mobile_number=data['mobile_number'],
            city=data['city'],
            referral_code=referral_code,
        )
        user.set_password(data['password'])

        if data.get('referral_code'):
            referrer = User.query.filter_by(referral_code=data['referral_code']).first()
            if referrer:
                user.referred_by = referrer
            else:
                return {"error": "Invalid referral code."}, 400

        db.session.add(user)
        db.session.commit()

        return {"message": "Registered successfully", "referral_code": referral_code}, 201

class Login(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            token = generate_token(user.id)
            return {"token": token}, 200
        return {"error": "Invalid credentials"}, 401

class Referrals(Resource):
    @jwt_required
    def get(self):
        try:
            user=g.user
            referrals = user.referrals.all()
            result = [{
                "name": ref.name,
                "email": ref.email,
                "registration_date": ref.created_at.strftime('%Y-%m-%d %H:%M:%S')
            } for ref in referrals]
            return {"referrals": result}, 200
        except Exception as e:
            return {"error": str(e)}, 500

class Health(Resource):
    def get(self):
        return {"status": "ok"}, 200
    

