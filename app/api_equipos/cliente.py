import requests

class EquiposClient: 
    def __init__(self, base_url): 
        self.base_url = base_url 
        self.session = requests.Session() # Crear una sesión de requests para reutilizar la conexión

    def get_equipo_by_id(self, id):
        # Obtener los datos del equipo con el id dado
        endpoint = self.base_url + f"/api/v3/equipos/{id}"
        response = self.session.get(endpoint) # Usar la sesión para enviar la petición GET
        return response.json()

    def get_all_equipos(self):
        # Obtener los datos de todos los equipos
        endpoint = self.base_url + "/api/v3/equipos"
        response = self.session.get(endpoint) # Usar la sesión para enviar la petición GET
        return response.json()

    def create_equipo(self, nombre, lider_id):
        # Crear un nuevo equipo con los datos dados
        endpoint = self.base_url + "/api/v3/equipos"
        data = {
            "nombre": nombre,
            "lider_id": lider_id
        }
        response = self.session.post(endpoint, json=data) # Usar la sesión para enviar la petición POST
        return response.json()

    def update_equipo(self, id, nombre, lider_id, maraton_id, estado_id):
        # Actualizar los datos del equipo con el id dado
        endpoint = self.base_url + f"/api/v3/equipos/{id}"
        data = {
            "nombre": nombre,
            "lider_id": lider_id,
            "maraton_id": maraton_id,
            "estado_id": estado_id
        }
        response = self.session.put(endpoint, json=data) # Usar la sesión para enviar la petición PUT
        return response.json()

    def delete_equipo(self, id):
        # Eliminar el equipo con el id dado
        endpoint = self.base_url + f"/api/v3/equipos/{id}"
        response = self.session.delete(endpoint) # Usar la sesión para enviar la petición DELETE
        return response.json()

    def registrar_usuario(self, equipo_id, usuario_id):
        # Registrar un usuario en un equipo
        endpoint = self.base_url + f"/api/v3/equipos/{equipo_id}/registrar/{usuario_id}"
        response = self.session.post(endpoint) # Usar la sesión para enviar la petición POST
        return response.json()
