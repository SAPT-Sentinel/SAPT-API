import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import unicodedata

from .criterio_4_1 import avaliar as avaliar_4_1
from .criterio_4_2 import avaliar as avaliar_4_2
from .criterio_4_3 import avaliar as avaliar_4_3
from .criterio_4_4 import avaliar as avaliar_4_4
from .criterio_4_5 import avaliar as avaliar_4_5
from .criterio_4_6 import avaliar as avaliar_4_6

def normalizar(texto):
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('ASCII').lower()

def encontrar_link_por_texto(soup, palavras_chave):
    links = soup.find_all("a", href=True)
    for link in links:
        texto = " ".join(link.stripped_strings).strip()
        texto_normalizado = normalizar(texto)
        for chave in palavras_chave:
            if normalizar(chave) in texto_normalizado:
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

    # Critérios 4.1, 4.2, 4.3 (todos acessíveis por "despesa atual")
    link_despesa_atual = encontrar_link_por_texto(soup, ["despesa empenhada, liquidada e paga (atual)"])
    if link_despesa_atual:
        try:
            html_desp, soup_desp, url_desp = carregar_subpagina(url_base, link_despesa_atual)
        except:
            html_desp, soup_desp, url_desp = html, soup, url_base
    else:
        html_desp, soup_desp, url_desp = html, soup, url_base

    resultados.append(avaliar_4_1(html_desp, soup_desp, url_desp))
    resultados.append(avaliar_4_2(html_desp, soup_desp, url_desp))
    resultados.append(avaliar_4_3(html_desp, soup_desp, url_desp))

    # Critério 4.4 - aquisição de bens
    link_bens = encontrar_link_por_texto(soup, ["aquisição de bens", "despesas com bens"])
    if link_bens:
        try:
            html_bens, soup_bens, url_bens = carregar_subpagina(url_base, link_bens)
        except:
            html_bens, soup_bens, url_bens = html, soup, url_base
    else:
        html_bens, soup_bens, url_bens = html, soup, url_base

    resultados.append(avaliar_4_4(html_bens, soup_bens, url_bens))

    # Critério 4.5 - patrocínio
    link_patrocinio = encontrar_link_por_texto(soup, ["patrocínio"])
    if link_patrocinio:
        try:
            html_patro, soup_patro, url_patro = carregar_subpagina(url_base, link_patrocinio)
        except:
            html_patro, soup_patro, url_patro = html, soup, url_base
    else:
        html_patro, soup_patro, url_patro = html, soup, url_base

    resultados.append(avaliar_4_5(html_patro, soup_patro, url_patro))

    # Critério 4.6 - publicidade
    link_publi = encontrar_link_por_texto(soup, ["publicidade"])
    if link_publi:
        try:
            html_pub, soup_pub, url_pub = carregar_subpagina(url_base, link_publi)
        except:
            html_pub, soup_pub, url_pub = html, soup, url_base
    else:
        html_pub, soup_pub, url_pub = html, soup, url_base

    resultados.append(avaliar_4_6(html_pub, soup_pub, url_pub))

    return resultados
