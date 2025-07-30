"""
Critério 2.6 – Divulga os atos normativos próprios?
➢ Fundamentação: Art. 37 da CF (princípio da publicidade) e arts. 3º, II;
   6º, I; 7º, II, V, VI e 8º da Lei nº 12.527/2011 – LAI.
➢ Classificação: Obrigatória.
➢ Aplicável a: Executivo, Legislativo, Judiciário, Tribunal de Contas,
   Ministério Público, Defensoria, Consórcios Públicos e Estatais.

Requisitos:
- Exibição dos atos normativos (portarias, decretos, instruções, resoluções)
- Documentos atualizados (últimos 30 dias)
- Série histórica (pelo menos 3 anos anteriores)
- Campo de filtro/pesquisa nos dados normativos
"""

import re
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def avaliar(html: str, soup: BeautifulSoup, url: str) -> dict:
    resultado = {
        "codigo": "2.6",
        "descricao": "Divulga os atos normativos próprios?",
        "fundamento": "Art. 37 da CF; Lei nº 12.527/2011, arts. 3º, 6º, 7º e 8º",
        "classificacao": "obrigatória",
        "aplicavel_a": "Todos",
        "disponibilidade": False,
        "atualidade": False,
        "serie_historica": False,
        "gravacao": None,
        "filtro": False,
        "justificativa": "Atos normativos não foram detectados com clareza."
    }

    texto = soup.get_text(separator=" ", strip=True).lower()
    html_lower = html.lower()

    # Verifica disponibilidade de termos normativos
    termos_normativos = ["decreto", "portaria", "resolução", "instrução normativa", "lei municipal"]
    encontrados = [t for t in termos_normativos if t in texto]
    if encontrados:
        resultado["disponibilidade"] = True

    # Verifica atualidade: data dentro dos últimos 30 dias
    datas = re.findall(r"(\\d{2}/\\d{2}/\\d{4})", texto)
    hoje = datetime.today()
    for data_str in datas:
        try:
            data = datetime.strptime(data_str, "%d/%m/%Y")
            if hoje - data <= timedelta(days=30):
                resultado["atualidade"] = True
                break
        except:
            continue

    # Verifica série histórica: pelo menos 3 anos anteriores
    anos = re.findall(r"(\\d{4})", texto)
    anos_validos = {int(a) for a in anos if a.isdigit() and 2000 < int(a) < hoje.year}
    if any(ano <= hoje.year - 3 for ano in anos_validos):
        resultado["serie_historica"] = True

    # Verifica se há campo de filtro na página
    filtros = soup.find_all("input", {"type": "text"})
    for f in filtros:
        if "busca" in f.get("name", "").lower() or "filtro" in f.get("name", "").lower():
            resultado["filtro"] = True
            break

    # Justificativa final
    partes = []
    if resultado["disponibilidade"]:
        partes.append("Atos normativos listados.")
    if resultado["atualidade"]:
        partes.append("Contém documentos recentes (últimos 30 dias).")
    if resultado["serie_historica"]:
        partes.append("Inclui documentos de anos anteriores (série histórica).")
    if resultado["filtro"]:
        partes.append("Campo de filtro de pesquisa disponível.")

    if partes:
        resultado["justificativa"] = " | ".join(partes)

    return resultado
