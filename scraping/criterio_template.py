"""
Template de avaliação de critério da Cartilha PNTP 2025

Este arquivo deve ser usado como base para criar scrapers específicos por critério.
"""

def avaliar(html: str, soup, url: str) -> dict:
    """
    Avalia o critério da cartilha PNTP com base na página fornecida.

    Retorna um dicionário com os seguintes campos:
    - codigo: código do critério (ex: 3.2)
    - descricao: descrição textual do critério
    - fundamento: base legal ou regulamentar
    - classificacao: essencial / obrigatória / recomendada
    - aplicavel_a: Poder ou esfera (Executivo, Legislativo, etc.)

    - disponibilidade: bool
    - atualidade: bool
    - serie_historica: bool
    - gravacao: bool
    - filtro: bool

    - justificativa: texto explicando os resultados
    """

    resultado = {
        "codigo": "X.X",
        "descricao": "Descrição do critério",
        "fundamento": "Art. ..., Decreto ...",
        "classificacao": "essencial",
        "aplicavel_a": "Executivo",

        "disponibilidade": False,
        "atualidade": False,
        "serie_historica": False,
        "gravacao": False,
        "filtro": False,

        "justificativa": ""
    }

    # Inserir lógica de verificação aqui

    return resultado
