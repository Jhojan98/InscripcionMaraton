from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_jwt_extended import JWTManager
base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'gestion.db')
db = SQLAlchemy(app)
app.secret_key = "secret"
app.config["JWT_SECRET_KEY"] = os.urandom(24) # Configurar una clave secreta para los tokens
jwt = JWTManager(app)
