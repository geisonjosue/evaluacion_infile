from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db import Base

class Departamento(Base):
    __tablename__ = "departamento"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)

    municipios = relationship("Municipio", back_populates="departamento_rel")
