from connection import with_connection

@with_connection
def create_table_usuario(*args,**kwargs):
    conn = kwargs.pop('connection')
    cursor = conn.cursor()
    query  = f'''
    CREATE TABLE IF NOT EXISTS usuario (
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
def create_table_equipo(*args,**kwargs):
    conn = kwargs.pop('connection')
    cursor = conn.cursor()
    query  = f'''
    CREATE TABLE IF NOT EXISTS equipo (
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
def create_table_integrante(*args,**kwargs):
    conn = kwargs.pop('connection')
    cursor = conn.cursor()
    query  = f'''
    CREATE TABLE IF NOT EXISTS integrante (
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
def create_table_maraton(*args,**kwargs):
    conn = kwargs.pop('connection')
    cursor = conn.cursor()
    query  = f'''
    CREATE TABLE IF NOT EXISTS maraton (
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
    create_table_usuario()
    create_table_equipo()
    create_table_integrante()
    create_table_maraton()
