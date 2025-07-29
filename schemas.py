# -*- coding: utf-8 -*-

from pydantic import BaseModel
from typing import Union

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
    # Para criar um usuário, a senha é necessária
    password: str

class User(UserBase):
    # Para ler um usuário, não queremos expor a senha
    id: int
    disabled: bool

    class Config:
        # Antigo 'orm_mode = True', agora 'from_attributes = True' no Pydantic v2
        # Permite que o Pydantic leia os dados diretamente de um objeto ORM
        from_attributes = True
