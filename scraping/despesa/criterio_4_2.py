"""
Critério 4.2 – Divulga as despesas por classificação orçamentária?

➢ Fundamentação:
- Arts. 7º, VI e 8º, §1º, III da Lei nº 12.527/2011 (LAI)
- Arts. 48, §1º, II e 48-A, I da LC nº 101/2000
- Art. 8º, I do Decreto nº 10.540/2020

➢ Classificação: Essencial
➢ Aplicável a: Executivo, Legislativo, Judiciário, TCs, MPs, Defensorias, Consórcios, Estatais

Disponibilidade:
Deve divulgar:
- Unidade orçamentária
- Função
- Subfunção
- Natureza da despesa (categoria econômica, grupo, elemento)
- Fonte dos recursos

Atualidade:
Atualização deve ser inferior a 30 dias da data da avaliação.

Série Histórica:
Dados de pelo menos 3 anos anteriores.

Gravação de Relatórios:
Exportação da base completa em formatos estruturados (CSV, XLS, JSON, etc.).

Filtro de Pesquisa:
Deve permitir filtros por exercício, mês e estrutura orçamentária (com navegação entre níveis).
"""

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def avaliar(html: str, soup: BeautifulSoup, url: str) -> dict:
    resultado = {
        "codigo": "4.2",
        "descricao": "Divulga as despesas por classificação orçamentária?",
        "fundamento": "LAI arts. 7º, 8º; LC 101/2000 arts. 48, 48-A; Dec. 10.540/2020 art. 8º",
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

    # --- Disponibilidade: palavras-chave da classificação ---
    termos_classificacao = [
        "unidade orçamentária", "função", "subfunção", 
        "natureza da despesa", "categoria econômica", 
        "grupo", "elemento", "fonte de recurso"
    ]
    encontrados = [t for t in termos_classificacao if t in texto]
    if len(encontrados) >= 3:  # exige pelo menos 3 elementos visíveis
        resultado["disponibilidade"] = True
        justificativas.append(f"Elementos da classificação orçamentária encontrados: {', '.join(encontrados)}")

    # --- Atualidade ---
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
            justificativas.append("Data presente, mas não interpretável.")

    # --- Série histórica ---
    anos = re.findall(r"\b(20[0-2][0-9])\b", html)
    if len(set(anos)) >= 3:
        resultado["serie_historica"] = True
        justificativas.append(f"Série histórica com anos: {', '.join(sorted(set(anos)))}")

    # --- Exportação ---
    formatos = ["csv", "xls", "xlsx", "json", "xml"]
    links = soup.find_all("a", href=True)
    if any(any(fmt in a["href"].lower() for fmt in formatos) for a in links):
        resultado["gravacao"] = True
        justificativas.append("Opções de exportação detectadas.")

    # --- Filtros (ano, mês, estrutura orçamentária) ---
    if any(palavra in texto for palavra in ["filtrar", "exercício", "mês", "data inicial", "data final", "classificação", "expandir", "analítico"]):
        resultado["filtro"] = True
        justificativas.append("Filtros por classificação orçamentária ou período identificados.")

    resultado["justificativa"] = " | ".join(justificativas)
    return resultado
