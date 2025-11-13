# Consideraciones del Proyecto RPA Amazon

## Manejo de Precios

Amazon muestra precios en USD o COP de forma inconsistente. La solución detecta automáticamente la moneda y convierte USD a COP usando la TRM configurada en `.env`.

**Mejora futura**: Consumir API del Banco de la República para TRM automática.

## Productos Extraídos

A veces se extraen menos de 20 productos por:
- Productos sin título o precio visible
- Elementos patrocinados con HTML diferente
- Productos con "más opciones de compra"

Esto es normal y no afecta la funcionalidad.

## Ejecución

- **Robot**: Local (necesita Chrome)
- **API/Web**: Docker

## CAPTCHA y Bloqueos

Si Amazon detecta scraping intensivo, puede mostrar CAPTCHA. Solución: aumentar tiempos de espera en `.env`.

## Correo Gmail

Requiere "contraseña de aplicación" de Google (no la contraseña normal). Generar desde configuración de seguridad de Google.

## Seguridad y Autenticación

⚠️ **La web y API no tienen login ni autenticación por limitaciones de tiempo.**

**Mejoras futuras recomendadas**:
- Implementar autenticación (JWT o sesiones)
- HTTPS
- Rate limiting en API
- Validación de usuarios

## Mantenimiento

Revisar periódicamente:
- TRM actualizada en `.env`
- Selectores de Amazon (si cambian su HTML)
- Logs de errores en `log.txt`

## Limitaciones

- Solo primera página de resultados (sin paginación)
- Sin login/autenticación
- Límite de 20 productos por categoría
- Base de datos SQLite (suficiente para volumen actual)