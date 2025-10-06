from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Produto(Base):
    __tablename__ = "produtos"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    preco = Column(Float)
    categoria_id = Column(
        Integer, 
        ForeignKey("categorias.id", ondelete="CASCADE"),
        nullable=False
    )
    categoria = relationship("Categoria", back_populates="produtos")


class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String)
    produtos = relationship(
        "Produto", 
        back_populates="categoria",
        cascade="all, delete-orphan")
