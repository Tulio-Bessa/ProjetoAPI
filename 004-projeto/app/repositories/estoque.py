from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException
from app.models.estoque import EstoqueMovimento, TipoMovimento
from app.models.produto import Produto
from app.core.config import settings

def create_movimento(db: Session, payload) -> EstoqueMovimento:
    produto = db.get(Produto, payload.produto_id)
    if not produto or not produto.ativo:
        raise HTTPException(status_code=404, detail="Produto nao encontrado ou inativo")

    if payload.tipo == TipoMovimento.SAIDA:
        saldo_atual = get_saldo(db, payload.produto_id)
        if not settings.ALLOW_NEGATIVE_STOCK and saldo_atual < payload.quantidade:
            raise HTTPException(status_code=400, detail=f"Saldo insuficiente: {saldo_atual}")

    movimento = EstoqueMovimento(
        produto_id=payload.produto_id,
        tipo=payload.tipo,
        quantidade=payload.quantidade,
        motivo=payload.motivo
    )
    db.add(movimento)
    db.commit()
    db.refresh(movimento)
    return movimento

def create_venda(db: Session, produto_id: int, quantidade: int):
    class _P: pass
    payload = _P()
    payload.produto_id = produto_id
    payload.tipo = TipoMovimento.SAIDA
    payload.quantidade = quantidade
    payload.motivo = "venda"
    return create_movimento(db, payload)

def create_devolucao(db: Session, produto_id: int, quantidade: int):
    class _P: pass
    payload = _P()
    payload.produto_id = produto_id
    payload.tipo = TipoMovimento.ENTRADA
    payload.quantidade = quantidade
    payload.motivo = "devolucao"
    return create_movimento(db, payload)

def create_ajuste(db: Session, produto_id: int, tipo: TipoMovimento, quantidade: int, motivo: str):
    if not motivo or motivo.strip() == "":
        raise HTTPException(status_code=400, detail="Motivo obrigatorio para ajuste")
    class _P: pass
    payload = _P()
    payload.produto_id = produto_id
    payload.tipo = tipo
    payload.quantidade = quantidade
    payload.motivo = motivo
    return create_movimento(db, payload)

def get_saldo(db: Session, produto_id: int) -> int:
    entradas = db.query(func.coalesce(func.sum(EstoqueMovimento.quantidade), 0)).filter(
        EstoqueMovimento.produto_id == produto_id,
        EstoqueMovimento.tipo == TipoMovimento.ENTRADA
    ).scalar() or 0

    saidas = db.query(func.coalesce(func.sum(EstoqueMovimento.quantidade), 0)).filter(
        EstoqueMovimento.produto_id == produto_id,
        EstoqueMovimento.tipo == TipoMovimento.SAIDA
    ).scalar() or 0

    return int(entradas) - int(saidas)

def get_extrato(db: Session, produto_id: int, limit: int = 50, offset: int = 0):
    q = db.query(EstoqueMovimento).filter(EstoqueMovimento.produto_id==produto_id).order_by(EstoqueMovimento.criado_em.desc()).limit(limit).offset(offset)
    return q.all()

def get_resumo(db: Session):
    produtos = db.query(Produto).all()
    resumo = []
    for p in produtos:
        saldo = get_saldo(db, p.id)
        resumo.append({
            "produto_id": p.id,
            "nome": p.nome,
            "saldo": saldo,
            "estoque_minimo": p.estoque_minimo or 0,
            "abaixo_minimo": saldo < (p.estoque_minimo or 0)
        })
    return resumo

def get_produtos_abaixo_minimo(db: Session):
    produtos = db.query(Produto).all()
    resultados = []
    for p in produtos:
        saldo = get_saldo(db, p.id)
        if saldo < (p.estoque_minimo or 0):
            resultados.append({
                "produto_id": p.id,
                "nome": p.nome,
                "saldo": saldo,
                "estoque_minimo": p.estoque_minimo or 0,
                "abaixo_minimo": True
            })
    return resultados
