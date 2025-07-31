"""
Critério 4.1 – Divulga o total das despesas empenhadas, liquidadas e pagas?

➞ Fundamentação:
- Art. 7º, VI e Art. 8º, §1º, III da Lei nº 12.527/2011 (LAI)
- Arts. 48, §1º, II e 48-A, I da LC nº 101/2000
- Art. 8º, I do Decreto nº 10.540/2020

➞ Classificação: Essencial
➞ Aplicável a: Executivo, Legislativo, Judiciário, Tribunais de Contas, Ministérios Públicos, Defensorias, Consórcios, Estatais

Disponibilidade:
- Deve exibir os totais de despesa empenhada, liquidada e paga
- Preferencialmente em uma única tela ou documento, para facilitar comparabilidade

Atualidade:
- Deve estar atualizada em até 30 dias anteriores à data da avaliação

Série Histórica:
- Deve apresentar dados de pelo menos 3 anos anteriores

Gravação de relatórios:
- Deve permitir exportação da base em formatos como CSV, XLS, JSON etc.

Filtro de Pesquisa:
- Deve haver filtros por ano, mês ou período
"""

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def avaliar(html: str, soup: BeautifulSoup, url: str) -> dict:
    resultado = {
        "codigo": "4.1",
        "descricao": "Divulga o total das despesas empenhadas, liquidadas e pagas?",
        "fundamento": "Art. 7º, VI e 8º, §1º, III da LAI; LC 101/00 art. 48, 48-A; Dec. 10.540/20 art. 8º",
        "classificacao": "essencial",
        "aplicavel_a": "Todos",
        "disponibilidade": False,
        "atualidade": False,
        "serie_historica": False,
        "gravacao": False,
        "filtro": False,
        "justificativa": ""
    }

    justificativas = []
    texto = soup.get_text(separator=" ", strip=True).lower()

    # Verifica colunas de despesa
    if all(p in texto for p in ["empenhado", "liquidado", "pago"]):
        resultado["disponibilidade"] = True
        justificativas.append("Totais de despesa empenhada, liquidada e paga identificados.")

    # Verifica data de atualização
    match_data = re.search(r"última atualização[:\s]+(\d{2}/\d{2}/\d{4})", html, re.IGNORECASE)
    if match_data:
        try:
            data = datetime.strptime(match_data.group(1), "%d/%m/%Y")
            if datetime.now() - data <= timedelta(days=30):
                resultado["atualidade"] = True
                justificativas.append(f"Atualizado em {match_data.group(1)}")
            else:
                justificativas.append(f"Data desatualizada: {match_data.group(1)}")
        except:
            justificativas.append("Data presente, mas não pôde ser interpretada.")

    # Verifica série histórica
    anos = re.findall(r"\b(20[0-2][0-9])\b", html)
    if len(set(anos)) >= 3:
        resultado["serie_historica"] = True
        justificativas.append(f"Série histórica com anos: {', '.join(sorted(set(anos)))}")

    # Verifica opções de exportação
    formatos = ["csv", "xls", "xlsx", "json", "xml"]
    links = soup.find_all("a", href=True)
    if any(any(fmt in a["href"].lower() for fmt in formatos) for a in links):
        resultado["gravacao"] = True
        justificativas.append("Exportação de relatórios identificada.")

    # Verifica filtros
    if any(t in texto for t in ["ano", "período", "filtrar", "data inicial", "data final"]):
        resultado["filtro"] = True
        justificativas.append("Filtros por período identificados.")

    resultado["justificativa"] = " | ".join(justificativas)
    return resultado
