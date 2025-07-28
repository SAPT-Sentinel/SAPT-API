"""
persist.py

Módulo utilitário para salvar os resultados de avaliação em disco.
Atualmente suporta exportação em formato JSON.

Uso:
    from utils.persist import salvar_em_json
    salvar_em_json(resultados, url, grupo)
"""

import os
import json
from datetime import datetime
from urllib.parse import urlparse

def normalizar_url_para_nome(url: str) -> str:
    """Transforma a URL em um nome de arquivo válido."""
    dominio = urlparse(url).netloc.replace('.', '_')
    return dominio

def salvar_em_json(resultados: list, url: str, grupo: str, pasta_base="avaliacoes"):
    """
    Salva os resultados da avaliação em arquivo .json.

    Parâmetros:
        resultados: lista de dicionários de avaliação
        url: URL avaliada
        grupo: nome do grupo de critérios (ex: 'inicial')
        pasta_base: pasta onde os arquivos serão salvos
    """
    data_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    dominio = normalizar_url_para_nome(url)

    pasta_destino = os.path.join(pasta_base, grupo)
    os.makedirs(pasta_destino, exist_ok=True)

    nome_arquivo = f"{data_str}__{dominio}.json"
    caminho_arquivo = os.path.join(pasta_destino, nome_arquivo)

    with open(caminho_arquivo, "w", encoding="utf-8") as f:
        json.dump(resultados, f, ensure_ascii=False, indent=2)

    print(f"[✔] Resultados salvos em: {caminho_arquivo}")
