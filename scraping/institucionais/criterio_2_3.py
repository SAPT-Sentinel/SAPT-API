"""
Critério 2.3 – Identifica o nome dos atuais responsáveis pela gestão do Poder/Órgão?
➢ Fundamentação: Art. 8º, §3º, I, da Lei nº 12.527/2011 – LAI.
➢ Classificação: Obrigatória.
➢ Aplicável a: Executivo, Legislativo, Judiciário, Tribunal de Contas, Ministério Público,
    Defensoria, Consórcios Públicos, Estatais Dependentes e Independentes.

Nesta página (/institucional), identifica cargos como “Prefeito”, “Secretário (a)”, além
de seções como “PREFEITO E VICE”, listando responsáveis com seus respectivos nomes.
"""
from bs4 import BeautifulSoup
import re

def avaliar(html: str, soup: BeautifulSoup, url: str) -> dict:
    resultado = {
        "codigo": "2.3",
        "descricao": "Identifica o nome dos atuais responsáveis pela gestão do Poder/Órgão?",
        "fundamento": "Art. 8º, §3º, I, da Lei nº 12.527/2011",
        "classificacao": "obrigatória",
        "aplicavel_a": "Todos",
        "disponibilidade": False,
        "atualidade": None,
        "serie_historica": None,
        "gravacao": None,
        "filtro": None,
        "justificativa": "Nenhum responsável claramente identificado na página."
    }

    texto = soup.get_text(separator="\n", strip=True)
    texto_lower = texto.lower()

    # Títulos indicativos estruturais
    if "prefeito e vice" in texto_lower or "prefeito" in texto_lower:
        # Captura nomes depois dos títulos
        matches = re.findall(r"(prefeito[a]?:?\s*[a-zãâéêíóúç ]+)", texto_lower)
        nomes = []
        for m in matches:
            # limpa prefixo e caracteres extras
            names_only = m.split(":")[-1].strip()
            if names_only and names_only not in nomes:
                nomes.append(names_only.title())
        if nomes:
            resultado["disponibilidade"] = True
            resultado["justificativa"] = (
                "Responsáveis identificados: " + ", ".join(nomes)
            )
            return resultado

    # Busca por cargos comuns e nomes próprios no texto
    cargos = ["secretário", "secretária", "vice-prefeito", "controlador", "procurador geral"]
    encontrados = []
    for cargo in cargos:
        if cargo in texto_lower:
            encontrados.append(cargo)

    # Captura linhas completas que contenham cargo e nome
    if encontrados:
        linhas = texto.split("\n")
        nomes_lidos = []
        for linha in linhas:
            low = linha.lower()
            for cargo in encontrados:
                if cargo in low:
                    nomes_lidos.append(linha.strip())
        if nomes_lidos:
            resultado["disponibilidade"] = True
            resultado["justificativa"] = (
                "Linhas com cargo+nome presentes: " + "; ".join(nomes_lidos[:3])
            )

    return resultado
