import psycopg2
from psycopg2.extras import RealDictCursor

def get_db_connection():
    conn = psycopg2.connect(
        dbname='soporte_tickets',
        user='postgres',
        password='1234',
        host='localhost',
        cursor_factory=RealDictCursor  # Permite devolver los registros como diccionarios
    )
    print('--con', conn)
    return conn