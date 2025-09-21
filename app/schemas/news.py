from pydantic import BaseModel, Field
from typing import Optional, Any

class CategoriaBase(BaseModel):
    nombre: str

class CategoriaRead(CategoriaBase):
    id: int
    estado: bool
    class Config:
        from_attributes = True

class NoticiaBase(BaseModel):
    titulo: str
    resumen: Optional[str] = None
    contenido: Optional[str] = None
    id_categoria: Optional[int] = None
    imagen_destacada: Optional[str] = None
    noticia_membresia: bool = False

class NoticiaCreate(NoticiaBase):
    pass

class NoticiaRead(BaseModel):
    id: int
    estado: bool
    titulo: str
    resumen: Optional[str] = None
    imagen_destacada: Optional[str] = None
    noticia_membresia: bool
    fecha_creacion: Any
    id_categoria: Optional[int] = None
    id_usuario: Optional[int] = None
    class Config:
        from_attributes = True

class NoticiaUpdate(BaseModel):
    titulo: Optional[str] = None
    contenido: Optional[str] = None
    id_categoria: Optional[int] = None
    imagen: Optional[str] = None

# item que ve el admin en el datatable sin contenido
class NoticiaListItem(BaseModel):
    id: int
    titulo: str
    resumen: Optional[str] = None
    estado: bool
    fecha_creacion: Any
    categoria: Optional[str] = None
    autor: Optional[str] = None
    numero_visualizaciones: int
    noticia_membresia: bool

# respuesta para datatables server side
class DataTableResponse(BaseModel):
    draw: int
    recordsTotal: int
    recordsFiltered: int
    data: list[NoticiaListItem]

# cards para lector 6 en 6
class NewsCard(BaseModel):
    id: int
    titulo: str
    resumen: Optional[str] = None
    imagen_destacada: Optional[str] = None
    fecha_creacion: Any

class PageResponse(BaseModel):
    items: list[NewsCard]
    page: int
    page_size: int
    has_more: bool
    total: int
