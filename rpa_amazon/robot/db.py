import sqlite3
import os


def conectar_db(db_name="productos_amazon.db"):
    """
    Conecta a la base de datos SQLite y crea la tabla si no existe.
    Retorna la conexión y el cursor.
    """
    try:
        # Conectar a la base de datos (se crea si no existe)
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # Crear tabla si no existe

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                categoria TEXT,
                nombre TEXT,
                precio TEXT,
                precio_cop REAL,
                entrega TEXT
            )
        """)
        
        conn.commit()
        print(f"Conectado a la base de datos: {db_name}")
        
        return conn, cursor
        
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        raise


def limpiar_db(conn, cursor):
    """
    Elimina todos los registros de la tabla productos (opcional).
    Útil para empezar con una base de datos limpia.
    """
    try:
        cursor.execute("DELETE FROM productos")
        conn.commit()
        print("Base de datos limpiada")
    except sqlite3.Error as e:
        print(f"Error al limpiar la base de datos: {e}")


def cerrar_db(conn):
    """
    Cierra la conexión a la base de datos.
    """
    if conn:
        conn.close()
        print("Conexión a la base de datos cerrada")

def save_to_db(self, product_info):
    """Guarda los productos en la base de datos."""
    print(f"  Guardando {len(product_info)} productos en la BD...")
    
    for product in product_info:
        try:
            self.cursor.execute("""
                INSERT INTO productos (categoria, nombre, precio, precio_cop, entrega)
                VALUES (?, ?, ?, ?, ?)
            """, (
                product['categoria'],
                product['nombre'],
                product['precio'],
                product['precio_cop'],
                product['entrega']
            ))
        except Exception as e:
            print(f"    [ERROR] No se pudo guardar: {e}")

    
    self.conn.commit()
    print(f" Productos guardados correctamente")



