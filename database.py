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
    estado: str = Query(..., alias="estado")
):
    # Normaliza el input
    estado_normalizado = estado.upper().strip()
    
    # Consulta a la base de datos
    estados_validos = database.obtener_estados()
    
    # Verifica si el estado existe
    es_valido = estado_normalizado in estados_validos
    
    return {
        "estado_ingresado": estado,
        "es_valido": es_valido
        #"estados_validos": estados_validos if not es_valido else None  # Opcional: enviar lista si es inválido
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
        "farmacias": resultado if resultado else "No encontrado"
    }
