from db.connection import with_connection

class IntegranteDAO():
    def data(self,
            equipo,
            usuario):
        self._equipo = equipo
        self._usuario = usuario

    @with_connection
    def insert_integrante(self, *args, **kwargs):
        conn = kwargs.pop('connection')
        cursor = conn.cursor()
        query = f'''
            INSERT INTO integrante
            (equipo,
            usuario)
            VALUES(?,?)
        '''
        cursor.execute(query,
                                (self._equipo,
                                self._usuario)
        )
        return cursor.lastrowid
    

    @with_connection
    def select_integrante(self, equipo, usuario, *args, **kwargs):
        conn = kwargs.pop('connection')
        cursor = conn.cursor()
        query = f'''
            SELECT equipo,
                usuario
            FROM integrante
            WHERE equipo = ? AND usuario = ?
        '''
        cursor.execute(query, (equipo, usuario))
        result = cursor.fetchone()
        return result
