# scraper.py

import sys
from pathlib import Path
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

# Adiciona a raiz do projeto ao sys.path
sys.path.append(str(Path(__file__).resolve().parent.parent))

def carregar_html(url):
    """Faz download do HTML da página e retorna o HTML bruto e o objeto BeautifulSoup."""
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        return html, soup
    except Exception as e:
        raise RuntimeError(f"[ERRO] Não foi possível carregar a URL: {e}")

def listar_dominios():
    """Lista os diretórios de domínio que contêm um manager.py"""
    base_dir = Path(__file__).parent
    dominios = []
    for item in base_dir.iterdir():
        if item.is_dir() and (item / 'manager.py').exists():
            dominios.append(item.name)
    return dominios

def importar_manager(dominio_nome):
    """Importa dinamicamente o módulo manager de um domínio"""
    try:
        return __import__(f"scraping.{dominio_nome}.manager", fromlist=['avaliar'])
    except ImportError as e:
        print(f"[ERRO] Não foi possível importar o manager de {dominio_nome}: {e}")
        return None

def executar_scraping(url: str) -> dict:
    """Executa o scraping para todos os domínios encontrados."""
    html, soup = carregar_html(url)
    dominios = listar_dominios()

    resultado_final = {"urlAvaliada": url, "dominios": {}}

    for dominio in dominios:
        manager = importar_manager(dominio)
        if manager and hasattr(manager, 'avaliar'):
            try:
                resultados = manager.avaliar(html, soup, url)
                resultado_final["dominios"][dominio] = resultados
            except Exception as e:
                print(f"[ERRO] ao avaliar domínio '{dominio}': {e}")
        else:
            print(f"[AVISO] Manager de '{dominio}' não possui função avaliar().")

    return resultado_final
