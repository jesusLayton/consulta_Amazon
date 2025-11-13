import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import pandas as pd
import os


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
    """
    Registra mensajes o errores en log.txt con salto de línea.
    """
    with open("log.txt", "a", encoding="utf-8") as log_file:
        log_file.write(message + "\n")


def log_print(message):
    """
    Imprime en consola Y guarda en log.txt
    """
    print(message)
    log_message(message)


def validate_product_data(product_data):
    """
    Valida que un producto tenga nombre, precio y tipo de entrega.
    """
    required_keys = ["nombre", "precio", "entrega"]
    return all(key in product_data and product_data[key] for key in required_keys)


def convertir_a_cop(precio_str):
    """
    Detecta automáticamente si el precio es USD o COP según el prefijo.
    - Si contiene "COP": Lo deja como está (ya es COP)
    - Si contiene "US" o "$": Lo convierte de USD a COP usando TRM del .env
    
    Ejemplos:
        "US$99.99" -> 449955.0 (USD convertido a COP con TRM)
        "$99.99" -> 449955.0 (USD convertido a COP con TRM)
        "COP $1,250,000" -> 1250000.0 (Ya es COP, se mantiene)
    """
    try:
        # Verificar si el precio contiene "COP" (ya está en pesos colombianos)
        if "COP" in precio_str.upper():
            # Limpiar y retornar como está, redondeado a 2 decimales
            precio_limpio = precio_str.upper().replace("COP", "").replace("$", "").replace(",", "").strip()
            return round(float(precio_limpio), 2)
        
        # Si no es COP, asumimos que es USD y convertimos
        # Limpiar el precio (quitar US, $, espacios, comas)
        precio_limpio = precio_str.replace("US", "").replace("$", "").replace(",", "").strip()
        
        if not precio_limpio or precio_limpio == "0":
            return 0.0
        
        precio_float = float(precio_limpio)
        
        # USAR TRM desde el archivo .env
        tasa_cambio = float(os.getenv("TRM_COP", "4500"))
        precio_cop = precio_float * tasa_cambio
        
        # Redondear a 2 decimales
        return round(precio_cop, 2)
        
    except Exception as e:
        log_message(f"Error al convertir precio '{precio_str}': {e}")
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
        # CONSULTA CORREGIDA: Usar precio_cop para encontrar el más barato
        df = pd.read_sql_query("""
            SELECT 
                p1.categoria as 'Categoría',
                p1.nombre as 'Producto',
                p1.precio as 'Precio',
                p1.precio_cop as 'Precio COP'
            FROM productos p1
            INNER JOIN (
                SELECT categoria, MIN(precio_cop) as min_precio
                FROM productos
                WHERE precio_cop > 0
                GROUP BY categoria
            ) p2 ON p1.categoria = p2.categoria AND p1.precio_cop = p2.min_precio
        """, conn)
        
        # Verificar si hay datos
        if df.empty:
            print("No hay datos para enviar")
            log_message("No hay datos para enviar en el correo")
            return False
        
        # Formatear precio COP
        df['Precio COP'] = df['Precio COP'].apply(lambda x: f"${x:,.2f}")
        
        # Crear Excel
        excel_file = "resumen_productos.xlsx"
        df.to_excel(excel_file, index=False)
        
        # Crear correo
        msg = MIMEMultipart()
        msg['From'] = remitente
        msg['To'] = destinatario
        msg['Subject'] = 'Resumen de Productos Amazon'
        
        # Cuerpo del correo
        cuerpo = f"Adjunto encontraras el resumen de los {len(df)} productos mas baratos encontrados en Amazon."
        msg.attach(MIMEText(cuerpo, 'plain', 'utf-8'))
        
        # Adjuntar Excel
        with open(excel_file, 'rb') as archivo:
            parte = MIMEBase('application', 'octet-stream')
            parte.set_payload(archivo.read())
            encoders.encode_base64(parte)
            parte.add_header(
                'Content-Disposition', 
                f'attachment; filename="{excel_file}"'
            )
            msg.attach(parte)
        
        # Enviar
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        texto = msg.as_string()
        server.sendmail(remitente, destinatario, texto)
        server.quit()
        
        print(f"\n Correo enviado a {destinatario}")
        log_message(f"Correo enviado exitosamente a {destinatario}")
        return True
        
    except Exception as e:
        print(f"\n Error al enviar correo: {e}")
        log_message(f"Error al enviar correo: {e}")
        return False