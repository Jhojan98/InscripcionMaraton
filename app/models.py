import os
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from main import db,app
from marshmallow import validate, Schema, fields
from flask_marshmallow import Marshmallow

#base_dir = os.path.abspath(os.path.dirname(__file__))
#app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'gestion.db')
#db = SQLAlchemy(app)
ma = Marshmallow(app)

class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    contraseña = db.Column(db.String(64), nullable=False)
    tipo = db.Column(db.String(16), nullable=False, default="normal")
    equipos = db.relationship("Equipo", secondary="integrante", back_populates="usuarios")
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "contraseña": self.contraseña,
            "tipo": self.tipo,
            "equipos": [equipo.to_dict() for equipo in self.equipos]
        }

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


# Marshmallow Schemas
#class UsuarioSchema(ma.Schema):
#    class Meta:
#        fields = ('id', 'nombre', 'email', 'contraseña', 'tipo')

class UsuarioSchema(Schema):
    nombre = fields.Str(required=True)
    email = fields.Email(required=True, unique=True)
    contraseña = fields.Str(required=True, validate=validate.Length(min=6))
    tipo = fields.Str(required=True, validate=validate.OneOf(["normal", "admin"]))


class EquipoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'lider', 'maraton', 'estado', 'usuarios')

class IntegranteSchema(ma.Schema):
    class Meta:
        fields = ('equipo_id', 'usuario_id')

class MaratonSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'fecha', 'duracion', 'nivel', 'premio', 'cupos')

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

equipo_schema = EquipoSchema()
equipos_schema = EquipoSchema(many=True)

integrante_schema = IntegranteSchema()
integrantes_schema = IntegranteSchema(many=True)

maraton_schema = MaratonSchema()
maratones_schema = MaratonSchema(many=True)
"""
def create_tables():
    # Crea las tablas solo si no existen
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    create_tables()

"""