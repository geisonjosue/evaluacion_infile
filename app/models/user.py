from sqlalchemy import Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class User(Base):
    __tablename__ = "usuario"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    estado: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    confirmacion: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)  
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    telefono: Mapped[int | None] = mapped_column(Integer, nullable=True)
    correo: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)

    id_municipio: Mapped[int | None] = mapped_column(ForeignKey("municipio.id"), nullable=True)
    id_rol: Mapped[int | None] = mapped_column(ForeignKey("rol.id"), nullable=True)

    municipio_rel = relationship("Municipio", back_populates="usuarios")
    rol_rel = relationship("Rol", back_populates="usuarios")
