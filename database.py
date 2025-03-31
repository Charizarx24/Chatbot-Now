# database.py
import sqlite3

def obtener_estados() -> list:
    """Devuelve una lista de estados únicos registrados en la DB"""
    conn = sqlite3.connect('farmacias.db')
    cursor = conn.cursor()
    
    cursor.execute('SELECT DISTINCT estado FROM productos')
    estados = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    return estados

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
