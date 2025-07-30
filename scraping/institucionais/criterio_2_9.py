"""
Critério 2.9 – Inclui botão do Radar da Transparência Pública no site institucional ou portal transparência?
➢ Fundamentação: Art. 37 da CF (princípio da publicidade) e art. 3º da Lei nº 12.527/2011 – LAI.
➢ Classificação: Recomendada.
➢ Aplicável a: Executivo, Legislativo, Judiciário, Tribunal de Contas,
   Ministério Público, Defensoria, Consórcios Públicos e Estatais Dependentes e Independentes.

Requisitos:
- O site institucional ou portal de transparência deve apresentar um botão, banner ou link
  com o texto “Radar da Transparência Pública”, apontando para https://radardatransparencia.atricon.org.br.
- O link deve estar em local de fácil acesso, visível no primeiro nível da navegação.
"""

from bs4 import BeautifulSoup

def avaliar(html: str, soup: BeautifulSoup, url: str) -> dict:
    resultado = {
        "codigo": "2.9",
        "descricao": "Inclui botão do Radar da Transparência Pública no site institucional ou portal transparência?",
        "fundamento": "Art. 37 da CF e art. 3º da Lei nº 12.527/2011",
        "classificacao": "recomendada",
        "aplicavel_a": "Todos",
        "disponibilidade": False,
        "atualidade": None,
        "serie_historica": None,
        "gravacao": None,
        "filtro": None,
        "justificativa": "Nenhum link para o Radar da Transparência Pública foi encontrado na página."
    }

    links = soup.find_all("a", href=True)
    for link in links:
        href = link['href'].lower()
        if "radardatransparencia.atricon.org.br" in href:
            resultado["disponibilidade"] = True
            resultado["justificativa"] = f"Link encontrado: {href}"
            break

    return resultado
