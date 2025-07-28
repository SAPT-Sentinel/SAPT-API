"""
Critério 1.2 - Possui portal da transparência próprio ou compartilhado?
Classificação: Essencial
Aplicável a: Todos os Poderes e Entes

Este critério será considerado atendido se a página inicial tiver um link visível
apontando para o portal da transparência, com texto ou URL sugerindo essa finalidade.
"""

def avaliar(html: str, soup, url: str) -> dict:
    resultado = {
        "codigo": "1.2",
        "descricao": "Possui portal da transparência próprio ou compartilhado?",
        "fundamento": "Art. 8º, §1º, II, da Lei 12.527/2011",
        "classificacao": "essencial",
        "aplicavel_a": "Todos",
        "disponibilidade": False,
        "atualidade": None,
        "serie_historica": None,
        "gravacao": None,
        "filtro": None,
        "justificativa": ""
    }

    palavras_chave = ["transparência", "acesso à informação", "acessoainformacao"]
    links = soup.find_all("a", href=True)

    for link in links:
        texto = link.get_text(strip=True).lower()
        href = link['href'].lower()
        if any(p in texto or p in href for p in palavras_chave):
            resultado["disponibilidade"] = True
            resultado["justificativa"] = f"Link encontrado: texto='{texto}', href='{href}'"
            break
    else:
        resultado["justificativa"] = "Nenhum link para portal da transparência encontrado."

    return resultado
