from flask import request, Blueprint, jsonify
from database import db
import bcrypt
from Blueprints.user.user_models import User, UserSchema
from .helper_functions import pw_is_strong

user_bp = Blueprint('user', __name__)

@user_bp.route('/signup', methods=['POST'])
def signup():
    data = request.json
    full_name = data.get('full_name')
    username = data.get('username')
    password = data.get('password')
    if full_name=='' or username=='' or password=='':
        return jsonify({'error': 'All fields are required'}), 400
    if not pw_is_strong(password):
        return jsonify({'error': 'Choose a stronger password'}), 400
    salt = bcrypt.gensalt()
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), salt)

    new_user = User(full_name=full_name, username=username, password=hashed_pw)
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        error_message = str(e.orig)
        if 'UNIQUE' in error_message:
            error_message = 'Sorry, this username is taken'
        return jsonify({'error': error_message}), 400

    return jsonify({'message': 'user signed up'})

@user_bp.route('/get_all_users')
def get_all_users():
    users = User.query.all()
    userSchema = UserSchema()
    users = userSchema.dump(users, many=True)
    return jsonify(users)
    

@user_bp.route('/login')
def login():
    return jsonify({'message': 'login'})


