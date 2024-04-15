from flask import request, Blueprint, jsonify
from database import db
import bcrypt
from Blueprints.user.user_models import User, UserSchema
from .helper_functions import pw_is_strong, create_jwt, verify_jwt

user_bp = Blueprint('user', __name__)

@user_bp.route('/signup', methods=['POST'])
def signup():

    # Retrieve Json data
    data = request.json
    full_name = data.get('full_name')
    is_employer = data.get('is_employer')
    username = data.get('username')
    password = data.get('password')

    # Check if any value is null
    if full_name=='' or username=='' or password=='':
        return jsonify({'error': 'All fields are required'}), 400
    
    # Make sure the password is trong enough
    if not pw_is_strong(password):
        return jsonify({'error': 'Choose a stronger password'}), 400
    
    # Hash the Password
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)

    # Create a user and save it to the db (with error handling)
    new_user = User(full_name=full_name, is_employer=is_employer, username=username, password=hashed_pw)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        error_message = str(e.orig)
        if 'UNIQUE' in error_message:
            error_message = 'Sorry, this username is taken'
        return jsonify({'error': error_message}), 400

    token = create_jwt(new_user.id)

    return jsonify({'token': token})

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'username does not exist'}), 401

    if not bcrypt.checkpw(password.encode('utf-8'), user.password):
        return jsonify({'error': 'wrong password'}), 401

    token = create_jwt(user.id)

    return jsonify({'token': token})

@user_bp.route('/get_all_users')
def get_all_users():
    users = User.query.all()
    userSchema = UserSchema()
    users = userSchema.dump(users, many=True)
    return jsonify(users)
    




