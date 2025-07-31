"""
Critério 3.3 – Divulga a lista dos inscritos em dívida ativa, contendo, no mínimo, dados referentes ao nome do inscrito e o valor total da dívida?

➞ Fundamentação: Art. 198, §3º, II da Lei 5.172/1966 (CTN).
➞ Classificação: Obrigatória.
➞ Aplicável a: Executivo

Disponibilidade:
Deve apresentar:
- Nome do inscrito
- Valor total da dívida

A publicação da dívida ativa é permitida por lei, desde que protegidos dados pessoais sensíveis (CPF, endereço).

Atualidade:
Deve conter informações atualizadas até o último exercício encerrado.

Série Histórica:
Considera-se atendido quando há registros para pelo menos 3 anos anteriores.

Gravação de relatórios:
Exportação da base completa em formatos editáveis como CSV, XLS, JSON, etc.

Filtro de Pesquisa:
Deve permitir filtro por nome e ano de inscrição em dívida ativa.
"""

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def avaliar(html: str, soup: BeautifulSoup, url: str) -> dict:
    resultado = {
        "codigo": "3.3",
        "descricao": "Divulga a lista dos inscritos em dívida ativa, contendo nome e valor total da dívida?",
        "fundamento": "Art. 198, §3º, II da Lei 5.172/1966 (CTN)",
        "classificacao": "obrigatória",
        "aplicavel_a": "Executivo",
        "disponibilidade": False,
        "atualidade": False,
        "serie_historica": False,
        "gravacao": False,
        "filtro": False,
        "justificativa": ""
    }

    justificativas = []
    texto = soup.get_text(separator=" ", strip=True).lower()

    # --- Nome + Valor ---
    if any(p in texto for p in ["nome", "valor", "dívida ativa"]):
        if re.search(r"\bnome\b.*\bvalor\b", texto) or "valor da dívida" in texto:
            resultado["disponibilidade"] = True
            justificativas.append("Colunas de nome e valor da dívida identificadas.")

    # --- Atualidade ---
    match_data = re.search(r"última atualização[:\s]+(\d{2}/\d{2}/\d{4})", html, re.IGNORECASE)
    if match_data:
        try:
            data = datetime.strptime(match_data.group(1), "%d/%m/%Y")
            if datetime.now() - data <= timedelta(days=365):
                resultado["atualidade"] = True
                justificativas.append(f"Atualizado em {match_data.group(1)}")
            else:
                justificativas.append(f"Data desatualizada: {match_data.group(1)}")
        except:
            justificativas.append("Data presente, mas não pôde ser interpretada.")

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
        justificativas.append("Exportação da base detectada.")

    # --- Filtros ---
    if any(t in texto for t in ["filtrar", "buscar", "nome", "ano"]):
        resultado["filtro"] = True
        justificativas.append("Filtros de nome e/ou ano identificados.")

    resultado["justificativa"] = " | ".join(justificativas)
    return resultado
