from pydantic import BaseModel

class MunicipioBase(BaseModel):
    nombre: str
    id_departamento: int

class MunicipioRead(MunicipioBase):
    id: int

    class Config:
        from_attributes = True
