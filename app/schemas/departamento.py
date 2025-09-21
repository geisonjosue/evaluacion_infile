from pydantic import BaseModel

class DepartamentoBase(BaseModel):
    nombre: str

class DepartamentoRead(DepartamentoBase):
    id: int

    class Config:
        from_attributes = True
