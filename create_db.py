import sqlite3

# Crear conexión y base de datos
conn = sqlite3.connect('farmacias.db')
cursor = conn.cursor()

# Crear tabla 'productos'
cursor.execute('''
CREATE TABLE IF NOT EXISTS productos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    estado TEXT NOT NULL,
    producto TEXT NOT NULL,
    farmacias TEXT NOT NULL
)
''')

# Insertar datos de ejemplo
datos_ejemplo = [
    ('ZULIA', 'PARACETAMOL', 'Farmacia Guadalajara, Farmacia San Juan'),
    ('CARACAS', 'IBUPROFENO', 'Farmacia Roma, Farmacia Condesa'),
    ('CARABOBO', 'AMOXICILINA', 'Farmacia Monterrey, Farmacia San Pedro'),
    ('TEST1', 'PARACETAMOL', 'Farmacia Cancún, Farmacia Playa'),
]

cursor.executemany(
    'INSERT INTO productos (estado, producto, farmacias) VALUES (?, ?, ?)',
    datos_ejemplo
)


# Guardar cambios y cerrar conexión
conn.commit()
conn.close()

print("Base de datos 'farmacias.db' creada con éxito!")