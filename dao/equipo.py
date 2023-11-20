from db.connection import with_connection

class EquipoDAO():
    def data(self,
            id,
            nombre,
            lider,
            maraton,
            estado):
        self._id = id
        self._nombre = nombre
        self._lider = lider
        self._maraton = maraton
        self._estado = estado

    @with_connection
    def insert_equipo(self, *args, **kwargs):
        conn = kwargs.pop('connection')
        cursor = conn.cursor()
        query = f'''
            INSERT INTO equipo
            (id,
            nombre,
            lider,
            maraton,
            estado)
            VALUES(?,?,?,?,?)
        '''
        cursor.execute(query,
                                (self._id,
                                self._nombre,
                                self._lider,
                                self._maraton,
                                self._estado)
        )
        return cursor.lastrowid
    

    @with_connection
    def select_equipo(self, nombre, *args, **kwargs):
        conn = kwargs.pop('connection')
        cursor = conn.cursor()
        query = f'''
            SELECT id,
                nombre,
                lider,
                maraton,
                estado
            FROM equipo
            WHERE nombre = ?
        '''
        cursor.execute(query, (nombre,))
        result = cursor.fetchone()
        return result