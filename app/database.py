import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase  # Mudança aqui
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do .env
load_dotenv()

# Pega a URL do banco do .env ou usa o sqlite local por padrão
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./test.db")

# Cria o motor do banco de dados
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}  # Necessário apenas para SQLite
)

# Configura a sessão
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# NOVO PADRÃO: Substitui o antigo declarative_base() para evitar Warnings
class Base(DeclarativeBase):
    pass

# Dependência para obter a sessão do banco nas rotas
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()