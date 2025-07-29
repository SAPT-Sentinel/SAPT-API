# main.py
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path
from typing import Dict, Any, Union
from datetime import datetime, timedelta, timezone

from fastapi import FastAPI, HTTPException, Depends, status, Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from dotenv import load_dotenv

# --- 1. CONFIGURAÇÃO INICIAL E CARREGAMENTO DE SEGREDOS ---
# Carrega as variáveis do arquivo .env para o ambiente do sistema
load_dotenv()

# Adiciona a pasta 'scraping' ao path do Python para que os imports funcionem
sys.path.append(str(Path(__file__).parent))

# Importa a lógica de scraping que já tínhamos
from scraping.inicial import manager as inicial_manager
import requests
from bs4 import BeautifulSoup

# Pega as configurações de segurança do ambiente (arquivo .env)
SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# --- 2. CONFIGURAÇÃO DA API E UTILITÁRIOS DE SEGURANÇA ---
app = FastAPI(
    title="SAPT - API de Análise de Transparência (Segura com JWT)",
    description="Uma API que executa scripts de web scraping e é protegida por autenticação de usuário via token JWT.",
    version="2.0.0"
)

# Contexto para criptografar e verificar senhas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Esquema de autenticação que o FastAPI usará para a documentação e validação
# 'tokenUrl="token"' diz que o endpoint para obter o token se chama '/token'
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# --- 3. MODELOS DE DADOS E BANCO DE DADOS FALSO ---
# Modelos Pydantic para validação de dados do usuário
class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class UserInDB(User):
    hashed_password: str

# Em um projeto real, esta informação viria de um banco de dados (PostgreSQL, MySQL, etc.)
# Para este exemplo, usamos um dicionário em memória.
fake_users_db = {
    "sapt_user": {
        "username": "sapt_user",
        "full_name": "Usuário SAPT",
        "email": "user@sapt.com",
        "hashed_password": pwd_context.hash("sapt_password123"), # Senha 'sapt_password123' criptografada
        "disabled": False,
    }
}

# Funções para interagir com nosso "banco de dados"
def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# --- 4. FUNÇÕES PARA GERENCIAR O TOKEN JWT ---
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Cria um novo token de acesso."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        # Se não for passado um tempo de expiração, usa 15 minutos como padrão
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_active_user(token: str = Depends(oauth2_scheme)):
    """
    Dependência de segurança: decodifica o token, valida e retorna o usuário.
    Esta função será o "guarda-costas" dos nossos endpoints.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        # Decodifica o token JWT
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub") # 'sub' é o nome padrão para o "sujeito" do token
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    # Busca o usuário no nosso "banco de dados"
    user = get_user(fake_users_db, username=username)
    if user is None or user.disabled:
        raise credentials_exception
    return user


# --- 5. LÓGICA DE NEGÓCIO (SCRAPING) ---
# Esta parte permanece exatamente como antes.
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


# --- 6. ENDPOINTS DA API ---

@app.post("/token")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint de login. O cliente envia 'username' e 'password' e, se forem válidos,
    recebe um token de acesso.
    """
    user = get_user(fake_users_db, form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Nome de usuário ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/api/analise")
async def analisar_portal(
    url: str = Query(..., min_length=15, description="A URL completa do portal a ser analisado."),
    current_user: User = Depends(get_current_active_user)
):
    """
    Endpoint protegido que executa a análise de transparência.
    Requer um token JWT válido no cabeçalho de autorização.
    """
    # Se o código chegou até aqui, significa que o 'get_current_active_user' validou o token com sucesso.
    try:
        resultado = executar_analise_completa(url)
        return resultado
    except Exception as e:
        print(f"Erro inesperado no servidor: {e}")
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro interno inesperado: {e}")