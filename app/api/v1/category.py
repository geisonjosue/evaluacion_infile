from fastapi import APIRouter, Depends, Request, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db import get_db
from app.models.user import User
from app.schemas.category import CategoriaCreate, CategoriaUpdate, CategoriaRead, DataTableResponse
from app.services.category_service import (
    list_categories_datatable,
    create_category,
    update_category,
    soft_delete_category
)

router = APIRouter(
    prefix="/categories",
    tags=["Categorias"],
    dependencies=[Depends(get_current_user)]
)

# Listado datatable
@router.get("/", response_model=DataTableResponse)
def list_admin_datatable(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = dict(request.query_params)
    return list_categories_datatable(db, params)

# Crear
@router.post("/", response_model=CategoriaRead, status_code=status.HTTP_201_CREATED)
def crear_categoria(payload: CategoriaCreate, db: Session = Depends(get_db)):
    return create_category(db, payload)

# Editar
@router.put("/{id}", response_model=CategoriaRead)
def editar_categoria(id: int, payload: CategoriaUpdate, db: Session = Depends(get_db)):
    categoria = update_category(db, id, payload)
    if not categoria:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return categoria

# Delete logico
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_categoria(id: int, db: Session = Depends(get_db)):
    ok = soft_delete_category(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return None
