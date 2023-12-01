import requests
import json
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
        if not tipo:
            tipo = 1
        endpoint = self.base_url + "/api/v1/usuarios"
        data = {
            "nombre": nombre,
            "email": email,
            "contraseña": contraseña,
            "tipo_id": tipo
        }
        response = self.session.post(endpoint, json=data) # Usar la sesión para enviar la petición POST
        result = response.json()
        """
        if response.status_code == 200:
            message = result["message"]
            category = "success"
        else:
            message = result["message"]
            category = "error"
        """
        self.token = None
        categ, message = result.popitem()
        print(categ)
        print(message)
        category = "success"
        return message,category

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
        result = response.json()
        if response.status_code == 200:
            message = result["message"]
            category = "success"
        return message, category

    def login_user(self, nombre_o_email, contraseña):
        # Iniciar sesión con el nombre o el email y la contraseña dados
        endpoint = self.base_url + "/api/v1/login"
        data = {
            "nombre": nombre_o_email,
            "email": nombre_o_email,
            "contraseña": contraseña
        }
        response = self.session.post(endpoint, json=data) # Usar la sesión para enviar la petición POST
        result = response.json()
        if response.status_code == 200:
            # Si la respuesta es exitosa, guardar el token y devolver el mensaje de éxito y la categoría "success"
            self.token = result.get("response", {}).get("secret_key", None)
            message = result["message"]
            category = "success"
        else:
            # Si la respuesta es errónea, devolver el mensaje de error, la categoría "error" y el código de estado
            self.token = None
            message = result["error"]
            category = "error"
            # También puedes devolver el código de estado si quieres usarlo para algo más
        return message, category # Devolver el mensaje y la categoría como una tupla
    
    