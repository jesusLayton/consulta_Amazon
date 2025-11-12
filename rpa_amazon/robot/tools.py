import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd


def read_products2(file_path):
    """
    Lee productos desde un archivo .txt.
    Cada línea del archivo debe contener un producto.
    Retorna una lista con los nombres de los productos.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            products = [line.strip() for line in f if line.strip()]
        return products
    except FileNotFoundError:
        log_message(f"Archivo no encontrado: {file_path}")
        return []
    except Exception as e:
        log_message(f"Error al leer {file_path}: {e}")
        return []
    
import pandas as pd

import pandas as pd

def read_products(file_path):
    """
    Lee productos desde un archivo .xlsx.
    Espera que la primera columna contenga los nombres de los productos.
    """
    try:
        df = pd.read_excel(file_path)
        products = df.iloc[:, 0].dropna().tolist()
        products = [str(p).strip() for p in products if str(p).strip()]
        return products
    except FileNotFoundError:
        log_message(f"Archivo no encontrado: {file_path}")
        return []
    except Exception as e:
        log_message(f"Error al leer {file_path}: {e}")
        return []


def log_message(message):
    """Registra mensajes en un archivo log."""
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{message}\n")


def convertir_a_cop(precio_usd):
    """
    Convierte un precio en USD a COP.
    Ejemplo: "$99.99" -> 449955.0
    """
    try:
        # Limpiar el precio (quitar $ y espacios)
        precio_limpio = precio_usd.replace("$", "").replace(",", "").strip()
        precio_float = float(precio_limpio)
        
        # Tasa de cambio aproximada (ajustar según necesidad)
        tasa_cambio = 4500
        precio_cop = precio_float * tasa_cambio
        
        return precio_cop
    except:
        return 0.0


def log_message(message):
    """
    Registra mensajes o errores en log.txt con salto de línea.
    """
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")


def validate_product_data(product_data):
    """
    Valida que un producto tenga nombre, precio y tipo de entrega.
    """
    required_keys = ["nombre", "precio", "entrega"]
    return all(key in product_data and product_data[key] for key in required_keys)


def convertir_a_cop(precio_usd):
    """
    Convierte un precio en USD a COP.
    Asume una tasa de cambio (ajústala según necesites).
    """
    try:
        # Limpiar el precio: remover $, comas, etc.
        precio_limpio = precio_usd.replace("$", "").replace(",", "").strip()
        if not precio_limpio or precio_limpio == "0":
            return 0
        
        # Convertir a float
        precio_float = float(precio_limpio)
        
        # Tasa de cambio USD a COP (ajusta según el valor actual)
        tasa_cambio = 4000  # Ejemplo: 1 USD = 4000 COP
        
        return round(precio_float * tasa_cambio, 2)
    except Exception as e:
        log_message(f"Error al convertir precio '{precio_usd}': {e}")
        return 0
    

# fucnion de prueba para vlidar la lectura de la base de datos y el envio de correo
def enviar_correo_resumen123(conn, destinatario, remitente, password):
    """
    Envía por correo un Excel con los productos más baratos por categoría.
    
    Args:
        conn: Conexión a la base de datos
        destinatario (str): Email destino
        remitente (str): Tu Gmail
        password (str): Contraseña de aplicación de Gmail
    """
    try:
        # Consultar productos más bartos
        df = pd.read_sql_query("""
            SELECT 
                categoria as 'Categoría',
                nombre as 'Producto',
                precio_usd as 'Precio usd',
                
            FROM productos
            WHERE precio_cop = (
                SELECT MIN(precio_cop) 
                FROM productos p2 
                WHERE p2.categoria = productos.categoria AND p2.precio_cop > 0
            )
        """, conn)
        
        # Formatear precio COP
        df['Precio COP'] = df['Precio COP'].apply(lambda x: f"${x:,.0f}")
        
        # Crear Excel
        excel_file = "resumen_productos.xlsx"
        df.to_excel(excel_file, index=False)
        
        # Crear correo
        msg = MIMEMultipart()
        msg['From'] = remitente
        msg['To'] = destinatario
        msg['Subject'] = 'Resumen de Productos Amazon'
        
        # Cuerpo simple
        cuerpo = f"Adjunto encontrarás el resumen de los {len(df)} productos más baratos encontrados en Amazon."
        msg.attach(MIMEText(cuerpo, 'plain'))
        
        # Adjuntar Excel
        with open(excel_file, 'rb') as archivo:
            parte = MIMEBase('application', 'octet-stream')
            parte.set_payload(archivo.read())
            encoders.encode_base64(parte)
            parte.add_header('Content-Disposition', f'attachment; filename={excel_file}')
            msg.attach(parte)
        
        # Enviar
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        server.send_message(msg)
        server.quit()
        
        print(f"\n✓ Correo enviado a {destinatario}")
        return True
        
    except Exception as e:
        print(f"\n✗ Error al enviar correo: {e}")
        return False
    


import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


def read_products(file_path):
    """
    Lee productos desde un archivo .xlsx.
    Espera que la primera columna contenga los nombres de los productos.
    """
    try:
        df = pd.read_excel(file_path)
        products = df.iloc[:, 0].dropna().tolist()
        products = [str(p).strip() for p in products if str(p).strip()]
        return products
    except FileNotFoundError:
        log_message(f"Archivo no encontrado: {file_path}")
        return []
    except Exception as e:
        log_message(f"Error al leer {file_path}: {e}")
        return []


def log_message(message):
    """Registra mensajes en un archivo log."""
    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(f"{message}\n")


def convertir_a_cop(precio_usd):
    """
    Convierte un precio en USD a COP.
    Ejemplo: "$99.99" -> 449955.0
    """
    try:
        precio_limpio = precio_usd.replace("$", "").replace(",", "").strip()
        precio_float = float(precio_limpio)
        tasa_cambio = 4500
        precio_cop = precio_float * tasa_cambio
        return precio_cop
    except:
        return 0.0


def enviar_correo_resumen(conn, destinatario, remitente, password):
    """
    Envía por correo un Excel con los productos más baratos por categoría.
    
    Args:
        conn: Conexión a la base de datos
        destinatario (str): Email destino
        remitente (str): Tu Gmail
        password (str): Contraseña de aplicación de Gmail
    """
    try:
        # Consultar productos más baratos usando precio_usd
        df = pd.read_sql_query("""
            SELECT 
                categoria as 'Categoría',
                nombre as 'Producto',
                precio_usd as 'Precio USD',
                precio_cop as 'Precio COP'
            FROM productos p1
            WHERE id = (
                SELECT p2.id
                FROM productos p2
                WHERE p2.categoria = p1.categoria 
                AND CAST(REPLACE(REPLACE(p2.precio_usd, '$', ''), ',', '') AS REAL) > 0
                ORDER BY CAST(REPLACE(REPLACE(p2.precio_usd, '$', ''), ',', '') AS REAL) ASC
                LIMIT 1
            )
        """, conn)
        
        # Formatear precio COP
        df['Precio COP'] = df['Precio COP'].apply(lambda x: f"${x:,.0f}")
        
        # Crear Excel
        excel_file = "resumen_productos.xlsx"
        df.to_excel(excel_file, index=False)
        
        # Crear correo
        msg = MIMEMultipart()
        msg['From'] = remitente
        msg['To'] = destinatario
        msg['Subject'] = 'Resumen de Productos Amazon'
        
        # Cuerpo simple
        cuerpo = f"Adjunto encontrarás el resumen de los {len(df)} productos más baratos encontrados en Amazon."
        msg.attach(MIMEText(cuerpo, 'plain'))
        
        # Adjuntar Excel
        with open(excel_file, 'rb') as archivo:
            parte = MIMEBase('application', 'octet-stream')
            parte.set_payload(archivo.read())
            encoders.encode_base64(parte)
            parte.add_header('Content-Disposition', f'attachment; filename={excel_file}')
            msg.attach(parte)
        
        # Enviar
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        server.send_message(msg)
        server.quit()
        
        print(f"\n✓ Correo enviado a {destinatario}")
        return True
        
    except Exception as e:
        print(f"\n✗ Error al enviar correo: {e}")
        return False








