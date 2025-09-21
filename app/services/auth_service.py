from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import verify_password, create_access_token
from fastapi import HTTPException, status
from datetime import timedelta

def authenticate_user(db: Session, correo: str, password: str):
    user = db.query(User).filter(User.correo == correo).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")
    if not user.confirmacion:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Usuario no confirmado")
    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales invalidas")
    return user

def login_user(db: Session, correo: str, password: str):
    user = authenticate_user(db, correo, password)
    access_token_expires = timedelta(minutes=60)
    access_token = create_access_token(
        data={"sub": str(user.id), "correo": user.correo},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
