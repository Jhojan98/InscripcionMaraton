from flask import render_template, redirect, url_for
from dao.usuario import UsuarioDAO


def handle_login(form):
    username = form['username']
    password = form['password']
    
    usuario = UsuarioDAO()
    data = usuario.select_usuario(username,password)
    
    if(data != None):
        context = {
            'is_admin':data[-1] == 1,
        }
        return redirect(url_for('home_vehicles', **context))
    
    context = {
        'error': 'Incorrect fields',       
    }
    return render_template('login.html', **context) 