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
        
        
        return redirect(url_for('login'))
    else:
        return render_template('auth/login.html')

@app.route('/singup', methods=['GET', 'POST'])
def singup():
    if request.method == 'POST':
        try:
            participante = request.form['participante']
            correo = request.form['correo']
            materia = request.form['materia']
            password = request.form['password']
            
            print(f'Participante: {participante}')
            print(f'Correo: {correo}')
            print(f'Materia: {materia}')
            print(f'Contraseña: {password}')
            
            return render_template('auth/login.html')
        except KeyError as e:
            print(f"Error: {e}")    
    else:
        return render_template('auth/singup.html')

@app.route('/home')
def home():
    return render_template('home.html')
# El resto de las rutas son similares, solo cambia el método del cliente que se usa
if __name__ == "__main__":
    app.run(debug=True)
    