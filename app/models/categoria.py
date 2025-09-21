from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class Categoria(Base):
    __tablename__ = "categoria"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    estado: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    noticias = relationship("Noticia", back_populates="categoria_rel")
