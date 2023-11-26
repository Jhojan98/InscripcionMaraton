from flask import request, jsonify
from flask_restful import  Resource,abort
from flask_marshmallow import Marshmallow
from main import db,app
from models import  equipo_schema,Equipo
from sqlalchemy.orm.exc import NoResultFound # Importar la excepción NoResultFound
from marshmallow.exceptions import ValidationError

class EquipoResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            
            existing_equipo = Equipo.query.filter_by(nombre=data.get("nombre",None)).first()

            if existing_equipo:
                return {"error": "Ya existe un equipo con el mismo nombre"}, 400
            
            equipo = equipo_schema.load(data)
            equipo_model = Equipo(**equipo)
            db.session.add(equipo_model)
            db.session.commit()
            
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
