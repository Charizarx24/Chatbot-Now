# database.py
import sqlite3

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