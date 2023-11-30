# Importar las bibliotecas necesarias
from flask import request, jsonify
from flask_restful import  Resource,abort
from flask_marshmallow import Marshmallow
from main import db,app
from models import  Usuario,usuarios_schema,usuario_schema
from sqlalchemy.orm.exc import NoResultFound # Importar la excepción NoResultFound
from marshmallow.exceptions import ValidationError

class Hello(Resource):
    def get(self):
        return {"message": "Hello, world!"}
    
class UsuarioResource(Resource):
    def get(self):
        usuarios = Usuario.query.all()
        result = usuarios_schema.dump(usuarios)
        return jsonify(result)
    
    def post(self):
        try:
            data = request.get_json()
            
            existing_user_name = Usuario.query.filter_by(nombre=data.get("nombre",None)).first()
            existing_user_email = Usuario.query.filter_by(email=data.get("email",None)).first()

            if existing_user_name:
                return {"error": "Ya existe un usuario con el mismo nombre"}, 400

            if existing_user_email:
                return {"error": "Ya existe un usuario con el mismo correo"}, 400
            
            print(data.get("nombre",None))
            usuario = usuario_schema.load(data)
            usuario_model = Usuario(**usuario)
            db.session.add(usuario_model)
            db.session.commit()
            
            return {"message": "El usuario fue creado con éxito"}, 201

        except ValidationError as e:
            return e.messages, 400

class UsuarioIdResource(Resource):
    def get(self, name):
        try:
            usuario = Usuario.query.filter_by(name=name).one()
            result = usuario_schema.dump(usuario)
            return jsonify(result)
        except NoResultFound:
            abort(404, message="No se encontró el usuario con el id {}".format(id))
        except Exception as e:
            abort(500, message="Se produjo un error al procesar la solicitud")

    def put(self, id):
        data = request.get_json()
        nombre = data.get("nombre",None)
        email = data.get("email",None)
        contraseña = data.get("contraseña",None)
        tipo = data.get("tipo",None)
        #if nombre and email and contraseña and tipo:
        try:
            usuario = Usuario.query.filter_by(id=id).one()
            if nombre:
                usuario.nombre = nombre
            if email:
                usuario.email = email
            if contraseña:
                usuario.contraseña = contraseña
            if tipo:
                usuario.tipo = tipo
            db.session.commit()
            return jsonify({"mensaje": "El usuario {} fue actualizado con éxito".format(nombre)})
        except NoResultFound:
            abort(404, message="No se encontró el usuario con el id {}".format(id))
        except Exception as e:
            abort(500, message="Se produjo un error al procesar la solicitud")
        #else:
        #    abort(400, message="Los datos del usuario son inválidos")

    def delete(self, id):
        try:
            varid=id
            usuario = Usuario.query.filter_by(id=id).one()
            db.session.delete(usuario)
            db.session.commit()
            return jsonify({"mensaje": "El usuario con el id {} fue eliminado con éxito".format(varid)})
        except NoResultFound:
            abort(404, message="No se encontró el usuario con el id {}".format(varid))
        except Exception as e:
            abort(500, message="Se produjo un error al procesar la solicitud")
