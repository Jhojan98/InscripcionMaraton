from flask import Flask, render_template, request, url_for, redirect, flash

from api_usuarios.cliente import UsuariosClient
from api_equipos.cliente import EquiposClient
from api_maraton.cliente import MaratonesClient 
from flask import Flask
import os
from flask_restful import Api
from api_usuarios.api import UsuarioResource,UsuarioIdResource,LoginResource
from api_equipos.api import EquipoResource,EquipoIdResource,EquipoUsuarioResource
from api_maraton.api import MaratonResource,MaratonIdResource
from main import app,db

import json
api = Api(app)

# Crear un cliente para las apis
clienteUsuarios = UsuariosClient("http://localhost:5000")
clienteEquipos = EquiposClient("http://localhost:5000")
clienteMaraton = MaratonesClient("http://localhost:5000")

api.add_resource(UsuarioResource, "/api/v1/usuarios")
api.add_resource(LoginResource, "/api/v1/login")
api.add_resource(UsuarioIdResource, "/api/v1/usuarios", "/api/v1/usuarios/<string:nombre>")
api.add_resource(EquipoResource, "/api/v3/equipos")
api.add_resource(EquipoIdResource, "/api/v3/equipos","/api/v1/equipos/<int:id>")
api.add_resource(EquipoUsuarioResource, "/api/v3/equipos", "/api/v1/equipos/<int:id_equipo>/<int:id_usuario>")
api.add_resource(MaratonResource, "/api/v2/maratones")
api.add_resource(MaratonIdResource, "/api/v2/maratones","/api/v1/maratones/<int:id>")


@app.route('/')
def index():

    usuarios =  clienteUsuarios.get_all_users()
    return render_template('index.html', usuarios=usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        message, category = clienteUsuarios.login_user(request.form['nombre'],request.form['password']) # Obtener el mensaje y la categoría del cliente
        if message == "El usuario y la contraseña son válidos":
            return render_template('auth/home.html')
        flash(message, category) # Usar el flash con el mensaje y la categoría
        return render_template('auth/login.html') # Renderizar el template HTML que muestra el mensaje flash
    return render_template('auth/login.html')


@app.route('/singup', methods=['GET', 'POST'])
def singup():
    if request.method == 'POST': 
        nombre = request.form['participante']
        correo = request.form['correo']
        #materia = request.form['materia']
        password = request.form['password']

        # Llamar al método create_user de tu instancia de cliente y pasarle los datos del formulario
        message, category = clienteUsuarios.create_user(nombre, correo, password, 1)
        if message == "El usuario fue creado con éxito":
            return redirect('/login')
        else:
            flash(message,category)
            return render_template('auth/singup.html')
    else:
        return render_template('auth/singup.html')

@app.route('/home')
def home():
    return render_template('home.html')
# El resto de las rutas son similares, solo cambia el método del cliente que se usa
if __name__ == "__main__":
    app.run(debug=True)
    