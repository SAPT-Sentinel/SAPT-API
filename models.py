# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, Integer, String, Float, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class User(Base):
    """
    Modelo SQLAlchemy que representa a tabela 'users' no banco de dados.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    full_name = Column(String(100), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    disabled = Column(Boolean, default=False)

    # Relacionamento: Um usuário pode ter várias análises
    analises = relationship("Analise", back_populates="usuario")


class Analise(Base):
    """
    Modelo para a tabela 'analises'. Guarda a informação geral de uma análise.
    """
    __tablename__ = "analises"

    id = Column(Integer, primary_key=True, index=True)
    url_avaliada = Column(String(512), nullable=False)
    data_analise = Column(DateTime, default=datetime.utcnow)
    
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relacionamento com User e ResultadoAnalise
    usuario = relationship("User", back_populates="analises")
    resultados = relationship("ResultadoAnalise", back_populates="analise", cascade="all, delete-orphan")


class Criterio(Base):
    """
    Modelo para a tabela 'criterios'. Catálogo central de todos os critérios.
    """
    __tablename__ = "criterios"

    id = Column(Integer, primary_key=True, index=True)
    # Usamos o código do critério como identificador único de negócio
    codigo = Column(String(50), unique=True, index=True, nullable=False)
    nome_criterio = Column(String(255), nullable=False)
    dominio = Column(String(100), index=True)
    descricao = Column(Text, nullable=True)

    # Relacionamento com ResultadoAnalise
    resultados = relationship("ResultadoAnalise", back_populates="criterio")


class ResultadoAnalise(Base):
    """
    Modelo para a tabela 'resultados_analise'. Conecta uma Análise a um Critério
    e armazena o resultado da avaliação.
    """
    __tablename__ = "resultados_analise"

    id = Column(Integer, primary_key=True, index=True)
    passou = Column(Boolean, nullable=True) # Usamos nullable para casos onde não se aplica
    detalhes = Column(Text, nullable=True)
    pontuacao = Column(Float, nullable=True)

    analise_id = Column(Integer, ForeignKey("analises.id"))
    criterio_id = Column(Integer, ForeignKey("criterios.id"))

    # Relacionamento com Analise e Criterio
    analise = relationship("Analise", back_populates="resultados")
    criterio = relationship("Criterio", back_populates="resultados")
