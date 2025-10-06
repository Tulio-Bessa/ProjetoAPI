from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from models import ProdutoCreate,CategoriaCreate, CategoriaOut, ProdutoOut   
from schemas import Produto, Categoria
from database import SessionLocal, engine, Base

Base.metadata.create_all(bind=engine)
app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get ("/produtos")
def listar_produtos (db : Session = Depends(get_db)):
    return db.query(Produto).all()

@app.get("/produtos/{prod_id}", response_model=dict)
def listar_id(prod_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == prod_id).first()
    if not produto:
        return {"erro": "produto nao encontrado"}
    return {
        "id": produto.id,
        "nome": produto.nome,
        "preco": produto.preco
    }

@app.post("/produtos", status_code=201)
def criar(prod: ProdutoCreate, db: Session = Depends(get_db)):
    novo_prod = Produto(nome=prod.nome, preco=prod.preco,categoria_id=prod.categoria_id )
    db.add(novo_prod)
    db.commit()
    db.refresh(novo_prod)
    return novo_prod

@app.delete("/produtos/{prod_id}", status_code=200)
def excluir(prod_id: int, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == prod_id).first()
    if not produto:
        return {"erro": "produto nao encontrado"}
    db.delete(produto)
    db.commit()
    return {"mensagem": f"Produto com id {id} excluido"}


@app.post("/categorias", status_code=201)
def criar_categoria(cat: CategoriaCreate, db: Session = Depends(get_db)):
    nova_cat = Categoria(nome=cat.nome)
    db.add(nova_cat)
    db.commit()
    db.refresh(nova_cat)
    return nova_cat

@app.get ("/categorias")
def listar_categorias (db : Session = Depends(get_db)):
    return db.query(Categoria).all()

@app.get("/categorias/{cat_id}", response_model=dict)
def listar_id(cat_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == cat_id).first()
    if not categoria:
        return {"erro": "Categoria nao encontrado"}
    return {
        "id": categoria.id,
        "nome": categoria.nome
    }

@app.delete("/categorias/{cat_id}", status_code=200)
def excluir_categorias(cat_id: int, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == cat_id).first()
    if not categoria:
        return {"erro": "categoria nao encontrado"}
    db.delete(categoria)
    db.commit()
    return {"mensagem": f"Categoria com id {id} excluido"}

@app.put("/categorias/{cat_id}", status_code=200)
def atualizar_categoria(cat_id: int, cat: CategoriaCreate, db: Session = Depends(get_db)):
    categoria = db.query(Categoria).filter(Categoria.id == cat_id).first()
    if not categoria:
        return {"erro": "categoria nao encontrado"}
    categoria.nome = cat.nome
    db.commit()
    db.refresh(categoria)
    return categoria


@app.put("/produtos/{prod_id}", status_code=200)
def atualizar_produto(prod_id: int, prod: ProdutoCreate, db: Session = Depends(get_db)):
    produto = db.query(Produto).filter(Produto.id == prod_id).first()
    if not produto:
        return {"erro": "produto nao encontrado"}
    produto.nome = prod.nome
    produto.preco = prod.preco
    produto.categoria_id = prod.categoria_id
    db.commit()
    db.refresh(produto)
    return produto


@app.get("/produtos/categoria/{categoria_id}", status_code=200)
def listar_produtos_por_categoria(categoria_id: int, db: Session = Depends(get_db)):
    produtos = db.query(Produto).filter(Produto.categoria_id == categoria_id).all()
    return produtos