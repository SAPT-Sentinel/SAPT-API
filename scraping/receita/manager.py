import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import unicodedata

from .criterio_3_1 import avaliar as avaliar_3_1
from .criterio_3_2 import avaliar as avaliar_3_2
from .criterio_3_3 import avaliar as avaliar_3_3

def normalizar(texto):
    """Remove acentos e converte para minúsculas."""
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').lower()

def encontrar_link_por_texto(soup, palavras_chave):
    """
    Procura o href de um <a> cujo texto contenha qualquer uma das palavras-chave (normalizado).
    """
    links = soup.find_all("a", href=True)
    for link in links:
        texto = " ".join(link.stripped_strings).strip()
        texto_normalizado = normalizar(texto)
        for palavra in palavras_chave:
            if normalizar(palavra) in texto_normalizado:
                return link['href']
    return None

def carregar_subpagina(base_url, caminho):
    url_completa = urljoin(base_url, caminho)
    response = requests.get(url_completa, timeout=20)
    response.raise_for_status()
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return html, soup, url_completa

def avaliar(html: str, soup: BeautifulSoup, url_base: str) -> list:
    resultados = []

    # --- Critérios 3.1 e 3.2 ---
    termos_receita = ["receita prevista", "receita arrecadada", "receita atual", "orcamento receitas"]
    link_receita = encontrar_link_por_texto(soup, termos_receita)
    if link_receita:
        try:
            html_rec, soup_rec, url_rec = carregar_subpagina(url_base, link_receita)
        except:
            html_rec, soup_rec, url_rec = html, soup, url_base
    else:
        html_rec, soup_rec, url_rec = html, soup, url_base

    resultados.append(avaliar_3_1(html_rec, soup_rec, url_rec))
    resultados.append(avaliar_3_2(html_rec, soup_rec, url_rec))

    # --- Critério 3.3 (Dívida Ativa) ---
    termos_divida = ["divida ativa", "dívida ativa", "inscritos em dívida"]
    link_divida = encontrar_link_por_texto(soup, termos_divida)
    if link_divida:
        try:
            html_div, soup_div, url_div = carregar_subpagina(url_base, link_divida)
        except:
            html_div, soup_div, url_div = html, soup, url_base
    else:
        html_div, soup_div, url_div = html, soup, url_base

    resultados.append(avaliar_3_3(html_div, soup_div, url_div))

    return resultados
