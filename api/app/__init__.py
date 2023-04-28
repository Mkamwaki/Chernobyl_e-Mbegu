from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_admin import Admin
from flask_migrate import Migrate

app = Flask(__name__)

app.config["SECRET_KEY"] = 'superstrongCHERNOBYLkey'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config["LOGIN_MANAGER_UNAUTHORIZED_VIEW"] = "/unauthorized"

CORS(app)
db = SQLAlchemy(app)

migrate = Migrate(app, db)

admin = Admin(app, name='Agriculture', template_mode='bootstrap4')

from app import views