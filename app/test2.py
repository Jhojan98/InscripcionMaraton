from flask import Flask, render_template, request, url_for, redirect, flash

from api_usuarios.cliente import UsuariosClient
from api_equipos.cliente import EquiposClient
from api_maraton.cliente import MaratonesClient 
from flask import Flask
import os
from flask_restful import Api
from api_usuarios.api import UsuarioResource,UsuarioIdResource,LoginResource,InscritoResource
from api_equipos.api import EquipoResource,EquipoIdResource,EquipoUsuarioResource
from api_maraton.api import MaratonResource,MaratonIdResource,MaratonInscribirResource
from main import app,db


api = Api(app)

# Crear un cliente para las apis
clienteUsuarios = UsuariosClient("http://localhost:5000")
clienteEquipos = EquiposClient("http://localhost:5000")
clienteMaraton = MaratonesClient("http://localhost:5000")

api.add_resource(UsuarioResource, "/api/v1/usuarios")
api.add_resource(LoginResource, "/api/v1/login")
api.add_resource(InscritoResource, "/api/v1/inscribir")
api.add_resource(UsuarioIdResource, "/api/v1/usuarios", "/api/v1/usuarios/<string:nombre>")
api.add_resource(EquipoResource, "/api/v3/equipos")
api.add_resource(EquipoIdResource, "/api/v3/equipos","/api/v3/equipos/<string:nombre>")
api.add_resource(EquipoUsuarioResource, "/api/v3/equipos", "/api/v3/equipos/<int:id_equipo>/registrar/<int:id_usuario>")
api.add_resource(MaratonResource, "/api/v2/maratones")
#api.add_resource(MaratonIdResource, "/api/v2/maratones","/api/v2/maratones/<int:id>/<int:id>")
api.add_resource(MaratonInscribirResource, "/api/v2/maratones","/api/v2/maratones/<int:maraton_id>/inscribir/<int:equipo_id>")
nombreEquipoo = "Por defecto"
@app.route('/')
def index():

    usuarios =  clienteUsuarios.get_all_users()
    return render_template('index.html', usuarios=usuarios)

@app.route('/login', methods=['GET', 'POST'])
def login(): 
    if request.method == 'POST':
        message, category = clienteUsuarios.login_user(request.form['nombre'],request.form['password']) # Obtener el mensaje y la categoría del cliente
        if message == "El usuario y la contraseña son válidos":
            return redirect('/registroEquipo')
        flash(message, category) # Usar el flash con el mensaje y la categoría
        return render_template('auth/login.html') # Renderizar el template HTML que muestra el mensaje flash
    return render_template('auth/login.html')


@app.route('/singup', methods=['GET', 'POST'])
def singup():
    if request.method == 'POST': 
        nombre = request.form['participante']
        correo = request.form['correo']
        materia = request.form['materia']
        password = request.form['password']

        # Llamar al método create_user de tu instancia de cliente y pasarle los datos del formulario
        message, category = clienteUsuarios.create_user(nombre, correo, password, 1)
        
        if message == "El usuario fue creado con éxito":
            clienteUsuarios.inscribir_usuario(nombre,materia)
            return redirect('/login')
        else:
            flash(message,category)
            return render_template('auth/singup.html')
    else:
        return render_template('auth/singup.html')

@app.route('/home')
def home():
    return render_template('auth/registroEquipo.html')




@app.route('/registroEquipo', methods=['GET', 'POST'])
def registroEquipo():
    if request.method == 'POST':
        try:
            global nombreEquipoo
            participante1 = request.form['participante1']
            participante2 = request.form['participante2']
            participante3 = request.form['participante3']
            nombreLider = request.form['Lider']
            nombreEquipo = request.form['nombreEquipo']
            nombreEquipoo = nombreEquipo
            lider = clienteUsuarios.get_user_by_name(nombreLider)
            part1 = clienteUsuarios.get_user_by_name(participante1)
            print(part1)
            part2 = clienteUsuarios.get_user_by_name(participante2)
            part3 = clienteUsuarios.get_user_by_name(participante3)
            if isinstance(lider, dict):
                print("ENTRO")
                category,message = lider.popitem()
                flash(message,category)
                #clienteEquipos.create_equipo(nombreEquipo,lider['id'])
                equipo = clienteEquipos.get_equipo_by_nombre(nombreEquipo)
                print(equipo)
                print(part1['id'])
                print(equipo['id'])
                #mesasage = clienteEquipos.registrar_usuario(equipo['id'],part1['id'])
                #mesasage = clienteEquipos.registrar_usuario(equipo['id'],part2['id'])
                #mesasage = clienteEquipos.registrar_usuario(equipo['id'],part3['id'])
            else:
                print("no entro")
                print(lider)
                
            print(f'Participante 1: {participante1}')
            print(f'Participante 2: {participante2}')
            print(f'Participante 3: {participante3}')
            print(f'NOMBRE EQUIPO: {nombreEquipoo}')
            print(f'Nombre del equipo: {nombreEquipo}')

            
            return redirect(url_for("menuNivel"))
        except KeyError as e:
            print(f"Error: {e}")
    return render_template('auth/registroEquipo.html')

@app.route("/menuNivel", methods=["GET", "POST"])
def menuNivel():
    global nombreEquipoo
    if request.method == 'POST':
        try:
           
            print(nombreEquipoo)
            data = request.get_json()
            equipo = clienteEquipos.get_equipo_by_nombre(nombreEquipoo)
            nivel = data['nivel']
            if nivel == "Intermedia":
                print("entro")
                maratonId = '2'
            elif nivel == "Profesional":
                maratonId = '4'
            elif nivel == "Avanzada":
                maratonId = '3'
            else:
                maratonId = '1'
            print(f'Nivel: {nivel}')
            print(equipo['id'])
            print(maratonId)
            hola = clienteMaraton.inscribir_equipo(equipo['id'],maratonId)
            return redirect(url_for('menuNivel'))
        
        
        except KeyError as e:
            print(f"Error: {e}")    
    else:
        return render_template('auth/menuNivel.html')
if __name__ == "__main__":
    app.run(debug=True)
    