import mysql.connector
from mysql.connector import Error

def test_connection():
    try:
        conn = mysql.connector.connect(
            host='monorail.proxy.rlwy.net',
            user='root',
            password='uCEEoyKCKRnnUmAfifTHZJuXlMcKvODu',
            database='railway',
            port=38549
        )
        if conn.is_connected():
            print("Conexión a la base de datos exitosa.")
            cursor = conn.cursor()
            cursor.execute("SELECT nombre_cancion, dificultad FROM Canciones")
            canciones = cursor.fetchall()
            print("Datos obtenidos de la base de datos:", canciones)
            cursor.close()
        else:
            print("No se pudo conectar a la base de datos.")
    except Error as e:
        print(f"Error al conectar a la base de datos: {e}")
    finally:
        if conn.is_connected():
            conn.close()
            print("Conexión cerrada.")

if __name__ == "__main__":
    test_connection()
