from sqlalchemy import create_engine # eh usada pra criar conexao com bd
from sqlalchemy.orm import declarative_base, sessionmaker
# declarative_base -> criar a classe base para os modelos
# sessionmaker -> objeto pra gerenciar a comunicacao com bd

# definindo o arquivo do bd
# sqlite:// -> definicao do driver SQLite
DATABASE_URL = "sqlite:///./produtos.db" 

# definir o motor que conecta ao bd
engine = create_engine(DATABASE_URL, connect_args = {"check_same_thread": False})

#autoflush=False, impede que mudanças sejam automaticamente escritas no banco antes de um commit explícito
SessionLocal = sessionmaker(bind=engine, autoflush=False)
# criacao de os modelos de dados no BD
Base = declarative_base()