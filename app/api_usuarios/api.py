# Importar las bibliotecas necesarias
from flask import request, jsonify
from flask_restful import  Resource,abort
from flask_marshmallow import Marshmallow
from main import db,app
from models import  Usuario,usuarios_schema,usuario_schema,Materia,Inscrito
from sqlalchemy.orm.exc import NoResultFound # Importar la excepción NoResultFound
from marshmallow.exceptions import ValidationError
from sqlalchemy.orm.exc import NoResultFound # Importar la excepción NoResultFound


class LoginResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            existing_user = Usuario.query.filter((Usuario.nombre == data.get("nombre",None)) | (Usuario.email == data.get("email",None))).first()
            if existing_user and existing_user.contraseña == data.get("contraseña",None):
                return {"message": "El usuario y la contraseña son válidos"}, 200
            else:
                return {"error": "El usuario o la contraseña son inválidos"}, 401

        except ValidationError as e:
            return e.messages, 400
        except NoResultFound:
            return {"error": "No se encontró el usuario con el nombre o el email proporcionados"}, 404
        except Exception as e:
            return {"error": "Se produjo un error al procesar la solicitud"}, 500

class InscritoResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            nombre = data.get("nombre",None)
            materia_id = data.get("materia",None)
            usuario = Usuario.query.filter_by(nombre=nombre).first()
            materia = Materia.query.filter_by(id=materia_id).first()
            inscrito = Inscrito(usuario=usuario.id, materia=materia.id)
            db.session.add(inscrito)
            db.session.commit()
            return {"message": "El usuario fue inscrito en la materia con éxito"}, 201
        except Exception as e:
            return {"error": "Se produjo un error al procesar la solicitud"}, 500
                
class UsuarioResource(Resource):
    def get(self):
        usuarios = Usuario.query.all()
        result = usuarios_schema.dump(usuarios)
        return jsonify(result)
    
    def post(self):
        try:
            data = request.get_json()
            nombre = data.get("nombre",None)
            email = data.get("email",None)
            contraseña = data.get("contraseña",None)
            tipo = data.get("tipo",None)
            if not nombre:
                 return {"message": "Falto el nombre"}, 400
            existing_user_name = Usuario.query.filter_by(nombre=data.get("nombre",None)).first()
            existing_user_email = Usuario.query.filter_by(email=data.get("email",None)).first()

            if existing_user_name:
                return {"message": "Ya existe un usuario con el mismo nombre"}, 400

            if existing_user_email:
                return {"message": "Ya existe un usuario con el mismo correo"}, 400
            
            
            usuario = usuario_schema.load(data)
            usuario_model = Usuario(**usuario)
            db.session.add(usuario_model)
            db.session.commit()
            
            return {"message": "El usuario fue creado con éxito"}, 200

        except ValidationError as e:
            return e.messages, 400

class UsuarioIdResource(Resource):
    def get(self, nombre):
        try:
            usuario = Usuario.query.filter_by(nombre=nombre).one()
            result = usuario_schema.dump(usuario)
            return jsonify(result)
        except NoResultFound:
            abort(404, message="No se encontró el usuario con el nombre {}".format(nombre))
        except Exception as e:
            abort(500, message="Se produjo un error al procesar la solicitud")

    def put(self, nombre):
        data = request.get_json()
        nombre = data.get("nombre",None)
        email = data.get("email",None)
        contraseña = data.get("contraseña",None)
        tipo = data.get("tipo",None)
        #if nombre and email and contraseña and tipo:
        try:
            usuario = Usuario.query.filter_by(nombre=nombre).one()
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
            abort(404, message="No se encontró el usuario con el nombre {}".format(nombre))
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
