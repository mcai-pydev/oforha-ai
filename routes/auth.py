from flask import Blueprint, request, jsonify
from models import User
from functools import wraps

auth = Blueprint('auth', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token is missing'}), 401
        
        # Remove 'Bearer ' prefix if present
        if token.startswith('Bearer '):
            token = token.split(' ')[1]
            
        payload = User.verify_token(token)
        if not payload:
            return jsonify({'message': 'Invalid or expired token'}), 401
            
        return f(*args, **kwargs)
    return decorated

@auth.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ['username', 'email', 'password']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Check if user already exists
    if User.find_by_email(data['email']):
        return jsonify({'message': 'Email already registered'}), 400
    if User.find_by_username(data['username']):
        return jsonify({'message': 'Username already taken'}), 400
    
    # Create new user
    user = User(
        username=data['username'],
        email=data['email'],
        password=data['password']
    )
    
    if user.save():
        # Generate token
        token = user.generate_token()
        return jsonify({
            'message': 'User created successfully',
            'token': token,
            'user': {
                'id': str(user._id),
                'username': user.username,
                'email': user.email
            }
        }), 201
    else:
        return jsonify({'message': 'Error creating user'}), 500

@auth.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Validate required fields
    if not all(k in data for k in ['email', 'password']):
        return jsonify({'message': 'Missing required fields'}), 400
    
    # Find user
    user = User.find_by_email(data['email'])
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    # Verify password
    if not user.verify_password(data['password']):
        return jsonify({'message': 'Invalid password'}), 401
    
    # Generate token
    token = user.generate_token()
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': {
            'id': str(user._id),
            'username': user.username,
            'email': user.email
        }
    })

@auth.route('/profile', methods=['GET'])
@token_required
def get_profile():
    token = request.headers.get('Authorization').split(' ')[1]
    payload = User.verify_token(token)
    
    user = User.find_by_email(payload['email'])
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({
        'user': {
            'id': str(user._id),
            'username': user.username,
            'email': user.email,
            'created_at': user.created_at
        }
    }) 