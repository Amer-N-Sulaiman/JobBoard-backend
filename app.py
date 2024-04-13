from flask import Flask
from Blueprints.user.user import user_bp
from database import db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db.init_app(app)
app.register_blueprint(user_bp, url_prefix='/user')

if __name__ == "__main__":
    app.run(debug=True)