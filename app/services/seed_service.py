from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.rol import Rol
from app.models.departamento import Departamento
from app.models.municipio import Municipio

def seed_roles(db: Session):
    roles = [
        {"id": 1, "nombre": "Administrador"},
        {"id": 2, "nombre": "Lector"}
    ]

    for role in roles:
        exists = db.scalar(select(Rol).where(Rol.id == role["id"]))
        if not exists:
            db.add(Rol(id=role["id"], nombre=role["nombre"]))

    db.commit()

def seed_departamentos_municipios(db: Session):
    # Definir un set de prueba
    data = {
        "Alta Verapaz": ["Cobán", "Chisec", "San Pedro Carchá"],
        "Baja Verapaz": ["Salamá", "Rabinal"]
    }

    for dep_name, municipios in data.items():
        dep = db.scalar(select(Departamento).where(Departamento.nombre == dep_name))
        if not dep:
            dep = Departamento(nombre=dep_name)
            db.add(dep)
            db.flush()  # obtener id del departamento antes de insertar municipios

        for mun_name in municipios:
            exists = db.scalar(select(Municipio).where(Municipio.nombre == mun_name))
            if not exists:
                db.add(Municipio(nombre=mun_name, id_departamento=dep.id))

    db.commit()
