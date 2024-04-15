import re
import jwt
import datetime
from flask import current_app

def pw_is_strong(password):
    # define our regex pattern for validation
    pattern = r"^(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}$"

    # We use the re.match function to test the password against the pattern
    match = re.match(pattern, password)

    # return True if the password matches the pattern, False otherwise
    return bool(match)

def create_jwt(user_id):
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=5)  # Token expiry time
    }
    secret_key = current_app.config['SECRET_KEY']
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    return token

def verify_jwt(token):
    secret_key = current_app.config['SECRET_KEY']  # Same key as used in creation
    try:
        payload = jwt.decode(token, secret_key, algorithms=['HS256'])
        return payload  # Returns the payload if verification is successful
    except jwt.ExpiredSignatureError:
        return {'error': 'token expired'}
    except jwt.InvalidTokenError:
        return {'error': 'invalid token'}  # Token is invalid