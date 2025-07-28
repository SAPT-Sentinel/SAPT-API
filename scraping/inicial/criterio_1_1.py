"""
Critério 1.1 - Possui sítio oficial próprio na internet?
Fundamentação: Art. 8º, §1º, I, da Lei 12.527/2011
Classificação: Essencial
Aplicável a: Todos os Poderes e Entes

Este critério considera atendido se a URL analisada for válida, pública e possuir domínio próprio
ligado à administração pública (ex: .gov.br).
"""

from urllib.parse import urlparse

def avaliar(html: str, soup, url: str) -> dict:
    resultado = {
        "codigo": "1.1",
        "descricao": "Possui sítio oficial próprio na internet?",
        "fundamento": "Art. 8º, §1º, I, da Lei 12.527/2011",
        "classificacao": "essencial",
        "aplicavel_a": "Todos",
        "disponibilidade": False,
        "atualidade": None,
        "serie_historica": None,
        "gravacao": None,
        "filtro": None,
        "justificativa": ""
    }

    try:
        dominio = urlparse(url).netloc
        if dominio.endswith(".gov.br"):
            resultado["disponibilidade"] = True
            resultado["justificativa"] = f"Domínio identificado: {dominio}"
        else:
            resultado["justificativa"] = f"Domínio inválido para órgão público: {dominio}"
    except Exception as e:
        resultado["justificativa"] = f"Erro na verificação de domínio: {str(e)}"

    return resultado
