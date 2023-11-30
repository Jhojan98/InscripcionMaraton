import requests

class UsuariosClient:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session() # Crear una sesión de requests para reutilizar la conexión

    def get_user_by_name(self, name):
        # Obtener los datos del usuario con el name dado
        endpoint = self.base_url + f"/api/v1/usuarios/{name}"
        response = self.session.get(endpoint) # Usar la sesión para enviar la petición GET
        return response.json()

    def get_all_users(self):
        # Obtener los datos de todos los usuarios
        endpoint = self.base_url + "/api/v1/usuarios"
        response = self.session.get(endpoint) # Usar la sesión para enviar la petición GET
        return response.json()

    def create_user(self, nombre, email, contraseña, tipo):
        # Crear un nuevo usuario con los datos dados
        endpoint = self.base_url + "/api/v1/usuarios"
        data = {
            "nombre": nombre,
            "email": email,
            "contraseña": contraseña,
            "tipo": tipo
        }
        response = self.session.post(endpoint, json=data) # Usar la sesión para enviar la petición POST
        return response.json()

    def update_user(self, id, nombre, email, contraseña, tipo):
        # Actualizar los datos del usuario con el id dado
        endpoint = self.base_url + f"/api/v1/usuarios/{id}"
        data = {
            "nombre": nombre,
            "email": email,
            "contraseña": contraseña,
            "tipo": tipo
        }
        response = self.session.put(endpoint, json=data) # Usar la sesión para enviar la petición PUT
        return response.json()

    def delete_user(self, id):
        # Eliminar el usuario con el id dado
        endpoint = self.base_url + f"/api/v1/usuarios/{id}"
        response = self.session.delete(endpoint) # Usar la sesión para enviar la petición DELETE
        return response.json()
