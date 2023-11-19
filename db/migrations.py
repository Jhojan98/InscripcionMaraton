from connection import with_connection

@with_connection
def create_table_usuarios(*args,**kwargs):
    conn = kwargs.pop('connection')
    cursor = conn.cursor()
    query  = f'''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nombre TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        contraseña TEXT NOT NULL,
        tipo TEXT NOT NULL CHECK (tipo IN ('normal', 'lider', 'admin', 'miembro'))
    )
    '''
    cursor.execute(query)
    result = cursor.fetchone()
    return result

@with_connection
def create_table_equipos(*args,**kwargs):
    conn = kwargs.pop('connection')
    cursor = conn.cursor()
    query  = f'''
    CREATE TABLE IF NOT EXISTS equipos (
        id INTEGER PRIMARY KEY,
        nombre TEXT UNIQUE NOT NULL,
        lider INTEGER NOT NULL,
        maraton INTEGER NOT NULL,
        estado TEXT NOT NULL CHECK (estado IN ('pendiente', 'aceptado', 'rechazado')),
        FOREIGN KEY (lider) REFERENCES usuarios (id) ON DELETE CASCADE,
        FOREIGN KEY (maraton) REFERENCES maratones (id) ON DELETE CASCADE
    )
    '''
    cursor.execute(query)
    result = cursor.fetchone()
    return result

@with_connection
def create_table_integrantes(*args,**kwargs):
    conn = kwargs.pop('connection')
    cursor = conn.cursor()
    query  = f'''
    CREATE TABLE IF NOT EXISTS integrantes (
        equipo INTEGER NOT NULL,
        usuario INTEGER NOT NULL,
        PRIMARY KEY (equipo, usuario),
        FOREIGN KEY (equipo) REFERENCES equipos (id) ON DELETE CASCADE,
        FOREIGN KEY (usuario) REFERENCES usuarios (id) ON DELETE CASCADE
    )
    '''
    cursor.execute(query)
    result = cursor.fetchone()
    return result

@with_connection
def create_table_maratones(*args,**kwargs):
    conn = kwargs.pop('connection')
    cursor = conn.cursor()
    query  = f'''
    CREATE TABLE IF NOT EXISTS maratones (
        id INTEGER PRIMARY KEY,
        nombre TEXT UNIQUE NOT NULL,
        fecha DATE NOT NULL,
        duracion INTEGER NOT NULL,
        nivel TEXT NOT NULL CHECK (nivel IN ('principiante', 'intermedio', 'avanzado')),
        premio TEXT NOT NULL,
        cupos INTEGER NOT NULL
    )
    '''
    cursor.execute(query)
    result = cursor.fetchone()
    return result


if __name__ == "__main__":
    create_table_usuarios()
    create_table_equipos()
    create_table_integrantes()
    create_table_maratones()
