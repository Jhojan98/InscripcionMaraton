# Importar las bibliotecas necesarias
from flask import request, jsonify
from flask_restful import  Resource
from main import db,app
from models import  Usuario


class Hello(Resource):
    def get(self):
        return {"message": "Hello, world!"}
    

# Definir la clase UsuarioResource que hereda de Resource
class UsuarioResource(Resource):
    def get(self, id):
        try:
            usuario = Usuario.query.get(id)
            if usuario:
                return {
                    "nombre": usuario.nombre,
                    "email": usuario.email,
                    "contraseña": usuario.contraseña,
                    "tipo": usuario.tipo,
                    # ... otros campos
                }, 200
            else:
                return jsonify({"error": "No se encontró el usuario con el id {}".format(id)}), 404
        except Exception as e:
            return jsonify({"error": "Se produjo un error al procesar la solicitud"}), 500
   
    def post(self):
        data = request.get_json()
        nombre = data.get("nombre")
        email = data.get("email")
        contraseña = data.get("contraseña")
        tipo = data.get("tipo")
        if nombre and email and contraseña and tipo:
            usuario = Usuario(nombre=nombre, email=email, contraseña=contraseña, tipo=tipo)
            db.session.add(usuario)
            db.session.commit()
            return jsonify({"mensaje": "El usuario {} fue creado con éxito".format(nombre)}), 201
        else:
            return jsonify({"error": "Los datos del usuario son inválidos"}), 400

    # Definir el método put para actualizar un usuario por su id
    def put(self, id):
        data = request.get_json()
        nombre = data.get("nombre")
        email = data.get("email")
        contraseña = data.get("contraseña")
        tipo = data.get("tipo")
        if nombre and email and contraseña and tipo:
            usuario = Usuario.query.get(id)
            if usuario:
                usuario.nombre = nombre
                usuario.email = email
                usuario.contraseña = contraseña
                usuario.tipo = tipo
                db.session.commit()
                return jsonify({"mensaje": "El usuario {} fue actualizado con éxito".format(nombre)}), 200
            else:
                return jsonify({"error": "No se encontró el usuario con el id {}".format(id)}), 404
        else:
            return jsonify({"error": "Los datos del usuario son inválidos"}), 400

    # Definir el método delete para eliminar un usuario por su id
    def delete(self, id):
        usuario = Usuario.query.get(id)
        if usuario:
            db.session.delete(usuario)
            db.session.commit()
            return jsonify({"mensaje": "El usuario {} fue eliminado con éxito".format(usuario.nombre)}), 200
        else:
            return jsonify({"error": "No se encontró el usuario con el id {}".format(id)}), 404

