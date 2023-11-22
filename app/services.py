from api_usuarios.cliente import UsuariosClient

def show_profile(id):
    # Crear una instancia del cliente de usuarios con la URL base de la API
    usuarios_client = UsuariosClient("http://localhost:5000")
    # Obtener los datos del usuario con el id dado usando el método get_user_by_id
    user = usuarios_client.get_user_by_id(id)
    # Devolver los datos del usuario
    return user
