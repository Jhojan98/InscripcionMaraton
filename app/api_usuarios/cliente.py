import requests

class UsuariosClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_user_by_id(self, id):
        # Obtener los datos del usuario con el id dado
        endpoint = self.base_url + f"/api/v1/usuarios/{id}"
        response = requests.get(endpoint)
        return response.json()

    def get_all_users(self):
        # Obtener los datos de todos los usuarios
        endpoint = self.base_url + "/api/v1/usuarios"
        response = requests.get(endpoint)
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
        response = requests.post(endpoint, json=data)
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
        response = requests.put(endpoint, json=data)
        return response.json()

    def delete_user(self, id):
        # Eliminar el usuario con el id dado
        endpoint = self.base_url + f"/api/v1/usuarios/{id}"
        response = requests.delete(endpoint)
        return response.json()
