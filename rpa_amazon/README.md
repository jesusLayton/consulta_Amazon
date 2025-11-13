
# RPA Amazon - Sistema de Consulta de Productos

Sistema automatizado para consultar y comparar productos en Amazon, con API REST, interfaz web y notificaciones por correo.

## Características

- 🤖 Robot de scraping con Selenium
- 📊 API REST con FastAPI
- 🌐 Interfaz web con Flask
- 📧 Notificación por correo con Excel
- 🐳 Dockerizado completamente
- 💾 Base de datos SQLite
- 📝 Sistema de logging con timestamp

## Requisitos

- Python 3.11+
- Docker y Docker Compose
- Google Chrome (para el robot)
- Cuenta Gmail (para notificaciones)

## Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/tu-usuario/rpa_amazon.git
cd rpa_amazon
```

### 2. Configurar variables de entorno

Crear archivo `.env` en la raíz:
```env
# Correo
EMAIL_REMITENTE=tu_correo@gmail.com
EMAIL_DESTINATARIO=destinatario@gmail.com
EMAIL_PASSWORD=contraseña_aplicacion_google

# Finanzas
TRM_COP=4200

# Amazon
AMAZON_URL=https://www.amazon.com
PRODUCTOS_A_EXTRAER=20

# Archivos
ARCHIVO_PRODUCTOS=productos.xlsx
NOMBRE_BASE_DATOS=productos_amazon.db

# Tiempos (segundos)
TIEMPO_ESPERA_CARGA=3
TIEMPO_ESPERA_BUSQUEDA=2
```

### 3. Configurar productos a buscar

Editar `robot/productos.xlsx` con las categorías deseadas (una por fila).

## Uso

### Levantar servicios (API + Web)
```bash
docker-compose build
docker-compose up
```

### Ejecutar robot de scraping
```bash
cd robot
python robot_amazon.py --visible
```

### Acceder a los servicios

- **Web**: http://localhost:5000
- **API**: http://localhost:8000
- **Documentación API**: http://localhost:8000/docs

## Estructura del Proyecto
```
rpa_amazon/
├── robot/                  # Robot de scraping
│   ├── robot_amazon.py
│   ├── tools.py
│   ├── db.py
│   ├── productos.xlsx
│   └── log.txt
├── api/                    # API REST
│   └── app.py
├── web/                    # Interfaz web
│   ├── app.py
│   └── templates/
│       └── index.html
├── docker-compose.yml
├── Dockerfile
├── .env
└── productos_amazon.db
```

## Funcionalidades

### Robot de Scraping

1. Lee categorías desde `productos.xlsx`
2. Busca en Amazon
3. Extrae primeros 20 productos por categoría:
   - Nombre
   - Precio (USD o COP)
   - Tipo de entrega
4. Convierte precios a COP automáticamente
5. Guarda en base de datos
6. Envía correo con Excel de productos más baratos

### API REST

**Endpoints disponibles:**

- `GET /` - Información de la API
- `GET /producto/{id}` - Consultar producto por ID
- `GET /productos?categoria=xbox&limite=100` - Listar productos con filtros

### Interfaz Web

- Visualización de productos
- Filtros por categoría
- Filtros por rango de precios en COP
- Diseño responsive

## Tecnologías

- **Python 3.11**
- **Selenium** - Web scraping
- **FastAPI** - API REST
- **Flask** - Interfaz web
- **SQLite** - Base de datos
- **Docker** - Containerización
- **pandas** - Procesamiento de datos

## Notas Importantes

### Contraseña de Gmail

Debes generar una "contraseña de aplicación" en Google (no tu contraseña normal):
1. Ir a cuenta de Google → Seguridad
2. Activar verificación en 2 pasos
3. Generar contraseña de aplicación
4. Usar esa contraseña en `.env`

### Precios USD/COP

Amazon muestra precios en diferentes monedas. El sistema detecta automáticamente y convierte a COP usando la TRM del `.env`.

### Productos Extraídos

Pueden extraerse menos de 20 productos si algunos no tienen precio o título visible. Esto es normal.

## Logs

Todo se registra en `robot/log.txt` con timestamp:
```
[2025-11-13 23:45:12] Directorio de trabajo: C:\Users\...
[2025-11-13 23:45:13] Productos cargados: 4
[2025-11-13 23:45:15] Navegando a Amazon
```

## Solución de Problemas

**El robot no encuentra productos:**
- Verificar que Amazon no haya cambiado selectores HTML
- Aumentar tiempos de espera en `.env`

**Error al enviar correo:**
- Verificar contraseña de aplicación de Google
- Verificar que verificación en 2 pasos esté activa

**Docker no levanta:**
- Verificar que Docker Desktop esté corriendo
- Verificar puertos 5000 y 8000 disponibles

## Limitaciones

- Sin autenticación en web/API (mejora futura)
- Solo primera página de resultados
- Límite de 20 productos por categoría
- Robot se ejecuta local (no en Docker)

## Mejoras Futuras

- Autenticación JWT en API
- TRM automática desde API del Banco de la República
- Paginación de resultados
- Robot completamente dockerizado
- Tests unitarios e integración

## Licencia

MIT

## Autor

[Tu Nombre]

## Contacto

Para dudas o sugerencias: tu_correo@ejemplo.com