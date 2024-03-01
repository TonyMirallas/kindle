from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from urllib.parse import quote_plus
from flask_jwt_extended import JWTManager

# ENV
load_dotenv()
app = Flask(__name__)

# SECRET KEY
secret_key = os.getenv('SECRET_KEY')
app.config['JWT_SECRET_KEY'] = secret_key
jwt = JWTManager(app)


# DATABASE
username = os.getenv('DB_USER')
password = quote_plus(os.getenv('DB_PASSWORD'))
database = os.getenv('DATABASE')
db_port = os.getenv('DB_PORT')

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{username}:{password}@localhost:{db_port}/{database}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# models only when we want to create the database
# from .models import KindleHighlight


with app.app_context():
    db.create_all()