from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://username:password@host/database'
db = SQLAlchemy(app)

class Numbers(db.Model):
    __tablename__ = 'numbers'
    id = db.Column(db.Integer, primary_key=True)
    num1 = db.Column(db.Integer)
    num2 = db.Column(db.Integer)
