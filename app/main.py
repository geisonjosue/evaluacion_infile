from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import init_db
from app.api.v1 import api_v1_router
from fastapi.openapi.utils import get_openapi
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI(title="INFILE News API")

# montar carpeta estatica
static_dir = os.getenv("STATIC_DIR", "static")
os.makedirs(static_dir, exist_ok=True)  # crea la carpeta si no existe
app.mount("/static", StaticFiles(directory=static_dir), name="static")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    init_db()

# incluye todas las rutas versionadas
app.include_router(api_v1_router)

@app.get("/")
def root():
    return {"message": "INFILE News API is running"}

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="INFILE News API",
        version="1.0.0",
        description="API para gestión de noticias",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
