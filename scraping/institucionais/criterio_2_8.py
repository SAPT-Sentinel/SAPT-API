"""
Critério 2.8 – Participa em redes sociais e apresenta, no seu sítio institucional, link de acesso ao seu perfil?
➢ Fundamentação: Arts. 3º, III; 6º, I; e 8º, §2º da Lei nº 12.527/2011 – LAI.
➢ Classificação: Recomendada.
➢ Aplicável a: Executivo, Legislativo, Judiciário, Tribunal de Contas,
   Ministério Público, Consórcios Públicos e Estatais Dependentes e Independentes.

Requisitos:
- O site institucional deve apresentar links diretos para perfis em redes sociais oficiais.
- A presença pode estar no cabeçalho, rodapé ou em seções institucionais.
- Plataformas válidas: Facebook, Instagram, Twitter, WhatsApp, TikTok, etc.
"""

from bs4 import BeautifulSoup

def avaliar(html: str, soup: BeautifulSoup, url: str) -> dict:
    resultado = {
        "codigo": "2.8",
        "descricao": "Participa em redes sociais e apresenta link no site?",
        "fundamento": "Lei nº 12.527/2011, arts. 3º, 6º e 8º",
        "classificacao": "recomendada",
        "aplicavel_a": "Todos",
        "disponibilidade": False,
        "atualidade": None,
        "serie_historica": None,
        "gravacao": None,
        "filtro": None,
        "justificativa": "Não foram encontrados links de redes sociais visíveis na página."
    }

    redes = ["facebook.com", "instagram.com", "twitter.com", "tiktok.com", "whatsapp.com"]
    encontrados = []

    links = soup.find_all("a", href=True)
    for link in links:
        href = link['href'].lower()
        for rede in redes:
            if rede in href:
                encontrados.append(href)

    if encontrados:
        resultado["disponibilidade"] = True
        resultado["justificativa"] = "Links de redes sociais encontrados: " + ", ".join(set(encontrados))

    return resultado
