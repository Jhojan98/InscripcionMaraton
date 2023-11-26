from flask import request, jsonify
from flask_restful import  Resource,abort
from flask_marshmallow import Marshmallow
from main import db,app
from models import  Maraton,maraton_schema,Equipo
from sqlalchemy.orm.exc import NoResultFound # Importar la excepción NoResultFound
from marshmallow.exceptions import ValidationError

class MaratonResource(Resource):
    def post(self):
        try:
            data = request.get_json()
            
            existing_maraton = Maraton.query.filter_by(nombre=data.get("nombre",None)).first()

            if existing_maraton:
                return {"error": "Ya existe una maratón con el mismo nombre"}, 400
            
            maraton = maraton_schema.load(data)
            maraton_model = Maraton(**maraton)
            db.session.add(maraton_model)
            db.session.commit()
            
            return {"message": "La maratón fue creada con éxito"}, 201

        except ValidationError as e:
            return e.messages, 400

class MaratonIdResource(Resource):
    def get(self, id):
        try:
            maraton = Maraton.query.filter_by(id=id).one()
            result = maraton_schema.dump(maraton)
            return jsonify(result)
        except NoResultFound:
            abort(404, message="No se encontró la maratón con el id {}".format(id))
        except Exception as e:
            abort(500, message="Se produjo un error al procesar la solicitud")

    def put(self, id):
        data = request.get_json()
        nombre = data.get("nombre",None)
        fecha = data.get("fecha",None)
        duracion = data.get("duracion",None)
        nivel_id = data.get("nivel_id",None)
        premio = data.get("premio",None)
        cupos = data.get("cupos",None)
        materia_id = data.get("materia_id",None)
        try:
            maraton = Maraton.query.filter_by(id=id).one()
            if nombre:
                maraton.nombre = nombre
            if fecha:
                maraton.fecha = fecha
            if duracion:
                maraton.duracion = duracion
            if nivel_id:
                maraton.nivel_id = nivel_id
            if premio:
                maraton.premio = premio
            if cupos:
                maraton.cupos = cupos
            if materia_id:
                maraton.materia_id = materia_id
            db.session.commit()
            return jsonify({"mensaje": "La maratón {} fue actualizada con éxito".format(nombre)})
        except NoResultFound:
            abort(404, message="No se encontró la maratón con el id {}".format(id))
        except Exception as e:
            abort(500, message="Se produjo un error al procesar la solicitud")

    def delete(self, id):
        try:
            varid=id
            maraton = Maraton.query.filter_by(id=id).one()
            db.session.delete(maraton)
            db.session.commit()
            return jsonify({"mensaje": "La maratón {} fue eliminada con éxito".format(maraton.nombre)})
        except NoResultFound:
            abort(404, message="No se encontró la maratón con el id {}".format(varid))
        except Exception as e:
            abort(500, message="Se produjo un error al procesar la solicitud")

    
    def inscribir_equipo(self, equipo_id, maraton_id):
        try:
            equipo = Equipo.query.filter_by(id=equipo_id).one()
            maraton = Maraton.query.filter_by(id=maraton_id).one()
            if equipo.maraton_id is not None:
                return {"error": "El equipo ya está inscrito en otra maratón"}, 400
            if maraton.cupos == 0:
                return {"error": "La maratón no tiene cupos disponibles"}, 400
            for usuario in equipo.usuarios:
                if usuario.materias[0].nivel.nombre != maraton.nivel.nombre and usuario.materias[0].nivel.nombre != "Elite":
                    return {"error": "El equipo no cumple con el nivel requerido para la maratón"}, 400
            equipo.maraton_id = maraton_id
            maraton.cupos -= 1
            db.session.commit()
            return {"message": "El equipo fue inscrito con éxito en la maratón"}, 201
        except NoResultFound:
            abort(404, message="No se encontró el equipo o la maratón con los ids dados")
        except Exception as e:
            abort(500, message="Se produjo un error al procesar la solicitud")
