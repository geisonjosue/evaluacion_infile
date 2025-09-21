from datetime import datetime
from sqlalchemy import Integer, String, Boolean, ForeignKey, Text, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class Noticia(Base):
    __tablename__ = "noticia"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    estado: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    numero_visualizaciones: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    noticia_membresia: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    fecha_creacion: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

    imagen_escaneada: Mapped[str | None] = mapped_column(String(255), nullable=True)
    titulo: Mapped[str] = mapped_column(String(100), nullable=False)
    imagen_destacada: Mapped[str | None] = mapped_column(String(255), nullable=True)
    resumen: Mapped[str | None] = mapped_column(String(150), nullable=True)
    contenido: Mapped[str | None] = mapped_column(Text, nullable=True)

    id_categoria: Mapped[int | None] = mapped_column(ForeignKey("categoria.id"), nullable=True)
    id_usuario: Mapped[int | None] = mapped_column(ForeignKey("usuario.id"), nullable=True)

    categoria_rel = relationship("Categoria", back_populates="noticias")
    autor_rel = relationship("User")
