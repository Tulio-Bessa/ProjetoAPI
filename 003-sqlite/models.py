from pydantic import BaseModel, ConfigDict

class ProdutoCreate(BaseModel):
    nome: str
    preco: float
    categoria_id: int

class ProdutoOut(BaseModel):
    id: int
    nome: str
    preco: float
    categoria_id: int
    model_config = ConfigDict(from_attributes=True)

class CategoriaCreate(BaseModel):
    nome: str

class CategoriaOut(BaseModel):
    id: int
    nome: str
    model_config = ConfigDict(from_attributes=True)

