from db.connection import with_connection

class UsuarioDAO():
    def data(self,
            id,
            nombre,
            email,
            contraseña,
            tipo):
        self._id = id
        self._nombre = nombre
        self._email = email
        self._contraseña = contraseña
        self._tipo = tipo

    @with_connection
    def insert_usuario(self, *args, **kwargs):
        conn = kwargs.pop('connection')
        cursor = conn.cursor()
        query = f'''
            INSERT INTO usuario
            (id,
            nombre,
            email,
            contraseña,
            tipo)
            VALUES(?,?,?,?,?)
        '''
        cursor.execute(query,
                                (self._id,
                                self._nombre,
                                self._email,
                                self._contraseña,
                                self._tipo)
        )
        return cursor.lastrowid
    

    @with_connection
    def select_usuario(self, email, contraseña, *args, **kwargs):
        conn = kwargs.pop('connection')
        cursor = conn.cursor()
        query = f'''
            SELECT id,
                nombre,
                email,
                contraseña,
                tipo
            FROM usuario
            WHERE email = ? AND contraseña = ?
        '''
        cursor.execute(query, (email, contraseña))
        result = cursor.fetchone()
        return result
