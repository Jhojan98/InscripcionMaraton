from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from ..models import db, Usuario

def post(self):
    # Obtener los datos del usuario del cuerpo de la petición
    data = request.get_json()
    nombre = data.get("nombre")
    email = data.get("email")
    contraseña = data.get("contraseña")
    tipo = data.get("tipo")
    # Validar los datos y crear el usuario en la base de datos
    if nombre and email and contraseña and tipo:
        usuario = Usuario(nombre=nombre, email=email, contraseña=contraseña, tipo=tipo)
        db.session.add(usuario)
        db.session.commit()
        # Devolver una respuesta JSON con el código de estado y el mensaje apropiados
        return jsonify({"mensaje": "El usuario {} fue creado con éxito".format(nombre)}), 201
    else:
        # Devolver un mensaje de error si los datos son inválidos
        return jsonify({"error": "Los datos del usuario son inválidos"}), 400

def put(self, id):
    # Obtener los datos del usuario del cuerpo de la petición
    data = request.get_json()
    nombre = data.get("nombre")
    email = data.get("email")
    contraseña = data.get("contraseña")
    tipo = data.get("tipo")
    # Validar los datos y actualizar el usuario con el id dado en la base de datos
    if nombre and email and contraseña and tipo:
        usuario = Usuario.query.get(id)
        if usuario:
            usuario.nombre = nombre
            usuario.email = email
            usuario.contraseña = contraseña
            usuario.tipo = tipo
            db.session.commit()
            # Devolver una respuesta JSON con el código de estado y el mensaje apropiados
            return jsonify({"mensaje": "El usuario {} fue actualizado con éxito".format(nombre)}), 200
        else:
            # Devolver un mensaje de error si no existe el usuario
            return jsonify({"error": "No se encontró el usuario con el id {}".format(id)}), 404
    else:
        # Devolver un mensaje de error si los datos son inválidos
        return jsonify({"error": "Los datos del usuario son inválidos"}), 400

def delete(self, id):
    # Eliminar el usuario con el id dado de la base de datos
    usuario = Usuario.query.get(id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        # Devolver una respuesta JSON con el código de estado y el mensaje apropiados
        return jsonify({"mensaje": "El usuario {} fue eliminado con éxito".format(usuario.nombre)}), 200
    else:
        # Devolver un mensaje de error si no existe el usuario
        return jsonify({"error": "No se encontró el usuario con el id {}".format(id)}), 404
