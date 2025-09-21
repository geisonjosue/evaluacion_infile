from pydantic import BaseModel
from typing import List

class CategoriaBase(BaseModel):
    nombre: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaUpdate(CategoriaBase):
    pass

class CategoriaRead(CategoriaBase):
    id: int
    estado: bool

    class Config:
        orm_mode = True

# Para datatable
class CategoriaListItem(BaseModel):
    id: int
    nombre: str
    estado: bool

    class Config:
        orm_mode = True

class DataTableResponse(BaseModel):
    draw: int
    recordsTotal: int
    recordsFiltered: int
    data: List[CategoriaListItem]
