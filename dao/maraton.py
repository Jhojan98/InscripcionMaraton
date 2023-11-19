from db.connection import with_connection

class MaratonDAO():
    def data(self,
            id,
            nombre,
            fecha,
            duracion,
            nivel,
            premio,
            cupos):
        self._id = id
        self._nombre = nombre
        self._fecha = fecha
        self._duracion = duracion
        self._nivel = nivel
        self._premio = premio
        self._cupos = cupos

    @with_connection
    def insert_maraton(self, *args, **kwargs):
        conn = kwargs.pop('connection')
        cursor = conn.cursor()
        query = f'''
            INSERT INTO maraton
            (id,
            nombre,
            fecha,
            duracion,
            nivel,
            premio,
            cupos)
            VALUES(?,?,?,?,?,?,?)
        '''
        cursor.execute(query,
                                (self._id,
                                self._nombre,
                                self._fecha,
                                self._duracion,
                                self._nivel,
                                self._premio,
                                self._cupos)
        )
        return cursor.lastrowid
    

    @with_connection
    def select_maraton(self, nombre, *args, **kwargs):
        conn = kwargs.pop('connection')
        cursor = conn.cursor()
        query = f'''
            SELECT id,
                nombre,
                fecha,
                duracion,
                nivel,
                premio,
                cupos
            FROM maraton
            WHERE nombre = ?
        '''
        cursor.execute(query, (nombre,))
        result = cursor.fetchone()
        return result