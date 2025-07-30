"""
Critério 2.1 - Divulga a sua estrutura organizacional?
➢ Fundamentação: Art. 8º, §3º, I, da Lei nº 12.527/2011 – LAI.
➢ Classificação: Obrigatória.
➢ Aplicável a: Executivo, Legislativo, Judiciário, Tribunal de Contas, Ministério Público,
  Defensoria, Consórcios Públicos, Estatais Dependentes e Independentes.

Disponibilidade:
Deve haver no site a apresentação da estrutura organizacional do órgão ou poder, de forma textual ou gráfica, deixando clara a hierarquia entre as unidades.
"""

from bs4 import BeautifulSoup

def avaliar(html: str, soup: BeautifulSoup, url: str) -> dict:
    resultado = {
        "codigo": "2.1",
        "descricao": "Divulga a sua estrutura organizacional?",
        "fundamento": "Art. 8º, §3º, I, da Lei nº 12.527/2011",
        "classificacao": "obrigatória",
        "aplicavel_a": "Todos",
        "disponibilidade": False,
        "atualidade": None,
        "serie_historica": None,
        "gravacao": None,
        "filtro": None,
        "justificativa": "Não foram localizados elementos visuais ou textuais claros da estrutura organizacional."
    }

    # Busca por palavras-chave em qualquer parte visível do HTML
    palavras_chave = [
        "estrutura organizacional", "organograma", "estrutura administrativa",
        "secretarias", "departamentos", "chefia", "gabinete", "coordenação"
    ]

    texto_visivel = soup.get_text(separator=" ", strip=True).lower()

    for palavra in palavras_chave:
        if palavra in texto_visivel:
            resultado["disponibilidade"] = True
            resultado["justificativa"] = f"Palavra-chave encontrada na página: '{palavra}'"
            break

    return resultado
