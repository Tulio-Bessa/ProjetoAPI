from pydantic import BaseModel, ConfigDict, conint
from datetime import datetime
from enum import Enum

class TipoMovimento(str, Enum):
    ENTRADA = "ENTRADA"
    SAIDA = "SAIDA"

class MovimentoCreate(BaseModel):
    produto_id: int
    tipo: TipoMovimento
    quantidade: conint(gt=0)
    motivo: str | None = None

class MovimentoOut(MovimentoCreate):
    id: int
    criado_em: datetime
    model_config = ConfigDict(from_attributes=True)

class VendaCreate(BaseModel):
    produto_id: int
    quantidade: conint(gt=0)

class DevolucaoCreate(BaseModel):
    produto_id: int
    quantidade: conint(gt=0)

class AjusteCreate(BaseModel):
    produto_id: int
    tipo: TipoMovimento
    quantidade: conint(gt=0)
    motivo: str

class SaldoOut(BaseModel):
    produto_id: int
    saldo: int
    model_config = ConfigDict(from_attributes=True)

class ResumoEstoqueOut(BaseModel):
    produto_id: int
    nome: str
    saldo: int
    estoque_minimo: int
    abaixo_minimo: bool
    model_config = ConfigDict(from_attributes=True)
