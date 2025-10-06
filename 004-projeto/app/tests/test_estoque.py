import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.db.base import Base
from app.models.produto import Produto
from app.models.estoque import EstoqueMovimento, TipoMovimento
from app.repositories import estoque as repo
from app.core import config

@pytest.fixture
def session():
    # in-memory SQLite for tests
    engine = create_engine('sqlite:///:memory:', connect_args={'check_same_thread': False})
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    db = Session()
    yield db
    db.close()

def test_entrada_saida_saldo(session):
    # create product
    p = Produto(nome='Teste', preco=1.0, categoria_id=1, estoque_minimo=5, ativo=True)
    session.add(p)
    session.commit()
    session.refresh(p)

    # entrada 10
    class P: pass
    pay = P(); pay.produto_id = p.id; pay.tipo = TipoMovimento.ENTRADA; pay.quantidade = 10; pay.motivo = 'teste'
    repo.create_movimento(session, pay)

    # saida 3 via venda
    with pytest.raises(Exception) as e_info:
        # temporarily allow negative to be False but enough stock exists so no raise
        pass
    mov = repo.create_venda(session, p.id, 3)
    saldo = repo.get_saldo(session, p.id)
    assert saldo == 7

def test_bloqueio_saida(session):
    # create product with zero stock
    p = Produto(nome='Produto2', preco=2.0, categoria_id=1, estoque_minimo=1, ativo=True)
    session.add(p); session.commit(); session.refresh(p)
    # ensure negative not allowed
    config.settings.ALLOW_NEGATIVE_STOCK = False
    with pytest.raises(Exception):
        repo.create_venda(session, p.id, 1)

    # allow negative and try again
    config.settings.ALLOW_NEGATIVE_STOCK = True
    mov = repo.create_venda(session, p.id, 1)
    assert mov.tipo == TipoMovimento.SAIDA

def test_ajuste_motivo_obrigatorio(session):
    p = Produto(nome='Produto3', preco=3.0, categoria_id=1, estoque_minimo=0, ativo=True)
    session.add(p); session.commit(); session.refresh(p)
    with pytest.raises(Exception):
        repo.create_ajuste(session, p.id, TipoMovimento.ENTRADA, 5, '')

def test_extrato_resumo_abaixo(session):
    p = Produto(nome='Produto4', preco=4.0, categoria_id=1, estoque_minimo=10, ativo=True)
    session.add(p); session.commit(); session.refresh(p)
    # create entrada 3 (below minimum)
    class P: pass
    pay = P(); pay.produto_id = p.id; pay.tipo = TipoMovimento.ENTRADA; pay.quantidade = 3; pay.motivo = 'in'
    repo.create_movimento(session, pay)
    resumo = repo.get_resumo(session)
    assert any(r['produto_id']==p.id and r['abaixo_minimo'] for r in resumo)
    abaixo = repo.get_produtos_abaixo_minimo(session)
    assert any(r['produto_id']==p.id for r in abaixo)
