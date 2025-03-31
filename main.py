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