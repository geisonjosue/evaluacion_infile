from typing import Optional, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc, asc
from app.models.noticia import Noticia
from app.models.categoria import Categoria
from app.models.user import User
from app.schemas.news import DataTableResponse, NoticiaListItem, PageResponse, NewsCard, NoticiaCreate, NoticiaUpdate
import os
from fastapi import UploadFile
from uuid import uuid4
import shutil
from datetime import datetime

STATIC_DIR = os.getenv("STATIC_DIR", "static")

def parse_dt_params(params: dict) -> Tuple[int, int, int, str, str]:
    # extrae draw start length search y sort
    draw = int(params.get("draw", 1))
    start = int(params.get("start", 0))
    length = int(params.get("length", 10))
    search = params.get("search[value]", "") or params.get("search", "")
    order_col = params.get("order[0][column]", "0")
    order_dir = params.get("order[0][dir]", "desc")

    # columnas permitidas
    columns = {
        "0": Noticia.id,
        "1": Noticia.titulo,
        "2": Noticia.fecha_creacion,
        "3": Noticia.estado,
        "4": Noticia.numero_visualizaciones,
        "5": Noticia.noticia_membresia,
    }
    sort_col = columns.get(order_col, Noticia.fecha_creacion)
    sort_dir = desc if order_dir == "desc" else asc
    return draw, start, length, search, sort_dir(sort_col)

def list_news_datatable(db: Session, params: dict) -> DataTableResponse:
    draw, start, length, search, sort_clause = parse_dt_params(params)

    base_q = select(Noticia).join(Categoria, isouter=True).join(User, Noticia.id_usuario == User.id, isouter=True)
    total = db.scalar(select(func.count()).select_from(Noticia)) or 0

    if search:
        like = f"%{search.lower()}%"
        base_q = base_q.where(
            func.lower(Noticia.titulo).like(like) |
            func.lower(Noticia.resumen).like(like)
        )

    filtered = db.scalar(select(func.count()).select_from(base_q.subquery())) or 0

    rows = db.execute(base_q.order_by(sort_clause).offset(start).limit(length)).scalars().all()

    data = []
    for n in rows:
        data.append(NoticiaListItem(
            id=n.id,
            titulo=n.titulo,
            resumen=n.resumen,
            estado=n.estado,
            fecha_creacion=n.fecha_creacion,
            categoria=n.categoria_rel.nombre if n.categoria_rel else None,
            autor=n.autor_rel.nombre if n.autor_rel else None,
            numero_visualizaciones=n.numero_visualizaciones,
            noticia_membresia=n.noticia_membresia
        ))

    return DataTableResponse(draw=draw, recordsTotal=total, recordsFiltered=filtered, data=data)

def list_news_public(db: Session, page: int = 1, page_size: int = 6) -> PageResponse:
    if page < 1:
        page = 1
    total = db.scalar(select(func.count()).select_from(Noticia).where(Noticia.estado.is_(True))) or 0
    offset = (page - 1) * page_size

    q = (
        select(Noticia)
        .where(Noticia.estado.is_(True))
        .order_by(desc(Noticia.fecha_creacion))
        .offset(offset)
        .limit(page_size)
    )
    rows = db.execute(q).scalars().all()

    items = [
        NewsCard(
            id=n.id,
            titulo=n.titulo,
            resumen=n.resumen,
            imagen_destacada=n.imagen_destacada,
            fecha_creacion=n.fecha_creacion,
        )
        for n in rows
    ]
    has_more = offset + len(items) < total
    return PageResponse(items=items, page=page, page_size=page_size, has_more=has_more, total=total)

def create_news(db: Session, payload: NoticiaCreate, user_id: int) -> Noticia:
    n = Noticia(
        titulo=payload.titulo,
        resumen=payload.resumen,
        contenido=payload.contenido,
        id_categoria=payload.id_categoria,
        imagen_destacada=payload.imagen_destacada,
        noticia_membresia=payload.noticia_membresia,
        id_usuario=user_id,
        estado=True,
        fecha_creacion=datetime.utcnow(),
    )
    db.add(n)
    db.commit()
    db.refresh(n)
    return n

def save_image(file: UploadFile) -> str:
    if not file.content_type.startswith("image/"):
        raise ValueError("El archivo debe ser una imagen")
    
    ext = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    path = os.path.join(STATIC_DIR, filename)

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return f"/static/{filename}"

def get_news_by_id(db: Session, news_id: int) -> Optional[Noticia]:
    return db.get(Noticia, news_id)

def update_news(db: Session, news_id: int, payload: NoticiaUpdate) -> Optional[Noticia]:
    noticia = db.get(Noticia, news_id)
    if not noticia or not noticia.estado:
        return None
    for field, value in payload.dict(exclude_unset=True).items():
        setattr(noticia, field, value)
    db.add(noticia)
    db.commit()
    db.refresh(noticia)
    return noticia

def soft_delete_news(db: Session, news_id: int) -> bool:
    noticia = db.get(Noticia, news_id)
    if not noticia or not noticia.estado:
        return False
    noticia.estado = False
    db.add(noticia)
    db.commit()
    return True
