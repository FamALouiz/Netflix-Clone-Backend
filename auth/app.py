from flask import request
from flask_restx import Namespace, Resource, fields

from models import User, Profile

auth_ns = Namespace('auth', description='Authentication related operations')

login_model = auth_ns.model('Login', {
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password'),
})

register_model = auth_ns.model('Register', {
    'email': fields.String(required=True, description='The user email'),
    'password': fields.String(required=True, description='The user password'),
    'firstName': fields.String(required=True, description='The user first name'),
    'lastName': fields.String(required=True, description='The user last name'),
})

@auth_ns.route('/login')
class LoginResource(Resource): 
    
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()['body']
        user = User.query.filter_by(email=data.get('email')).first()
        
        # Check if user exists
        if user is None: 
            return {'message': 'User not found'}, 404
        
        # Check if password is correct
        if user.password != data['password']: 
            return {'message': 'Invalid credentials'}, 401
        
        # Successful login
        return {'message': 'Login successful'}, 200

@auth_ns.route('/register')
class RegisterResource(Resource): 
    
    @auth_ns.expect(register_model)
    def post(self): 
        data = request.get_json()
        
        # Check if user exists
        user = User.query.filter_by(email=data['email']).first()
        
        if user is not None:
            return {'message': 'User already exists'}, 400
        
        # Create new user
        new_user = User(
            email=data['email'],
            password=data['password'],
        )
    
        new_user.save()
    
        new_first_profile = Profile(
            first_name=data['firstName'],
            last_name=data['lastName'],
            user_id = new_user.id
        )
        
        new_first_profile.save()
        
        new_user.update(profile_to_be_added=new_first_profile)
        
        return {'message': 'User created successfully'}, 201