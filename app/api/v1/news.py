from fastapi import APIRouter, Depends, Query, Request, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.db import get_db
from app.models.user import User
from app.services.news_service import (
    list_news_datatable,
    list_news_public,
    create_news,
    save_image,
    get_news_by_id,
    update_news,
    soft_delete_news
)
from app.schemas.news import DataTableResponse, PageResponse, NoticiaCreate, NoticiaRead, NoticiaUpdate


router = APIRouter(
    prefix="/news",
    tags=["Noticias"],
    dependencies=[Depends(get_current_user)]  
)

# Listar noticias para admin en datatable
@router.get("/", response_model=DataTableResponse)
def list_admin_datatable(
    request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    params = dict(request.query_params)
    return list_news_datatable(db, params)

# Listar noticias para lector publico en cards 6 en 6
@router.get("/cards", response_model=PageResponse)
def list_cards(
    page: int = Query(1, ge=1),
    page_size: int = Query(6, ge=1, le=50),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return list_news_public(db, page=page, page_size=page_size)

# Crear noticia
@router.post("/", response_model=NoticiaRead, status_code=status.HTTP_201_CREATED)
def crear_noticia(
    payload: NoticiaCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return create_news(db, payload, user_id=current_user.id)

# Subir imagen
@router.post("/upload-image")
def upload_image(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    try:
        path = save_image(file)
        return {"path": path}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Obtener noticia por ID
@router.get("/{id}", response_model=NoticiaRead)
def get_noticia(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    noticia = get_news_by_id(db, id)
    if not noticia or not noticia.estado:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    return noticia


# Editar noticia
@router.put("/{id}", response_model=NoticiaRead)
def editar_noticia(
    id: int,
    payload: NoticiaUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    noticia = update_news(db, id, payload)
    if not noticia:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    return noticia


# Delete logico
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_noticia(
    id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ok = soft_delete_news(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="Noticia no encontrada")
    return None
