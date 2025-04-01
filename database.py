# database.py
import sqlite3

def obtener_estados(estado: str) -> list:
    """Devuelve una lista de estados que coincidan con el termino de busqueda"""
    conn = sqlite3.connect('farmacias.db')
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT DISTINCT estado
    FROM productos
    WHERE LOWER(estado)
    LIKE LOWER(?)
    LIMIT 10
    """, (f"%{estado}%",))
    estados = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return estados

def obtener_productos(termino: str) -> list:
    conn = sqlite3.connect('farmacias.db')
    cursor = conn.cursor()
    
    # Búsqueda parcial (ejemplo con LIKE de SQL)
    cursor.execute("""
        SELECT DISTINCT producto 
        FROM productos 
        WHERE LOWER(producto) LIKE LOWER(?) 
        LIMIT 10
    """, (f"%{termino}%",))
    
    productos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return productos

def buscar_en_datos(estado: str, producto: str) -> list:
    conn = sqlite3.connect("farmacias.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT farmacias FROM productos 
        WHERE estado = ? AND producto = ?
    """, (estado, producto))
    
    resultado = cursor.fetchone()
    conn.close()
    
    return resultado[0].split(", ") if resultado else None
