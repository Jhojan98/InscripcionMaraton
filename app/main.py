from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'gestion.db')
db = SQLAlchemy(app)

