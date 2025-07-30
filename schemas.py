# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Union, List, Optional
from datetime import datetime

# --- Schemas para o Token JWT ---
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None

# --- Schemas para o Usuário ---
class UserBase(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    disabled: bool

    class Config:
        from_attributes = True

class LoginRequest(BaseModel):
    username: str
    password: str

# --- Schemas para Critério ---
class CriterioBase(BaseModel):
    codigo: str
    nome_criterio: str
    dominio: str
    descricao: Optional[str] = None

class CriterioCreate(CriterioBase):
    pass

class Criterio(CriterioBase):
    id: int

    class Config:
        from_attributes = True

# --- Schemas para Resultado da Análise ---
class AnaliseRequest(BaseModel):
    url: str
    
class ResultadoAnaliseBase(BaseModel):
    passou: Optional[bool] = None
    detalhes: Optional[str] = None
    pontuacao: Optional[float] = None

# --- NOVO SCHEMA ADICIONADO ---
class ResultadoAnaliseUpdate(BaseModel):
    # Usamos Optional para que o utilizador possa atualizar
    # apenas um campo se quiser.
    passou: Optional[bool] = None
    detalhes: Optional[str] = None

class ResultadoAnaliseCreate(ResultadoAnaliseBase):
    pass

class ResultadoAnalise(ResultadoAnaliseBase):
    id: int
    criterio: Criterio

    class Config:
        from_attributes = True

class ResultadoAnaliseCreate(ResultadoAnaliseBase):
    pass

class ResultadoAnalise(ResultadoAnaliseBase):
    id: int
    criterio: Criterio

    class Config:
        from_attributes = True

# --- Schemas para Análise (Histórico) ---
class AnaliseBase(BaseModel):
    url_avaliada: str

class AnaliseCreate(AnaliseBase):
    pass

# --- NOVO SCHEMA ADICIONADO ---
class AnaliseUpdate(BaseModel):
    # Define quais campos podem ser atualizados.
    # Neste caso, apenas a URL.
    url_avaliada: str

class Analise(AnaliseBase):
    id: int
    data_analise: datetime
    resultados: List[ResultadoAnalise] = []

    class Config:
        from_attributes = True
