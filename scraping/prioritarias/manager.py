"""
Módulo de execução dos critérios do grupo 'Inicial' (1.1 a 1.4)

Este módulo importa os avaliadores de cada critério e executa todos sequencialmente,
dado o HTML e o objeto BeautifulSoup da página analisada.
"""

from .criterio_1_1 import avaliar as avaliar_1_1
from .criterio_1_2 import avaliar as avaliar_1_2
from .criterio_1_3 import avaliar as avaliar_1_3
from .criterio_1_4 import avaliar as avaliar_1_4

def avaliar(html, soup, url):
    """Executa a avaliação de todos os critérios definidos para o domínio 'inicial'"""
    resultados = []

    resultados.append(avaliar_1_1(html, soup, url))
    resultados.append(avaliar_1_2(html, soup, url))
    resultados.append(avaliar_1_3(html, soup, url))
    resultados.append(avaliar_1_4(html, soup, url))

    return resultados
