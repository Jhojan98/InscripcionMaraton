from flask import request, jsonify
from flask_restful import  Resource,abort
from flask_marshmallow import Marshmallow
from main import db,app
from models import  equipo_schema,Equipo,Usuario,Integrante
from sqlalchemy.orm.exc import NoResultFound # Importar la excepción NoResultFound
from marshmallow.exceptions import ValidationError

class EquipoResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            
            existing_equipo = Equipo.query.filter_by(nombre=data.get("nombre",None)).first()
            miembro_equipo = Integrante.query.filter_by(usuario_id=data.get("lider_id",None)).first()
            existing_usuario = Usuario.query.filter_by(id=data.get("lider_id",None)).first()
            if not existing_usuario:
                return {"error": "No existe un usario con ese codigo"}, 400
            if miembro_equipo:
                return {"error": "El usuario ya pertenece a un equipo"}, 400
            if existing_equipo:
                return {"error": "Ya existe un equipo con el mismo nombre"}, 400
            lider_equipo =  Equipo.query.filter_by(lider_id=data.get("lider_id",None)).first()
            if lider_equipo:
                return {"error": "Ya existe un equipo con el usuario como lider"}, 400
            equipo = equipo_schema.load(data)
            equipo_model = Equipo(**equipo)
            db.session.add(equipo_model)
            db.session.commit()
            """
            equipoCreado = Equipo.query.filter_by(id=equipo_model.id).one()
            
            equipoCreado.usuarios.append(lider_equipo)
            db.session.commit()
            """
            #equipo = Equipo.query.filter_by(id=id_equipo).one() """
            return {"message": "El equipo fue creado con éxito"}, 201

        except ValidationError as e:
            return e.messages, 400

class EquipoIdResource(Resource):
    def get(self, id):
        try:
            equipo = Equipo.query.filter_by(id=id).one()
            result = equipo_schema.dump(equipo)
            return jsonify(result)
        except NoResultFound:
            abort(404, message="No se encontró el equipo con el id {}".format(id))
        except Exception as e:
            abort(500, message="Se produjo un error al procesar la solicitud")

    def put(self, id):
        data = request.get_json()
        nombre = data.get("nombre",None)
        lider_id = data.get("lider_id",None)
        maraton_id = data.get("maraton_id",None)
        estado_id = data.get("estado_id",None)
        try:
            equipo = Equipo.query.filter_by(id=id).one()
            if nombre:
                equipo.nombre = nombre
            if lider_id:
                equipo.lider_id = lider_id
            if maraton_id:
                equipo.maraton_id = maraton_id
            if estado_id:
                equipo.estado_id = estado_id
            db.session.commit()
            return jsonify({"mensaje": "El equipo {} fue actualizado con éxito".format(nombre)})
        except NoResultFound:
            abort(404, message="No se encontró el equipo con el id {}".format(id))
        except Exception as e:
            abort(500, message="Se produjo un error al procesar la solicitud")

    def delete(self, id):
        try:
            varid=id
            equipo = Equipo.query.filter_by(id=id).one()
            db.session.delete(equipo)
            db.session.commit()
            return jsonify({"mensaje": "El equipo con el id {} fue eliminado con éxito".format(varid)})
        except NoResultFound:
            abort(404, message="No se encontró el equipo con el id {}".format(varid))
        except Exception as e:
            abort(500, message="Se produjo un error al procesar la solicitud")
    
 #registrar_usuario   
class EquipoUsuarioResource(Resource):
    """
    def post(self, equipo_id, usuario_id):
        return  jsonify({"mensaje": "El equipo con el id {} fue recibido".format(equipo_id)})
    """
    def post(self, id_equipo, id_usuario):
        try:
            equipo = Equipo.query.filter_by(id=id_equipo).one()
            usuario = Usuario.query.filter_by(id=id_usuario).one()
            if usuario in equipo.usuarios:
                return {"error": "El usuario ya está registrado en el equipo"}, 400
            if len(equipo.usuarios) == 4:
                return {"error": "El equipo no tiene cupos disponibles"}, 400
            equipo.usuarios.append(usuario)
            if len(equipo.usuarios) == 4:
                equipo.estado_id = 2 # Estado completo
            db.session.commit()
            return {"message": "El usuario fue registrado con éxito en el equipo"}, 201
        except NoResultFound:
            abort(404, message="No se encontró el equipo o el usuario con los ids dados")
        except Exception as e:
            abort(500, message="Se produjo un error al procesar la solicitud")
    
    