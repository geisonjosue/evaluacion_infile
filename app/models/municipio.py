from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class Municipio(Base):
    __tablename__ = "municipio"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)

    id_departamento: Mapped[int] = mapped_column(ForeignKey("departamento.id"), nullable=False)

    usuarios = relationship("User", back_populates="municipio_rel")
    departamento_rel = relationship("Departamento", back_populates="municipios")
