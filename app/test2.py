from flask import Flask, render_template, request, url_for, redirect, flash
from api_usuarios.cliente import UsuariosClient # Importar la clase UsuariosClient desde el archivo cliente.py
from flask import Flask
import os
from flask_restful import Api
from api_usuarios.api import UsuarioResource,Hello,UsuarioIdResource
from api_equipos.api import EquipoResource,EquipoIdResource,EquipoUsuarioResource
from api_maraton.api import MaratonResource,MaratonIdResource
from main import app,db
from api_usuarios.cliente import UsuariosClient
import json
api = Api(app)

# Crear un cliente para la API de usuarios
cliente = UsuariosClient("http://localhost:5000")
api.add_resource(UsuarioResource, "/api/v1/usuarios")
api.add_resource(UsuarioIdResource, "/api/v1/usuarios", "/api/v1/usuarios/<int:id>")
api.add_resource(Hello, "/api/v1/hello")


@app.route('/')
def index():

    usuarios =  cliente.get_all_users()
    return render_template('index.html', usuarios=usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            usuario = request.form['usuario']
            password = request.form['password']
            print(f"Usuario: {usuario}, Password: {password}")
            
            success_message = 'Bienvenido {}'.format(usuario)
            
            return render_template('auth/home.html')

        except KeyError as e:
            print(f"Error: {e}")
    else:
        return render_template('auth/login.html')


@app.route('/singup', methods=['GET', 'POST'])
def singup():
    if request.method == 'POST':
        try:
            participante1 = request.form['participante1']
            codigo1 = request.form['codigo1']
            materia1 = request.form['materia1']
            # Repite lo mismo para participante2, codigo2, materia2, participante3, codigo3, materia3, usuario, password
            
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
    