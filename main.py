# -*- coding: utf-8 -*-

# A CORREÇÃO COMEÇA AQUI: Carregar o .env no início de tudo
from dotenv import load_dotenv
load_dotenv()
# FIM DA CORREÇÃO

import sys
from pathlib import Path
from typing import Dict, Any
from datetime import timedelta

from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# --- 1. CONFIGURAÇÃO INICIAL E IMPORTS ---
sys.path.append(str(Path(__file__).parent))

import crud
import models
import schemas
import security
from database import engine, get_db

from scraping.inicial import manager as inicial_manager
import requests
from bs4 import BeautifulSoup

models.Base.metadata.create_all(bind=engine)

# --- 2. INSTÂNCIA DA API ---
app = FastAPI(
    title="SAPT - API de Análise de Transparência (com MySQL)",
    description="Uma API que executa scripts de web scraping e é protegida por autenticação de usuário via token JWT, com persistência em banco de dados MySQL.",
    version="3.2.0"
)

# --- 3. LÓGICA DE NEGÓCIO (SCRAPING) ---
# (Esta parte não muda)
def carregar_html(url: str):
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        return html, soup
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=f"Falha ao carregar a URL: {e}")

def executar_analise_completa(url: str) -> Dict[str, Any]:
    html, soup = carregar_html(url)
    resultado_final = {"urlAvaliada": url, "dominios": {}}
    try:
        resultados_inicial = inicial_manager.avaliar(html, soup, url)
        resultado_final["dominios"]["inicial"] = resultados_inicial
    except Exception as e:
        print(f"Erro ao processar o domínio 'inicial': {e}")
        resultado_final["dominios"]["inicial"] = {"erro": f"Falha ao processar o domínio: {e}"}
    return resultado_final

# --- 4. ENDPOINTS DA API ---

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    db: Session = Depends(get_db), 
    form_data: OAuth2PasswordRequestForm = Depends()
):
    user = crud.get_user(db, username=form_data.username)
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=security.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(
    user: schemas.UserCreate, 
    db: Session = Depends(get_db),
    current_user: schemas.User = Depends(security.get_current_active_user) 
):
    db_user = crud.get_user(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Nome de usuário já registrado")
    return crud.create_user(db=db, user=user)


@app.get("/api/analise")
async def analisar_portal(
    url: str = Query(..., min_length=15, description="A URL completa do portal a ser analisado."),
    current_user: schemas.User = Depends(security.get_current_active_user)
):
    try:
        resultado = executar_analise_completa(url)
        return resultado
    except Exception as e:
        print(f"Erro inesperado no servidor: {e}")
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro interno inesperado: {e}")
