"""
Critério 1.4 - O site e o portal contêm ferramenta de pesquisa de conteúdo?
Classificação: Recomendado
Aplicável a: Todos os Poderes

Considera-se atendido se houver campo de busca (<input type='text'> ou similar)
presente na página inicial ou em páginas do portal.
"""

def avaliar(html: str, soup, url: str) -> dict:
    resultado = {
        "codigo": "1.4",
        "descricao": "O site e o portal contêm ferramenta de pesquisa de conteúdo?",
        "fundamento": "Boas práticas PNTP",
        "classificacao": "recomendado",
        "aplicavel_a": "Todos",
        "disponibilidade": False,
        "atualidade": None,
        "serie_historica": None,
        "gravacao": None,
        "filtro": None,
        "justificativa": ""
    }

    campos_busca = soup.find_all("input", {"type": ["text", "search"]})
    if campos_busca:
        resultado["disponibilidade"] = True
        resultado["justificativa"] = f"Encontrado(s) {len(campos_busca)} campo(s) de busca na página."
    else:
        resultado["justificativa"] = "Nenhum campo de busca encontrado."

    return resultado
