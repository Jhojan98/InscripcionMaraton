import requests

class MaratonesClient: 
    def init(self, base_url):
        self.base_url = base_url 
        self.session = requests.Session() # Crear una sesión de requests para reutilizar la conexión

    def get_maraton_by_id(self, id):
        # Obtener los datos de la maratón con el id dado
        endpoint = self.base_url + f"/api/v2/maratones/{id}"
        response = self.session.get(endpoint) # Usar la sesión para enviar la petición GET
        return response.json()

    def get_all_maratones(self):
        # Obtener los datos de todas las maratones
        endpoint = self.base_url + "/api/v2/maratones"
        response = self.session.get(endpoint) # Usar la sesión para enviar la petición GET
        return response.json()

    def create_maraton(self, nombre, fecha, duracion, nivel_id, premio, cupos, materia_id):
        # Crear una nueva maratón con los datos dados
        endpoint = self.base_url + "/api/v2/maratones"
        data = {
            "nombre": nombre,
            "fecha": fecha,
            "duracion": duracion,
            "nivel_id": nivel_id,
            "premio": premio,
            "cupos": cupos,
            "materia_id": materia_id
        }
        response = self.session.post(endpoint, json=data) # Usar la sesión para enviar la petición POST
        return response.json()

    def update_maraton(self, id, nombre, fecha, duracion, nivel_id, premio, cupos, materia_id):
        # Actualizar los datos de la maratón con el id dado
        endpoint = self.base_url + f"/api/v2/maratones/{id}"
        data = {
            "nombre": nombre,
            "fecha": fecha,
            "duracion": duracion,
            "nivel_id": nivel_id,
            "premio": premio,
            "cupos": cupos,
            "materia_id": materia_id
        }
        response = self.session.put(endpoint, json=data) # Usar la sesión para enviar la petición PUT
        return response.json()

    def delete_maraton(self, id):
        # Eliminar la maratón con el id dado
        endpoint = self.base_url + f"/api/v2/maratones/{id}"
        response = self.session.delete(endpoint) # Usar la sesión para enviar la petición DELETE
        return response.json()

    def inscribir_equipo(self, equipo_id, maraton_id):
        # Inscribir un equipo en una maratón
        endpoint = self.base_url + f"/api/v2/maratones/{maraton_id}/inscribir/{equipo_id}"
        response = self.session.post(endpoint) # Usar la sesión para enviar la petición POST
        return response.json()
