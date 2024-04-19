from flask import Flask, jsonify
from Blueprints.user.user import user_bp
from Blueprints.job.job import job_bp
from database import db
from flask_cors import CORS


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
app.config['SECRET_KEY'] = 'e7797ba6fcc64b5294a798fa798ece9f'

CORS(app)

db.init_app(app)
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(job_bp, url_prefix='/job')


@app.route('/')
def home():
    return jsonify({
        'message': 'Home'
    })
if __name__ == "__main__":
    app.run(debug=True)