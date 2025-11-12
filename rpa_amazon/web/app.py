from flask import Flask, render_template, request
import sqlite3
import os

app = Flask(__name__)

def get_db_connection():
    """Conecta a la base de datos"""
    db_path = os.path.join(os.path.dirname(__file__), '..', 'productos_amazon.db')
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    
    # Obtener filtros
    categoria = request.args.get('categoria', '')
    precio_min = request.args.get('precio_min', '')
    precio_max = request.args.get('precio_max', '')
    
    # Construir consulta
    query = "SELECT * FROM productos WHERE 1=1"
    params = []
    
    if categoria:
        query += " AND categoria LIKE ?"
        params.append(f"%{categoria}%")
    
    if precio_min:
        query += " AND precio_cop >= ?"
        params.append(float(precio_min))
    
    if precio_max:
        query += " AND precio_cop <= ?"
        params.append(float(precio_max))
    
    query += " ORDER BY categoria, precio_cop"
    
    productos = conn.execute(query, params).fetchall()
    
    # Obtener categorías únicas
    categorias = conn.execute("SELECT DISTINCT categoria FROM productos ORDER BY categoria").fetchall()
    
    conn.close()
    
    return render_template('index.html', 
                         productos=productos, 
                         categorias=categorias,
                         categoria_filtro=categoria,
                         precio_min_filtro=precio_min,
                         precio_max_filtro=precio_max)

if __name__ == '__main__':
    app.run(debug=True, port=5000)