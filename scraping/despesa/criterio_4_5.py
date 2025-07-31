"""
Critério 4.5 – Publica informações sobre despesas de patrocínio?

➢ Fundamentação:
- Art. 3º c/c art. 6º, I, c/c art. 7º, II e VI, c/c art. 8º, caput e §§ 1º-2º da Lei 12.527/2011 (LAI)
- Art. 93 da Lei 13.303/2016

➢ Classificação: Recomendada
➢ Aplicável a: Estatais Dependentes e Independentes

Disponibilidade:
- Deve divulgar as despesas classificadas como patrocínio

Atualidade:
- Informações devem estar atualizadas nos últimos 6 meses

Série Histórica:
- Deve conter dados de pelo menos 3 anos anteriores

Gravação de Relatórios:
- Exportação em formato estruturado como CSV, XLS, JSON, etc.

Filtro de Pesquisa:
- Deve permitir filtro por exercício, nome, entidade beneficiada ou tipo de patrocínio
"""

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def avaliar(html: str, soup: BeautifulSoup, url: str) -> dict:
    resultado = {
        "codigo": "4.5",
        "descricao": "Publica informações sobre despesas de patrocínio?",
        "fundamento": "Lei 12.527/2011 (LAI); Lei 13.303/2016 art. 93",
        "classificacao": "recomendada",
        "aplicavel_a": "Estatais",
        "disponibilidade": False,
        "atualidade": False,
        "serie_historica": False,
        "gravacao": False,
        "filtro": False,
        "justificativa": ""
    }

    justificativas = []
    texto = soup.get_text(separator=" ", strip=True).lower()

    # Disponibilidade
    if "patrocínio" in texto or "patrocinio" in texto:
        resultado["disponibilidade"] = True
        justificativas.append("Palavra-chave 'patrocínio' encontrada no conteúdo.")

    # Atualidade (últimos 6 meses)
    match_data = re.search(r"última atualização[:\s]+(\d{2}/\d{2}/\d{4})", html, re.IGNORECASE)
    if match_data:
        try:
            data = datetime.strptime(match_data.group(1), "%d/%m/%Y")
            if datetime.now() - data <= timedelta(days=183):
                resultado["atualidade"] = True
                justificativas.append(f"Atualizado em {match_data.group(1)}")
            else:
                justificativas.append(f"Data desatualizada: {match_data.group(1)}")
        except:
            justificativas.append("Data presente, mas não interpretável.")

    # Série histórica
    anos = re.findall(r"\b(20[0-2][0-9])\b", html)
    if len(set(anos)) >= 3:
        resultado["serie_historica"] = True
        justificativas.append(f"Série histórica com anos: {', '.join(sorted(set(anos)))}")

    # Gravação/exportação
    formatos = ["csv", "xls", "xlsx", "json", "xml"]
    links = soup.find_all("a", href=True)
    if any(any(fmt in a["href"].lower() for fmt in formatos) for a in links):
        resultado["gravacao"] = True
        justificativas.append("Exportação estruturada identificada.")

    # Filtros
    if any(p in texto for p in ["filtro", "exercício", "entidade", "nome", "buscar", "tipo de patrocínio"]):
        resultado["filtro"] = True
        justificativas.append("Filtros de pesquisa identificados.")

    resultado["justificativa"] = " | ".join(justificativas)
    return resultado
