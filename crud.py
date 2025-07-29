# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session

# A CORREÇÃO ESTÁ AQUI:
import models
import schemas
import security
# FIM DA CORREÇÃO

def get_user(db: Session, username: str):
    """
    Busca um único usuário pelo seu nome de usuário.
    """
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    """
    Cria um novo usuário no banco de dados.
    A senha em texto plano é convertida para um hash antes de ser salva.
    """
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
