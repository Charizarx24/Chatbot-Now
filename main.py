from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import database  # Módulo personalizado para buscar datos

app = FastAPI()

# Permite CORS (necesario para ManyChat)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
)

# Endpoint para validar estados
@app.get("/validar-estado")
async def validar_estado(
    termino: str = Query(..., alias="estado")
):
    # Normaliza el input
    estado_normalizado = termino.upper().strip()
    
    # Consulta a la base de datos
    estados_validos = database.obtener_estados(estado_normalizado)
    
    # Estructura para ManyChat (Dynamic Content)
    return {
        "version": "v2",
        "content": {
            "type": "instagram",
            "messages": [
                {
                    "type": "text",
                    "text": f"📌 Coincidencias para '{termino}':",
                }
            ],
            "quick_replies": [
                {
                    "type": "node",
                    "caption": f"{estado}",
                    "target": "flujo_seleccion_estado" # Nombre de tu flujo siguiente
                } for estado in estados_validos
            ]
        }
    }

@app.get("/buscar-productos")
async def buscar_productos(termino: str):
    # Normaliza el input
    producto_normalizado = termino.upper().strip()
    
    # Consulta a la base de datos
    productos_validos = database.obtener_productos(producto_normalizado)
    
    # Estructura para ManyChat (Dynamic Content)
    return {
        "version": "v2",
        "content": {
            "type": "instagram",
            "messages": [
                {
                    "type": "text",
                    "text": f"📌 Coincidencias para '{termino}':",
                }
            ],
            "quick_replies": [
                {
                    "type": "node",
                    "caption": f"{producto}",
                    "target": "flujo_seleccion_producto" # Nombre de tu flujo siguiente
                } for producto in productos_validos
            ]
        }
    }

@app.get("/buscar-farmacias")
async def buscar_farmacias(
    estado: str = Query(..., alias="estado"),
    producto: str = Query(..., alias="producto")
):
    # Normaliza los inputs a mayúsculas y sin tildes
    estado_normalizado = estado.upper().strip()
    producto_normalizado = producto.upper().strip()
    
    # Busca en la "base de datos" (Google Sheets, CSV, etc.)
    resultado = database.buscar_en_datos(estado_normalizado, producto_normalizado)
    
    return {
        "estado": estado_normalizado,
        "producto": producto_normalizado,
        "farmacias": "".join([f"\n• {f}" for f in resultado]) if resultado else False
    }

#Run app local -> uvicorn main:app