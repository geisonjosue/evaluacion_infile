from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserRead, LoginRequest, TokenResponse, ChangePasswordRequest
from app.services.user_service import create_user, confirm_user, update_password
from app.core.security import (
    verify_confirmation_token,
    create_reset_token,
    verify_reset_token,
    get_current_user,
    verify_password,
    get_password_hash
)
from app.services.auth_service import login_user
from app.services.email import send_confirmation_email, send_reset_password_email

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return create_user(db, user_in)

@router.get("/confirm/{token}", response_model=UserRead)
def confirm_account(token: str, db: Session = Depends(get_db)):
    user_id = verify_confirmation_token(token)
    if not user_id:
        raise HTTPException(status_code=400, detail="Token invalido o expirado")
    return confirm_user(db, user_id)

@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest, db: Session = Depends(get_db)):
    return login_user(db, request.correo, request.password)

@router.post("/forgot-password")
def forgot_password(correo: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.correo == correo).first()
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    token = create_reset_token(user.id)
    send_reset_password_email(user.correo, token)

    return {"message": "Se ha enviado un correo con instrucciones para restablecer la contraseña"}

@router.post("/reset-password")
def reset_password(token: str, new_password: str, db: Session = Depends(get_db)):
    user_id = verify_reset_token(token)
    if not user_id:
        raise HTTPException(status_code=400, detail="Token inválido o expirado")

    user = update_password(db, user_id, new_password)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return {"message": "Contraseña actualizada correctamente"}

@router.put("/change-password")
def change_password(
    body: ChangePasswordRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verificar la contraseña actual usando hashed_password
    if not verify_password(body.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="La contraseña actual es incorrecta"
        )

    # Guardar nueva contraseña hasheada
    current_user.hashed_password = get_password_hash(body.new_password)
    db.add(current_user)
    db.commit()
    db.refresh(current_user)

    return {"message": "Contraseña cambiada correctamente"}

