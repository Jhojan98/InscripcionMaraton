from flask import Flask
import os
from flask_restful import Api
from api_usuarios.api import UsuarioResource,Hello,UsuarioIdResource # Importar el módulo api_usuarios
from main import app,db

"""
# Crear la aplicación de Flask
base_dir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_dir, 'gestion.db')
# Crear la instancia de Api

"""
api = Api(app)
# Añadir el recurso UsuarioResource al objeto api
api.add_resource(UsuarioResource, "/usuarios")
api.add_resource(UsuarioIdResource, "/usuarios", "/usuarios/<int:id>")
api.add_resource(Hello, "/hello")

if __name__ == "__main__":
    app.run(debug=True)