from dao.usuario import UsuarioDAO
from dao.equipo import EquipoDAO
from dao.integrante import IntegranteDAO
from dao.maraton import MaratonDAO


# Crear algunos usuarios de ejemplo
usuario1 = UsuarioDAO()
usuario1.data(1, "Juan", "juan@gmail.com", "1234", "normal")

usuario2 = UsuarioDAO()
usuario2.data(2, "Ana", "ana@gmail.com", "5678", "lider")
usuario3 = UsuarioDAO()
usuario3.data(3, "Pedro", "pedro@gmail.com", "abcd", "miembro")
usuario4 = UsuarioDAO()
usuario4.data(4, "Laura", "laura@gmail.com", "efgh", "admin")

# Insertar los usuarios en la tabla de usuarios
usuario1.insert_usuario()
usuario2.insert_usuario()
usuario3.insert_usuario()
usuario4.insert_usuario()

# Seleccionar un usuario por su email y contraseña
usuario = usuario1.select_usuario("juan@gmail.com", "1234")
print(usuario)

# Crear algunos maratones de ejemplo
maraton1 = MaratonDAO()
maraton1.data(1, "Maratón de Python", "2023-12-01", 4, "intermedio", "Un curso online de Python", 10)
maraton2 = MaratonDAO()
maraton2.data(2, "Maratón de Java", "2023-11-15", 3, "avanzado", "Un libro de Java", 8)

# Insertar los maratones en la tabla de maratones
maraton1.insert_maraton()
maraton2.insert_maraton()

# Seleccionar un maratón por su nombre
maraton = maraton1.select_maraton("Maratón de Python")
print(maraton)

# Crear algunos equipos de ejemplo
equipo1 = EquipoDAO()
equipo1.data(1, "Los Pythones", 2, 1, "pendiente")
equipo2 = EquipoDAO()
equipo2.data(2, "Los Javeros", 2, 2, "aceptado")

# Insertar los equipos en la tabla de equipos
equipo1.insert_equipo()
equipo2.insert_equipo()

# Seleccionar un equipo por su nombre
equipo = equipo1.select_equipo("Los Pythones")
print(equipo)

# Crear algunos integrantes de ejemplo
integrante1 = IntegranteDAO()
integrante1.data(1, 2)
integrante2 = IntegranteDAO()
integrante2.data(1, 3)

# Insertar los integrantes en la tabla de integrantes
integrante1.insert_integrante()
integrante2.insert_integrante()

# Seleccionar un integrante por su equipo y usuario
integrante = integrante1.select_integrante(1, 2)
print(integrante)
