# -*- coding: utf-8 -*-

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Pega as credenciais do banco de dados do ambiente
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Monta a URL de conexão para o MySQL usando o driver PyMySQL
SQLALCHEMY_DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Cria o "motor" do SQLAlchemy, que gerencia a conexão com o banco
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Cria uma fábrica de sessões. Cada instância de SessionLocal será uma nova sessão no banco.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Cria uma classe Base que nossos modelos de ORM (tabelas) irão herdar
Base = declarative_base()

# --- Dependência para os Endpoints ---
def get_db():
    """
    Esta função é uma dependência do FastAPI que cria e fornece uma sessão de banco de dados
    para cada requisição e garante que ela seja fechada ao final.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
