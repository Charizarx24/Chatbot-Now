# database.py
import sqlite3

def obtener_estados(estado: str) -> list:
    """Devuelve una lista de estados que coincidan con el termino de busqueda"""
    conn = sqlite3.connect('farmacias.db')
    cursor = conn.cursor()
    
    cursor.execute("""
    SELECT DISTINCT city
    FROM Farmacias
    WHERE LOWER(city)
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
        SELECT DISTINCT name 
        FROM productos 
        WHERE LOWER(name) LIKE LOWER(?) 
        LIMIT 10
    """, (f"%{termino}%",))
    
    productos = [row[0] for row in cursor.fetchall()]
    conn.close()
    return productos

def buscar_en_datos(estado: str, producto: str) -> list:
    conn = sqlite3.connect("farmacias.db")
    cursor = conn.cursor()
    # Obtener el id del producto
    cursor.execute("""
        SELECT id FROM productos WHERE LOWER(name) = LOWER(?)
    """, (f"{producto}",))
    producto_row = cursor.fetchone()
    if not producto_row:
        conn.close()
        return []
    id_producto = producto_row[0]

    # Obtener los id_farmacia que tienen ese producto
    cursor.execute("""
        SELECT id_farmacia FROM farmaciaxproducto WHERE id_producto = ?
    """, (id_producto,))
    farmacia_ids = [row[0] for row in cursor.fetchall()]
    if not farmacia_ids:
        conn.close()
        return []

    # Buscar farmacias en ese estado con esos id
    placeholders = ",".join("?" for _ in farmacia_ids)
    query = f"""
        SELECT name, contact FROM farmacias
        WHERE id IN ({placeholders}) AND LOWER(city) = LOWER(?)
    """
    cursor.execute(query, (*farmacia_ids, estado))
    farmacias = [(row[0], row[1]) for row in cursor.fetchall()]

    conn.close()
    return farmacias