"""
Critério 4.6 – Publica informações detalhadas sobre a execução dos contratos de publicidade?

➢ Fundamentação:
- Lei 12.527/2011 (LAI): Art. 3º, 6º, I, 7º II e VI, 8º caput e §§ 1º-2º
- Lei 13.303/2016: Art. 93
- Lei 12.232/2010: Art. 10

➢ Classificação: Recomendada
➢ Aplicável a: Estatais Dependentes e Independentes

Disponibilidade:
- Deve apresentar: nomes dos fornecedores de serviços especializados e veículos,
  totais de valores pagos por tipo de serviço e meio de divulgação.

Atualidade:
- Informações atualizadas nos últimos 6 meses.

Série Histórica:
- Dados de pelo menos 3 anos anteriores.

Gravação de Relatórios:
- Exportação da base em formatos como CSV, XLS, JSON, etc.

Filtro de Pesquisa:
- Deve permitir filtro por fornecedor, serviço, veículo, tipo de mídia, período, etc.
"""

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def avaliar(html: str, soup: BeautifulSoup, url: str) -> dict:
    resultado = {
        "codigo": "4.6",
        "descricao": "Publica informações sobre contratos de publicidade com fornecedores, veículos e valores?",
        "fundamento": "Lei 12.527/2011 (LAI); Lei 13.303/2016; Lei 12.232/2010",
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
    termos = ["publicidade", "fornecedor", "veículo", "tipo de serviço", "meio de divulgação", "valores pagos"]
    encontrados = [t for t in termos if t in texto]
    if len(encontrados) >= 3:
        resultado["disponibilidade"] = True
        justificativas.append(f"Elementos encontrados: {', '.join(encontrados)}")

    # Atualidade
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

    # Gravação de Relatórios
    formatos = ["csv", "xls", "xlsx", "json", "xml"]
    links = soup.find_all("a", href=True)
    if any(any(fmt in a["href"].lower() for fmt in formatos) for a in links):
        resultado["gravacao"] = True
        justificativas.append("Exportação disponível.")

    # Filtro
    filtros = ["filtro", "buscar", "veículo", "serviço", "fornecedor", "tipo de mídia", "ano", "período"]
    if any(f in texto for f in filtros):
        resultado["filtro"] = True
        justificativas.append("Filtros de pesquisa encontrados.")

    resultado["justificativa"] = " | ".join(justificativas)
    return resultado
