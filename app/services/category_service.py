from sqlalchemy.orm import Session
from sqlalchemy import select, func, desc, asc
from app.models.categoria import Categoria
from app.schemas.category import (
    CategoriaCreate,
    CategoriaUpdate,
    CategoriaListItem,
    DataTableResponse
)

def parse_dt_params(params: dict):
    draw = int(params.get("draw", 1))
    start = int(params.get("start", 0))
    length = int(params.get("length", 10))
    search = params.get("search[value]", "") or params.get("search", "")
    order_col = params.get("order[0][column]", "0")
    order_dir = params.get("order[0][dir]", "desc")

    columns = {
        "0": Categoria.id,
        "1": Categoria.nombre,
        "2": Categoria.estado,
    }
    sort_col = columns.get(order_col, Categoria.id)
    sort_dir = desc if order_dir == "desc" else asc
    return draw, start, length, search, sort_dir(sort_col)


def list_categories_datatable(db: Session, params: dict) -> DataTableResponse:
    draw, start, length, search, sort_clause = parse_dt_params(params)

    base_q = select(Categoria)
    total = db.scalar(select(func.count()).select_from(Categoria)) or 0

    if search:
        like = f"%{search.lower()}%"
        base_q = base_q.where(func.lower(Categoria.nombre).like(like))

    filtered = db.scalar(select(func.count()).select_from(base_q.subquery())) or 0
    rows = db.execute(base_q.order_by(sort_clause).offset(start).limit(length)).scalars().all()

    data = [
        CategoriaListItem(
            id=c.id,
            nombre=c.nombre,
            estado=c.estado,
        )
        for c in rows
    ]

    return DataTableResponse(draw=draw, recordsTotal=total, recordsFiltered=filtered, data=data)

def create_category(db: Session, payload: CategoriaCreate) -> Categoria:
    c = Categoria(nombre=payload.nombre, estado=True)
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

def update_category(db: Session, id: int, payload: CategoriaUpdate) -> Categoria | None:
    c = db.get(Categoria, id)
    if not c or not c.estado:
        return None
    c.nombre = payload.nombre
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

def soft_delete_category(db: Session, id: int) -> bool:
    c = db.get(Categoria, id)
    if not c or not c.estado:
        return False
    c.estado = False
    db.add(c)
    db.commit()
    return True
