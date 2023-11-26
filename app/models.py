from main import db,app
from marshmallow import validate, Schema, fields
from flask_marshmallow import Marshmallow
from marshmallow import validate, Schema, fields

ma = Marshmallow(app)

# Tablas adicionales
class Tipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(16), unique=True, nullable=False)
    usuarios = db.relationship("Usuario", backref="tipo", lazy=True)
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "usuarios": [usuario.to_dict() for usuario in self.usuarios]
        }
class Estado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(16), unique=True, nullable=False)
    equipos = db.relationship("Equipo", backref="estado", lazy=True)
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "equipos": [equipo.to_dict() for equipo in self.equipos]
        }

class Nivel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(16), unique=True, nullable=False)
    maratones = db.relationship("Maraton", backref="nivel", lazy=True)
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "maratones": [maraton.to_dict() for maraton in self.maratones]
        }

class Materia(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), unique=True, nullable=False)
    nivel_id = db.Column(db.Integer, db.ForeignKey("nivel.id"), nullable=False) # Relación con la tabla Nivel
    usuarios = db.relationship("Usuario", secondary="inscrito", back_populates="materias")
    maratones = db.relationship("Maraton", backref="materia", lazy=True)
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "nivel": self.nivel.nombre, # Incluir el nombre del nivel
            "usuarios": [usuario.to_dict() for usuario in self.usuarios],
            "maratones": [maraton.to_dict() for maraton in self.maratones]
        }

class Inscrito(db.Model):
    materia = db.Column(db.Integer, db.ForeignKey("materia.id"), primary_key=True)
    usuario = db.Column(db.Integer, db.ForeignKey("usuario.id"), primary_key=True)
    def to_dict(self):
        return {
            "materia": self.materia,
            "usuario": self.usuario
        }

# Tablas originales
class Usuario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), unique=True, nullable=False)
    contraseña = db.Column(db.String(64), nullable=False)
    tipo_id = db.Column(db.Integer, db.ForeignKey("tipo.id"), nullable=False)
    equipos = db.relationship("Equipo", secondary="integrante", back_populates="usuarios")
    materias = db.relationship("Materia", secondary="inscrito", back_populates="usuarios")
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "email": self.email,
            "contraseña": self.contraseña,
            "tipo": self.tipo.nombre,
            "equipos": [equipo.to_dict() for equipo in self.equipos],
            "materias": [materia.nombre for materia in self.materias]
        }

class Equipo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), unique=True, nullable=False)
    lider_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), nullable=False)
    maraton_id = db.Column(db.Integer, db.ForeignKey("maraton.id"), nullable=False)
    estado_id = db.Column(db.Integer, db.ForeignKey("estado.id"), nullable=False)
    usuarios = db.relationship("Usuario", secondary="integrante", back_populates="equipos")
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "lider": self.lider.to_dict(),
            "maraton": self.maraton.to_dict(),
            "estado": self.estado.nombre,
            "usuarios": [usuario.to_dict() for usuario in self.usuarios]
        }


class Integrante(db.Model):
    equipo_id = db.Column(db.Integer, db.ForeignKey("equipo.id"), primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"), primary_key=True)

class Maraton(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(64), unique=True, nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    duracion = db.Column(db.Integer, nullable=False)
    nivel_id = db.Column(db.Integer, db.ForeignKey("nivel.id"), nullable=False)
    premio = db.Column(db.String(64), nullable=False)
    cupos = db.Column(db.Integer, nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey("materia.id"), nullable=False)
    equipos = db.relationship("Equipo", backref="maraton", lazy=True)
    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "fecha": self.fecha,
            "duracion": self.duracion,
            "nivel": self.nivel.nombre,
            "premio": self.premio,
            "cupos": self.cupos,
            "materia": self.materia.nombre,
            "equipos": [equipo.to_dict() for equipo in self.equipos]
        }


# Marshmallow Schemas
class TipoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'usuarios')

class EstadoSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'equipos')

class NivelSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'maratones')

class MateriaSchema(ma.Schema):
    class Meta:
        fields = ('id', 'nombre', 'usuarios', 'maratones')

class InscritoSchema(ma.Schema):
    class Meta:
        fields = ('materia_id', 'usuario_id')


class UsuarioSchema(Schema):
    nombre = fields.Str(required=True)
    email = fields.Email(required=True, unique=True)
    contraseña = fields.Str(required=True, validate=validate.Length(min=6))
    tipo_id = fields.Int(required=True, validate=validate.Range(min=1))

class EquipoSchema(Schema):
    nombre = fields.Str(required=True, unique=True)
    lider_id = fields.Int(required=True, validate=validate.Range(min=1))
    maraton_id = fields.Int(required=True, validate=validate.Range(min=1))
    estado_id = fields.Int(required=True, validate=validate.Range(min=1))

class IntegranteSchema(Schema):
    equipo_id = fields.Int(required=True, validate=validate.Range(min=1))
    usuario_id = fields.Int(required=True, validate=validate.Range(min=1))

class MaratonSchema(Schema):
    nombre = fields.Str(required=True, unique=True)
    fecha = fields.Date(required=True)
    duracion = fields.Int(required=True, validate=validate.Range(min=1))
    nivel_id = fields.Int(required=True, validate=validate.Range(min=1))
    premio = fields.Str(required=True)
    cupos = fields.Int(required=True, validate=validate.Range(min=1))

tipo_schema = TipoSchema()
tipos_schema = TipoSchema(many=True)

estado_schema = EstadoSchema()
estados_schema = EstadoSchema(many=True)

nivel_schema = NivelSchema()
niveles_schema = NivelSchema(many=True)

materia_schema = MateriaSchema()
materias_schema = MateriaSchema(many=True)

inscrito_schema = InscritoSchema()
inscritos_schema = InscritoSchema(many=True)

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

equipo_schema = EquipoSchema()
equipos_schema = EquipoSchema(many=True)

integrante_schema = IntegranteSchema()
integrantes_schema = IntegranteSchema(many=True)

maraton_schema = MaratonSchema()
maratones_schema = MaratonSchema(many=True)



