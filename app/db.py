import os
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()

from typing import Generator
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL no esta definido en el archivo .env")

engine = create_engine(DATABASE_URL, pool_pre_ping=True, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

class Base(DeclarativeBase):
    pass

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    # Importa modelos
    from app.models.departamento import Departamento
    from app.models.municipio import Municipio
    from app.models.rol import Rol
    from app.models.user import User
    from app.models.categoria import Categoria
    from app.models.noticia import Noticia

    # Crear tablas
    Base.metadata.create_all(bind=engine)

    # Poblar datos iniciales
    from app.services.seed_service import seed_roles, seed_departamentos_municipios
    db = SessionLocal()
    try:
        seed_roles(db)
        seed_departamentos_municipios(db)
    finally:
        db.close()