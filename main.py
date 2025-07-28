# main.py
# -*- coding: utf-8 -*-

import sys
from pathlib import Path
from typing import Dict, Any

from fastapi import FastAPI, HTTPException, Query
import requests
from bs4 import BeautifulSoup

# Adiciona a pasta 'scraping' ao path do Python para que possamos importar de lá
sys.path.append(str(Path(__file__).parent))

# Importa o 'manager' do nosso módulo de scraping
from scraping.inicial import manager as inicial_manager

# --- Configuração da API ---
app = FastAPI(
    title="SAPT - API de Análise de Transparência",
    description="Uma API que executa scripts de web scraping para avaliar portais da transparência.",
    version="1.0.0"
)

def carregar_html(url: str):
    """Faz download do HTML e retorna o HTML bruto e o objeto BeautifulSoup."""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status() # Lança um erro para status HTTP 4xx ou 5xx
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        return html, soup
    except requests.RequestException as e:
        # Trata erros de rede (DNS, conexão, timeout, etc.)
        raise HTTPException(status_code=400, detail=f"Falha ao carregar a URL: {e}")

def executar_analise_completa(url: str) -> Dict[str, Any]:
    """Orquestra a análise completa, chamando os managers de cada domínio e retornando um dicionário."""
    html, soup = carregar_html(url)
    
    resultado_final = {"urlAvaliada": url, "dominios": {}}

    # Executa o domínio 'inicial'
    try:
        resultados_inicial = inicial_manager.avaliar(html, soup, url)
        resultado_final["dominios"]["inicial"] = resultados_inicial
    except Exception as e:
        # Em uma API real, um log mais detalhado seria registrado aqui
        print(f"Erro ao processar o domínio 'inicial': {e}")
        # Informa no próprio JSON que houve um erro neste domínio
        resultado_final["dominios"]["inicial"] = {"erro": f"Falha ao processar o domínio: {e}"}

    # Se você tivesse outros domínios, chamaria os managers deles aqui...

    return resultado_final

# --- Endpoint da API (A URL que o usuário irá acessar) ---

@app.get("/api/analise", response_model=Dict[str, Any])
async def analisar_portal(url: str = Query(..., min_length=15, description="A URL completa do portal a ser analisado.")):
    """
    Recebe uma URL, executa a suíte de scripts de análise de transparência
    e retorna um relatório completo em formato JSON.
    """
    if not url.startswith("http"):
        raise HTTPException(status_code=400, detail="URL inválida. Deve começar com http:// ou https://")

    try:
        resultado = executar_analise_completa(url)
        # O FastAPI converte o dicionário em uma resposta JSON automaticamente
        return resultado
    except HTTPException as http_exc:
        # Repassa exceções HTTP que já tratamos (como em carregar_html)
        raise http_exc
    except Exception as e:
        # Captura qualquer outro erro inesperado e retorna um erro 500 (Erro Interno do Servidor)
        print(f"Erro inesperado no servidor: {e}") # Logar o erro
        raise HTTPException(status_code=500, detail=f"Ocorreu um erro interno inesperado: {e}")