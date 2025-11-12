from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import sqlite3
import sys
import os
import argparse

# Asegurar que Python encuentre el módulo tools
sys.path.append(os.path.dirname(__file__))

from tools import enviar_correo_resumen, read_products, log_message, convertir_a_cop
from db import conectar_db


class AmazonRobot:
    def __init__(self, headless=False):
        """
        Inicializa el robot de Amazon.
        
        Args:
            headless (bool): Si es True, el navegador se ejecuta sin ventana.
                           Si es False, se puede ver el navegador.
        """
        # Obtener directorio actual
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        print(f"Directorio de trabajo: {self.current_dir}")
        
        # Configurar el navegador
        options = Options()
        
        if headless:
            print("Modo headless activado (sin ventana)")
            options.add_argument("--headless=new")
        else:
            print("Modo visual activado (con ventana)")
        
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--start-maximized")
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), 
            options=options
        )
        
        # Conectar a la base de datos SqLite en la raz del proyecto
        db_path = os.path.join(os.path.dirname(self.current_dir), "productos_amazon.db")
        self.conn, self.cursor = conectar_db(db_path)

        # Limpiar la base de datos antes de empecar
        print("Limpiando base de datos anterior...")
        self.cursor.execute("DELETE FROM productos")
        self.conn.commit()
        print("Base de datos limpiada")

        # Leer productos desde productos.xlsx con ruta absoluta
        productos_path = os.path.join(self.current_dir, "productos.xlsx")
        self.products = read_products(productos_path)
        print(f"Productos cargados: {len(self.products)}")

    def search_product(self, product_name):
        """Abre Amazon y busca un producto."""
        print(f"  Navegando a Amazon...")
        self.driver.get("https://www.amazon.com")
        time.sleep(2)
        
        print(f"  Buscando: {product_name}")
        search_box = self.driver.find_element(By.ID, "twotabsearchtextbox")
        search_box.clear()
        search_box.send_keys(product_name)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)
        
        # Seleccionar "Destacados" después de la búsqueda
        self.select_destacados()

    def select_destacados(self):
        """
        Selecciona la opción 'Destacados' (Featured) en el menú de ordenamiento.
        """
        print(f"  Seleccionando 'Destacados'...")
        
        try:
            # Esperar a que aparezca el dropdown de ordenamiento
            wait = WebDriverWait(self.driver, 10)
            
            # Posibles selectores para el dropdown de ordenamiento
            selectores = [
                "span.a-button-text.a-declarative",  # Selector común
                "span[class*='a-dropdown-prompt']",   # Alternativo
                "#s-result-sort-select",              # ID directo del select
            ]
            
            dropdown = None
            for selector in selectores:
                try:
                    dropdown = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, selector)))
                    break
                except:
                    continue
            
            if dropdown:
                # Hacer clic en el dropdown
                dropdown.click()
                time.sleep(1)
                
                # Buscar y hacer clic en "Featured" o "Destacados"
                opciones_destacados = [
                    "//a[contains(text(), 'Featured')]",
                    "//a[contains(text(), 'Destacados')]",
                    "//option[@value='relevanceblender']",
                    "//a[@id='s-result-sort-select_0']",
                ]
                
                for opcion_xpath in opciones_destacados:
                    try:
                        opcion = self.driver.find_element(By.XPATH, opcion_xpath)
                        opcion.click()
                        print(f"    [OK] 'Destacados' seleccionado correctamente")
                        time.sleep(2)
                        return True
                    except:
                        continue
                
                print(f"    [WARNING] No se encontró la opción 'Destacados', continuando...")
                return False
            else:
                print(f"    [WARNING] No se encontró el menú de ordenamiento")
                return False
                
        except Exception as e:
            print(f"    [ERROR] Error al seleccionar 'Destacados': {e}")
            log_message(f"Error al seleccionar destacados: {e}")
            return False

    def extract_product_info(self, product_name):
        """Extrae los primeros 20 productos (nombre, precio, entrega)."""
        print(f"  Extrayendo información de productos...")
        
        # Esperar a que carguen los productos
        time.sleep(3)
        
        # Selector para productos
        products = self.driver.find_elements(
            By.CSS_SELECTOR, 
            "div[data-component-type='s-search-result']"
        )[:20]
        
        print(f"  Productos encontrados: {len(products)}")
        
        product_info = []

        for idx, product in enumerate(products, 1):
            # Extraer título
            try:
                title = product.find_element(By.CSS_SELECTOR, "h2 span").text
            except:
                print(f"    [SKIP] Producto {idx}: Sin título")
                continue
            
            # Extraer precio
            try:
                # Extraer el precio completo como aparece en Amazon
                price_element = product.find_element(By.CSS_SELECTOR, "span.a-price span.a-offscreen")
                price = price_element.get_attribute("textContent").strip()
            except:
                try:
                    # Método alternativo
                    price_whole = product.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
                    price_fraction = product.find_element(By.CSS_SELECTOR, "span.a-price-fraction").text
                    price = f"${price_whole}{price_fraction}"
                except:
                    price = "$0"
            
            # Extraer entrega
            try:
                entrega = product.find_element(By.CSS_SELECTOR, "div.a-row.a-color-base").text
            except:
                entrega = "Sin información"

            precio_cop = convertir_a_cop(price)
            
            data = {
                "categoria": product_name,
                "nombre": title,
                "precio_usd": price,
                "precio_cop": precio_cop,
                "entrega": entrega
            }
            product_info.append(data)
            print(f"    [OK] {idx}: {title[:40]}... - {price} (COP: ${precio_cop:,.0f})")

        print(f"  Total extraídos: {len(product_info)}")
        return product_info

    def save_to_db(self, product_info):
        """Guarda los productos en la base de datos."""
        print(f"  Guardando {len(product_info)} productos en la BD...")
        
        guardados = 0
        errores = 0
        
        for product in product_info:
            try:
                self.cursor.execute("""
                    INSERT INTO productos (categoria, nombre, precio_usd, precio_cop, entrega)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    product['categoria'],
                    product['nombre'],
                    product['precio_usd'],
                    product['precio_cop'],
                    product['entrega']
                ))
                guardados += 1
            except Exception as e:
                errores += 1
                log_message(f"Error guardando producto: {e}")
                print(f"    [ERROR] No se pudo guardar: {product['nombre'][:30]}...")
        
        self.conn.commit()
        print(f"  ✓ Guardados: {guardados} | Errores: {errores}")

    def create_summary(self):
        """Genera un resumen de los productos más baratos por categoría."""
        print("\nGenerando resumen de productos más baratos...")
        
        df = pd.read_sql_query("""
            SELECT categoria, nombre, precio_usd, precio_cop, entrega
            FROM productos
            WHERE precio_cop = (
                SELECT MIN(precio_cop) 
                FROM productos p2 
                WHERE p2.categoria = productos.categoria AND p2.precio_cop > 0
            )
        """, self.conn)
        
        print("\n" + "="*80)
        print("RESUMEN - PRODUCTO MAS BARATO POR CATEGORIA")
        print("="*80)
        
        for _, row in df.iterrows():
            print(f"\nCategoria: {row['categoria']}")
            print(f"  Producto: {row['nombre']}")
            print(f"  Precio USD: {row['precio_usd']}")
            print(f"  Precio COP: ${row['precio_cop']:,.2f}")
            print(f"  Entrega: {row['entrega']}")
        
        print("\n" + "="*80)

    def run(self):
        """Ejecuta el flujo completo del robot."""
        print("\n" + "="*60)
        print("ROBOT DE BUSQUEDA EN AMAZON")
        print("="*60)
        print(f"Productos a buscar: {len(self.products)}\n")
        
        for idx, product_name in enumerate(self.products, 1):
            print(f"\n[{idx}/{len(self.products)}] Buscando: {product_name}")
            print("-" * 60)
            
            try:
                self.search_product(product_name)
                info = self.extract_product_info(product_name)
                self.save_to_db(info)
                time.sleep(2)
            except Exception as e:
                error_msg = f"Error general con {product_name}: {e}"
                log_message(error_msg)
                print(f"  [ERROR] {error_msg}")
                continue

        self.create_summary()

        # Enviar correo con resumen
        enviar_correo_resumen(
            self.conn,
            "jesuslayton92@gmail.com",  
            "jesuslayton92@gmail.com",       
            "eyvk sfry milk gsim"       
        )
        print("\n" + "="*60)
        print("PROCESO COMPLETADO")
        print("="*60)

    

    def close(self):
        """Cierra el navegador y la base de datos."""
        print("\nCerrando navegador y base de datos...")
        self.driver.quit()
        self.conn.close()
        print("Cerrado correctamente")


if __name__ == "__main__":
    # Configurar argumentos de línea de comandos
    parser = argparse.ArgumentParser(description='Robot de busqueda en Amazon')
    parser.add_argument(
        '--visible', 
        action='store_true', 
        help='Ejecutar con el navegador visible'
    )
    parser.add_argument(
        '--headless', 
        action='store_true', 
        help='Ejecutar sin ventana del navegador (por defecto)'
    )
    
    args = parser.parse_args()
    
    # Determinar modo de ejecución
    headless_mode = not args.visible
    
    robot = AmazonRobot(headless=headless_mode)
    try:
        robot.run()
    finally:
        robot.close()