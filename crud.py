# -*- coding: utf-8 -*-

from sqlalchemy.orm import Session
from typing import List, Dict, Any

import models
import schemas
import security

# --- Funções CRUD para Usuário ---
def get_user(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = security.get_password_hash(user.password)
    db_user = models.User(username=user.username, email=user.email, full_name=user.full_name, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# --- Funções CRUD para Análise e Critérios ---
def get_criterio_by_codigo(db: Session, codigo: str):
    return db.query(models.Criterio).filter(models.Criterio.codigo == codigo).first()

def create_criterio(db: Session, criterio: schemas.CriterioCreate):
    db_criterio = models.Criterio(**criterio.model_dump())
    db.add(db_criterio)
    db.commit()
    db.refresh(db_criterio)
    return db_criterio

def create_analise(db: Session, url: str, user_id: int):
    db_analise = models.Analise(url_avaliada=url, user_id=user_id)
    db.add(db_analise)
    db.commit()
    db.refresh(db_analise)
    return db_analise

def create_resultado_analise(db: Session, analise_id: int, criterio_id: int, resultado: Dict[str, Any]):
    db_resultado = models.ResultadoAnalise(analise_id=analise_id, criterio_id=criterio_id, passou=resultado.get("disponibilidade"), detalhes=resultado.get("justificativa"))
    db.add(db_resultado)
    db.commit()
    db.refresh(db_resultado)
    return db_resultado

def salvar_resultado_completo_analise(db: Session, resultado_json: Dict[str, Any], user: models.User):
    analise = create_analise(db, url=resultado_json["urlAvaliada"], user_id=user.id)
    for dominio, criterios in resultado_json["dominios"].items():
        for criterio_data in criterios:
            criterio_db = get_criterio_by_codigo(db, codigo=criterio_data["codigo"])
            if not criterio_db:
                criterio_schema = schemas.CriterioCreate(codigo=criterio_data["codigo"], nome_criterio=criterio_data["descricao"], dominio=dominio, descricao=criterio_data.get("fundamento", ""))
                criterio_db = create_criterio(db, criterio=criterio_schema)
            create_resultado_analise(db=db, analise_id=analise.id, criterio_id=criterio_db.id, resultado=criterio_data)
    return analise

def get_analises_by_user(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Analise).filter(models.Analise.user_id == user_id).order_by(models.Analise.data_analise.desc()).offset(skip).limit(limit).all()

def get_all_analises(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Analise).order_by(models.Analise.data_analise.desc()).offset(skip).limit(limit).all()

def get_analise_by_id(db: Session, analise_id: int):
    return db.query(models.Analise).filter(models.Analise.id == analise_id).first()

def get_resultado_by_id(db: Session, resultado_id: int):
    """Busca um único resultado de análise pelo seu ID."""
    return db.query(models.ResultadoAnalise).filter(models.ResultadoAnalise.id == resultado_id).first()

def update_resultado_analise(db: Session, resultado_id: int, resultado_update: schemas.ResultadoAnaliseUpdate):
    """Atualiza um resultado de análise existente."""
    db_resultado = get_resultado_by_id(db, resultado_id)
    if db_resultado:
        # Atualiza apenas os campos que foram enviados
        if resultado_update.passou is not None:
            db_resultado.passou = resultado_update.passou
        if resultado_update.detalhes is not None:
            db_resultado.detalhes = resultado_update.detalhes
        
        db.commit()
        db.refresh(db_resultado)
    return db_resultado


def update_analise(db: Session, analise_id: int, analise_update: schemas.AnaliseUpdate):
    """Atualiza uma análise existente (apenas a URL)."""
    db_analise = get_analise_by_id(db, analise_id)
    if db_analise:
        db_analise.url_avaliada = analise_update.url_avaliada
        db.commit()
        db.refresh(db_analise)
    return db_analise

def delete_analise(db: Session, analise_id: int):
    """Apaga uma análise e seus resultados associados."""
    db_analise = get_analise_by_id(db, analise_id)
    if db_analise:
        db.delete(db_analise)
        db.commit()
    return db_analise
