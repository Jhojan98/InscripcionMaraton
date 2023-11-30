from flask import Flask
import os
from flask_restful import Api
from api_usuarios.api import UsuarioResource,Hello,UsuarioIdResource
from api_equipos.api import EquipoResource,EquipoIdResource,EquipoUsuarioResource
from api_maraton.api import MaratonResource,MaratonIdResource
from main import app,db
from api_usuarios.cliente import UsuariosClient

api = Api(app)
# Añadir el recurso UsuarioResource al objeto api
api.add_resource(UsuarioResource, "/usuarios")
api.add_resource(UsuarioIdResource, "/usuarios", "/usuarios/<int:id>")
api.add_resource(Hello, "/hello")
api.add_resource(EquipoResource, "/equipos")
api.add_resource(EquipoIdResource, "/equipos","/equipos/<int:id>")
api.add_resource(EquipoUsuarioResource, "/equipos", "/equipos/<int:id_equipo>/<int:id_usuario>")
api.add_resource(MaratonResource, "/maratones")
api.add_resource(MaratonIdResource, "/maratones","/maratones/<int:id>")



"""
user = clientUS.get_user_by_id(4) # Llamar al método get_user_by_id con el id 1
    print(user) # Imprimir el resultado
"""

if __name__ == "__main__":
    app.run(debug=True)
    