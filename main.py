# -*- coding: utf-8 -*-

from dotenv import load_dotenv
load_dotenv()

import sys
from pathlib import Path
from typing import Dict, Any, List
from datetime import timedelta

from fastapi import FastAPI, HTTPException, Depends, status, Query, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# --- 1. CONFIGURAÇÃO INICIAL E IMPORTS ---
sys.path.append(str(Path(__file__).parent))

import crud
import models
import schemas
from schemas import LoginRequest
from schemas import AnaliseRequest
import security
from database import engine, get_db

from scraping import scraper
import requests
from bs4 import BeautifulSoup
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

# --- 2. INSTÂNCIA DA API ---
app = FastAPI(
    title="SAPT - API de Análise de Transparência (com CRUD completo)",
    description="Uma API que executa, armazena, edita e apaga análises de transparência, com autenticação de usuário e histórico de resultados.",
    version="4.4.0"
)

# --- 3. LÓGICA DE NEGÓCIO (SCRAPING) ---
def executar_analise_completa(url: str) -> Dict[str, Any]:
    try:
        return scraper.executar_scraping(url)
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Falha ao carregar a URL: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro durante a execução da análise: {e}")

# --- 4. ENDPOINTS DA API ---

@app.post("/login", response_model=schemas.Token)
async def login_for_access_token(
    login_data: LoginRequest = Body(...),
    db: Session = Depends(get_db)
):
    user = crud.get_user(db, username=login_data.username)
    if not user or not security.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"}
        )
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Nome de usuário já registrado")
    return crud.create_user(db=db, user=user)

# --- ENDPOINTS DE ANÁLISE (CRUD COMPLETO) ---

@app.post("/api/analise", response_model=schemas.Analise)
async def analisar_e_salvar_portal(
    analise_request: AnaliseRequest,
    current_user: models.User = Depends(security.get_current_active_user),
    db: Session = Depends(get_db)
):
    try:
        resultado_json = executar_analise_completa(analise_request.url)
        analise_salva = crud.salvar_resultado_completo_analise(db=db, resultado_json=resultado_json, user=current_user)
        return analise_salva
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro interno inesperado: {e}")

@app.get("/api/analises/", response_model=List[schemas.Analise])
def ler_historico_de_analises(
    skip: int = 0, 
    limit: int = 100, 
    current_user: models.User = Depends(security.get_current_active_user),
    db: Session = Depends(get_db),
):
    """Retorna uma lista com o histórico de TODAS as análises realizadas no sistema."""
    analises = crud.get_all_analises(db, skip=skip, limit=limit)
    return analises

@app.get("/api/analises/{analise_id}", response_model=schemas.Analise)
def ler_analise_especifica(
    analise_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    """Retorna os detalhes de uma análise específica pelo seu ID."""
    db_analise = crud.get_analise_by_id(db, analise_id=analise_id)
    if db_analise is None:
        raise HTTPException(status_code=404, detail="Análise não encontrada")
    return db_analise

@app.put("/api/analises/{analise_id}", response_model=schemas.Analise)
def editar_analise(
    analise_id: int,
    analise_update: schemas.AnaliseUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    """Atualiza a URL de uma análise existente."""
    db_analise = crud.update_analise(db, analise_id=analise_id, analise_update=analise_update)
    if db_analise is None:
        raise HTTPException(status_code=404, detail="Análise não encontrada")
    return db_analise

@app.put("/api/resultados/{resultado_id}", response_model=schemas.ResultadoAnalise)
def editar_resultado_analise(
    resultado_id: int,
    resultado_update: schemas.ResultadoAnaliseUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    """
    Atualiza um resultado de análise específico (ex: muda se passou ou os detalhes).
    """
    db_resultado = crud.update_resultado_analise(db, resultado_id=resultado_id, resultado_update=resultado_update)
    if db_resultado is None:
        raise HTTPException(status_code=404, detail="Resultado da análise não encontrado")
    return db_resultado

@app.delete("/api/analises/{analise_id}", response_model=dict)
def apagar_analise(
    analise_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(security.get_current_active_user)
):
    """Apaga uma análise e todos os seus resultados associados do banco de dados."""
    db_analise = crud.delete_analise(db, analise_id=analise_id)
    if db_analise is None:
        raise HTTPException(status_code=404, detail="Análise não encontrada")
    return {"detail": "Análise apagada com sucesso"}

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:5173",  # seu frontend local
    "https://sapt-api.onrender.com",  # opcionalmente, o próprio domínio da API
    "https://sapt-ui-gap5.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # ou use ["*"] para permitir qualquer origem (menos seguro)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
