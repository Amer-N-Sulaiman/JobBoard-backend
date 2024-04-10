from flask import Blueprint, jsonify

user_bp = Blueprint('user', __name__)

user_bp.route('/signup')
def signup():
    return jsonify({'message': 'signup'})

user_bp.route('/login')
def login():
    return jsonify({'message': 'login'})