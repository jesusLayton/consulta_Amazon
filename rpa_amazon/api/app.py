from fastapi import FastAPI, HTTPException
import sqlite3
import os

app = FastAPI(title="API Productos Amazon")

def get_db_connection():
    """Conecta a la base de datos"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'productos_amazon.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.get("/")
def root():
    """Endpoint raíz"""
    return {
        "mensaje": "API de Productos Amazon",
        "endpoints": {
            "/producto/{id}": "Obtener producto por ID",
            "/productos": "Listar todos los productos",
            "/docs": "Documentación interactiva"
        }
    }

@app.get("/producto/{id}")
def get_producto(id: int):
    """
    Obtiene un producto por su ID      
    """
    conn = get_db_connection()
    producto = conn.execute("SELECT * FROM productos WHERE id = ?", (id,)).fetchone()
    conn.close()
    
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    
    return {
        "id": producto["id"],
        "categoria": producto["categoria"],
        "nombre": producto["nombre"],
        "precio": producto["precio"],
        "precio_cop": producto["precio_cop"],
        "entrega": producto["entrega"]

    }

@app.get("/productos")
def get_productos(categoria: str = None, limite: int = 100):
    """
    Lista todos los productos (opcional: filtrar por categoría)
    """
    conn = get_db_connection()
    
    if categoria:
        productos = conn.execute(
            "SELECT * FROM productos WHERE categoria LIKE ? LIMIT ?", 
            (f"%{categoria}%", limite)
        ).fetchall()
    else:
        productos = conn.execute("SELECT * FROM productos LIMIT ?", (limite,)).fetchall()
    
    conn.close()
    
    return {
        "total": len(productos),
        "productos": [
            {
                "id": p["id"],
                "categoria": p["categoria"],
                "nombre": p["nombre"],
                "precio": p["precio"],
                "precio_cop": p["precio_cop"],
                "entrega": p["entrega"]

            }
            for p in productos
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)