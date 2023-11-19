import sqlite3

def with_connection(fn):
    def wrapped(*args, **kwargs):
        conn = sqlite3.connect("gestion.db")
        try:
            result = fn(*args, connection=conn, **kwargs)
        except:
            conn.rollback()
            print("SQL failed")
            raise
        else:
            conn.commit()
        finally:
            conn.close()
        return result
    return wrapped 