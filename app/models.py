import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask

base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'gestion.db')
db = SQLAlchemy(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    contraseña = db.Column(db.String(64), nullable=False)
    tipo = db.Column(db.String(16), nullable=False, default="normal")
    equipos = db.relationship("Equipo", secondary="integrante", back_populates="usuarios")

class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), unique=True, nullable=False)
    lider = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    maraton = db.Column(db.Integer, db.ForeignKey("maraton.id"), nullable=False)
    estado = db.Column(db.String(16), nullable=False, default="pendiente")
    usuarios = db.relationship("Usuario", secondary="integrante", back_populates="equipos")

class Integrante(db.Model):
    equipo = db.Column(db.Integer, db.ForeignKey("equipo.id"), primary_key=True)
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), primary_key=True)

class Maraton(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), unique=True, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    duracion = db.Column(db.Integer, nullable=False)
    nivel = db.Column(db.String(16), nullable=False, default="principiante")
    premio = db.Column(db.String(64), nullable=False)
    cupos = db.Column(db.Integer, nullable=False)
"""
def create_tables():
    # Crea las tablas solo si no existen
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    create_tables()

"""