"""
Módulo de execução dos critérios do domínio 'institucionais' (2.1 a 2.9)

Este manager recebe o HTML e soup da página principal de acesso à informação
e tenta encontrar os links corretos para cada critério com base em palavras-chave.
Cada link é acessado individualmente e enviado para o avaliador correspondente.
"""

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

from .criterio_2_1 import avaliar as avaliar_2_1
from .criterio_2_2 import avaliar as avaliar_2_2
from .criterio_2_3 import avaliar as avaliar_2_3
from .criterio_2_4 import avaliar as avaliar_2_4
from .criterio_2_5 import avaliar as avaliar_2_5
from .criterio_2_6 import avaliar as avaliar_2_6
from .criterio_2_7 import avaliar as avaliar_2_7
from .criterio_2_8 import avaliar as avaliar_2_8
from .criterio_2_9 import avaliar as avaliar_2_9

def encontrar_link_por_palavra(soup, palavras):
    """Procura o primeiro link (href) cujo texto ou href contenha qualquer palavra-chave"""
    links = soup.find_all("a", href=True)
    for link in links:
        # Coleta todo o texto visível dentro do <a>, incluindo tags filhas como <p>, <span>
        texto_completo = " ".join(link.stripped_strings).lower()
        href = link['href'].lower()
        for palavra in palavras:
            if palavra in texto_completo or palavra in href:
                return link['href']
    return None

def carregar_subpagina(base_url, caminho):
    """Carrega o HTML e Soup de uma subpágina"""
    url_completa = urljoin(base_url, caminho)
    response = requests.get(url_completa, timeout=15)
    response.raise_for_status()
    html = response.text
    soup = BeautifulSoup(html, "html.parser")
    return html, soup, url_completa

def avaliar(html: str, soup: BeautifulSoup, url_base: str) -> list:
    resultados = []

    # Critérios 2.1 a 2.3 → página institucional
    link_inst = encontrar_link_por_palavra(soup, ["institucional"])
    if link_inst:
        html_inst, soup_inst, url_inst = carregar_subpagina(url_base, link_inst)
        resultados.append(avaliar_2_1(html_inst, soup_inst, url_inst))
        resultados.append(avaliar_2_2(html_inst, soup_inst, url_inst))
        resultados.append(avaliar_2_3(html_inst, soup_inst, url_inst))

    # Critério 2.4 → pode estar em qualquer página, aqui tentamos reutilizar institucional
    if link_inst:
        resultados.append(avaliar_2_4(html_inst, soup_inst, url_inst))

    # Critério 2.5 → pode estar no rodapé ou institucional também
    if link_inst:
        resultados.append(avaliar_2_5(html_inst, soup_inst, url_inst))

    # Critério 2.6 → normativos próprios
    link_norma = encontrar_link_por_palavra(soup, ["normativo", "atos"])
    if link_norma:
        html_norma, soup_norma, url_norma = carregar_subpagina(url_base, link_norma)
        resultados.append(avaliar_2_6(html_norma, soup_norma, url_norma))

    # Critério 2.7 → perguntas frequentes
    link_faq = encontrar_link_por_palavra(soup, ["pergunta", "faq"])
    if link_faq:
        html_faq, soup_faq, url_faq = carregar_subpagina(url_base, link_faq)
        resultados.append(avaliar_2_7(html_faq, soup_faq, url_faq))

    # Critério 2.8 → redes sociais no próprio soup da página principal
    resultados.append(avaliar_2_8(html, soup, url_base))

    # Critério 2.9 → link direto para o radar (verificado no HTML principal)
    resultados.append(avaliar_2_9(html, soup, url_base))

    return resultados
