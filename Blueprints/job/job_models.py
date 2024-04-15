from database import db
from datetime import datetime
import marshmallow as ma

class Job(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    body = db.Column(db.String(250), nullable=False)
    posted_by = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.Date, default=datetime.utcnow)

class JobSchema(ma.Schema):
    id = ma.fields.Str()
    title = ma.fields.Str()
    body = ma.fields.Str()
    posted_by = ma.fields.Str()
    date_posted = ma.fields.Date()
