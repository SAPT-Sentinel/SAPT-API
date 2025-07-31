"""
Critério 4.4 – Publica relação das despesas com aquisições de bens efetuadas pela instituição contendo:
identificação do bem, preço unitário, quantidade, nome do fornecedor e valor total de cada aquisição?

➢ Fundamentação:
- Estatais Dependentes: Art. 3º c/c art. 6º, I, art. 7º, II e VI, art. 8º caput e §1º III-IV, §2º – Lei 12.527/2011 (LAI); Art. 48 da Lei 13.303/2016
- Estatais Independentes: Arts. 3º III, 6º I, e 8º §2º – Lei 12.527/2011 (LAI)

➢ Classificação: Recomendada
➢ Aplicável a: Estatais Dependentes e Independentes

Disponibilidade:
- Deve listar: identificação do bem, preço unitário, quantidade, fornecedor e valor total

Atualidade:
- Dados atualizados nos últimos 6 meses

Série Histórica:
- Pelo menos 3 anos anteriores

Gravação de Relatórios:
- Exportação da base em formatos como csv, xls, json, etc.

Filtro de Pesquisa:
- Deve permitir busca por descrição, fornecedor, ano, período ou outros parâmetros relevantes
"""

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def avaliar(html: str, soup: BeautifulSoup, url: str) -> dict:
    resultado = {
        "codigo": "4.4",
        "descricao": "Publica relação de aquisições de bens com preço, quantidade, fornecedor e valor total?",
        "fundamento": "Lei 12.527/2011 (LAI); Lei 13.303/2016",
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

    # Verifica presença dos campos obrigatórios
    campos = ["identificação do bem", "preço unitário", "quantidade", "fornecedor", "valor total"]
    encontrados = [c for c in campos if c in texto]
    if len(encontrados) >= 3:
        resultado["disponibilidade"] = True
        justificativas.append(f"Campos encontrados: {', '.join(encontrados)}")

    # Atualidade - até 6 meses atrás
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

    # Série Histórica
    anos = re.findall(r"\b(20[0-2][0-9])\b", html)
    if len(set(anos)) >= 3:
        resultado["serie_historica"] = True
        justificativas.append(f"Série histórica com anos: {', '.join(sorted(set(anos)))}")

    # Exportação
    formatos = ["csv", "xls", "xlsx", "json", "xml"]
    links = soup.find_all("a", href=True)
    if any(any(fmt in a["href"].lower() for fmt in formatos) for a in links):
        resultado["gravacao"] = True
        justificativas.append("Exportação disponível.")

    # Filtros
    if any(p in texto for p in ["filtro", "buscar", "fornecedor", "bem", "ano", "período"]):
        resultado["filtro"] = True
        justificativas.append("Filtros de pesquisa identificados.")

    resultado["justificativa"] = " | ".join(justificativas)
    return resultado
