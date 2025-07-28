"""
loader.py

Módulo responsável por carregar o HTML de um portal a partir de sua URL
e repassar o conteúdo para o manager da categoria correspondente (ex: 'inicial').

Requisitos: requests, beautifulsoup4

Exemplo de uso:
    python -m scraping.loader https://www.exemplo.gov.br
"""

import sys
import os
from pathlib import Path
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import requests
from scraping.utils.persist import salvar_em_json

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
        print(f"[ERRO] Não foi possível carregar a URL: {e}")
        sys.exit(1)

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

def main():
    # Verifica se URL foi passada por argumento, senão solicita
    if len(sys.argv) > 1:
        url = sys.argv[1]
    else:
        url = input("Digite a URL do portal a ser avaliado: ").strip()

    html, soup = carregar_html(url)
    dominios = listar_dominios()

    if not dominios:
        print("[!] Nenhum domínio com manager.py encontrado.")
        return

    print(f"\n🔍 Avaliando: {url}")
    print(f"📁 Domínios detectados: {dominios}")

    for dominio in dominios:
        print(f"\n▶ Avaliando domínio: {dominio}")
        manager = importar_manager(dominio)
        if manager and hasattr(manager, 'avaliar'):
            resultados = manager.avaliar(html, soup, url)
            salvar_em_json(resultados, url, dominio)
        else:
            print(f"[!] Manager de '{dominio}' não possui função avaliar().")

if __name__ == "__main__":
    main()
