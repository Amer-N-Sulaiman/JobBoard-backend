from database import db
from datetime import datetime
import marshmallow as ma
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    date_joined = db.Column(db.Date, default=datetime.utcnow)

class UserSchema(ma.Schema):
    id = ma.fields.Str()
    full_name = ma.fields.Str()
    username = ma.fields.Str()
    date_joined = ma.fields.Date()
