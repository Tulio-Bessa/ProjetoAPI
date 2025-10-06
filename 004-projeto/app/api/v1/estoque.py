from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.deps import get_db
from app.schemas.estoque import MovimentoCreate, MovimentoOut, VendaCreate, DevolucaoCreate, AjusteCreate, ResumoEstoqueOut
from app.repositories import estoque as repo

rotas = APIRouter(prefix="/api/v1/estoque", tags=["Estoque"])

@rotas.post("/movimentos", response_model=MovimentoOut)
def criar_movimento(payload: MovimentoCreate, db: Session = Depends(get_db)):
    mov = repo.create_movimento(db, payload)
    return mov

@rotas.post("/venda", response_model=MovimentoOut)
def criar_venda(payload: VendaCreate, db: Session = Depends(get_db)):
    mov = repo.create_venda(db, payload.produto_id, payload.quantidade)
    return mov

@rotas.post("/devolucao", response_model=MovimentoOut)
def criar_devolucao(payload: DevolucaoCreate, db: Session = Depends(get_db)):
    mov = repo.create_devolucao(db, payload.produto_id, payload.quantidade)
    return mov

@rotas.post("/ajuste", response_model=MovimentoOut)
def criar_ajuste(payload: AjusteCreate, db: Session = Depends(get_db)):
    mov = repo.create_ajuste(db, payload.produto_id, payload.tipo, payload.quantidade, payload.motivo)
    return mov

@rotas.get("/extrato/{produto_id}", response_model=list[MovimentoOut])
def extrato(produto_id: int, limit: int = 50, offset: int = 0, db: Session = Depends(get_db)):
    from app.models.produto import Produto
    produto = db.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")
    return repo.get_extrato(db, produto_id, limit, offset)

@rotas.get("/resumo", response_model=list[ResumoEstoqueOut])
def resumo(db: Session = Depends(get_db)):
    return repo.get_resumo(db)

@rotas.get("/produtos/abaixo-minimo", response_model=list[ResumoEstoqueOut])
def produtos_abaixo(db: Session = Depends(get_db)):
    return repo.get_produtos_abaixo_minimo(db)

@rotas.get("/saldo/{produto_id}")
def saldo_produto(produto_id: int, db: Session = Depends(get_db)):
    from app.models.produto import Produto
    produto = db.get(Produto, produto_id)
    if not produto:
        raise HTTPException(status_code=404, detail="Produto nao encontrado")
    saldo = repo.get_saldo(db, produto_id)
    return {"produto_id": produto_id, "saldo": saldo}
