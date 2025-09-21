from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserBase(BaseModel):
    nombre: str
    telefono: Optional[int] = None
    correo: EmailStr
    id_municipio: Optional[int] = None
    id_rol: Optional[int] = None

class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=128)

class UserRead(UserBase):
    id: int
    estado: bool

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    correo: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    
class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str