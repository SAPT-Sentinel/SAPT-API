# -*- coding: utf-8 -*-

from sqlalchemy import Boolean, Column, Integer, String
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
