"""
Critério 1.3 - O acesso ao portal transparência está visível na capa do site?
Classificação: Essencial
Aplicável a: Todos

Este critério será atendido se o link de transparência estiver em uma posição visível,
como no menu principal ou cabeçalho da página.
"""

def avaliar(html: str, soup, url: str) -> dict:
    resultado = {
        "codigo": "1.3",
        "descricao": "O acesso ao portal transparência está visível na capa do site?",
        "fundamento": "Boas práticas PNTP",
        "classificacao": "essencial",
        "aplicavel_a": "Todos",
        "disponibilidade": False,
        "atualidade": None,
        "serie_historica": None,
        "gravacao": None,
        "filtro": None,
        "justificativa": ""
    }

    header = soup.find('header') or soup.find('nav')
    if header:
        links = header.find_all("a", href=True)
        for link in links:
            texto = link.get_text(strip=True).lower()
            href = link['href'].lower()
            if "transparência" in texto or "acesso" in href:
                resultado["disponibilidade"] = True
                resultado["justificativa"] = f"Link visível no cabeçalho: '{texto}' - href='{href}'"
                break
        else:
            resultado["justificativa"] = "Nenhum link visível para transparência encontrado no cabeçalho."
    else:
        resultado["justificativa"] = "Elemento <header> ou <nav> não encontrado."

    return resultado
