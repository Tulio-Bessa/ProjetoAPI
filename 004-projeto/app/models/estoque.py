from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
from app.db.base import Base

class TipoMovimento(str, enum.Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"

class EstoqueMovimento(Base):
    __tablename__ = "estoque_movimentos"

    id = Column(Integer, primary_key=True, index=True)
    produto_id = Column(Integer, ForeignKey("produtos.id", ondelete="CASCADE"), nullable=False)
    tipo = Column(Enum(TipoMovimento), nullable=False)
    quantidade = Column(Integer, nullable=False)
    motivo = Column(String, nullable=True)
    criado_em = Column(DateTime, default=datetime.utcnow)

    produto = relationship("Produto", backref="movimentos")
