from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException, status
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.core.security import get_password_hash, create_confirmation_token
from app.services.email import send_confirmation_email

def get_user_by_email(db: Session, correo: str) -> User | None:
    return db.scalar(select(User).where(User.correo == correo))

def create_user(db: Session, user_in: UserCreate) -> UserRead:
    # Validar si el correo ya existe
    if get_user_by_email(db, user_in.correo):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ya esta registrado"
        )

    hashed_password = get_password_hash(user_in.password)

    user = User(
        nombre=user_in.nombre,
        telefono=user_in.telefono,
        correo=user_in.correo,
        id_municipio=user_in.id_municipio,
        id_rol=user_in.id_rol or 2,
        hashed_password=hashed_password,
        estado=True,
        confirmacion=False
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # Generar token y enviar email
    token = create_confirmation_token(user.id)
    send_confirmation_email(user.correo, token)

    return user

def confirm_user(db: Session, user_id: int):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    if user.confirmacion:
        raise HTTPException(status_code=400, detail="Usuario ya confirmado")

    user.confirmacion = True
    db.commit()
    db.refresh(user)
    return user

def update_password(db: Session, user_id: int, new_password: str):
    user = db.get(User, user_id)
    if not user:
        return None
    user.hashed_password = get_password_hash(new_password)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

