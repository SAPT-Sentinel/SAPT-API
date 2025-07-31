"""
Critério 3.2 – Divulga a classificação orçamentária por natureza da receita (categoria econômica, origem, espécie)?

➢ Fundamentação: Art. 8º, II, 'e', do Decreto nº 10.540/2020.
➢ Classificação: Essencial.
➢ Aplicável a: Executivo.

Disponibilidade:
Deve apresentar, ao menos:
- Categoria econômica
- Origem
- Espécie
- Desdobramento
Exemplo: 111250 (1-Receitas Correntes; 1-Impostos; 1-Imp. Patrimônio; 2-IPTU)

Atualidade:
Atualização inferior a 30 dias da data da análise.

Série Histórica:
Dados devem estar disponíveis para pelo menos 3 anos anteriores.

Gravação de Relatórios:
Exportação da base completa em formato estruturado e legível por máquina.

Filtro de Pesquisa:
Navegação entre os níveis da classificação (colapsos, setas, etc.).
"""

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def avaliar(html: str, soup: BeautifulSoup, url: str) -> dict:
    resultado = {
        "codigo": "3.2",
        "descricao": "Divulga a classificacao orcamentaria por natureza da receita (categoria economica, origem, especie)?",
        "fundamento": "Art. 8º, II, 'e', do Decreto nº 10.540/2020",
        "classificacao": "essencial",
        "aplicavel_a": "Executivo",
        "disponibilidade": False,
        "atualidade": False,
        "serie_historica": False,
        "gravacao": False,
        "filtro": False,
        "justificativa": ""
    }

    def analisar_bloco(soup_local, html_local) -> list:
        justificativas = []
        texto = soup_local.get_text(separator=" ", strip=True).lower()

        # --- Classificacao por natureza (ex: 111250 + descricoes) ---
        if re.search(r"\b1{1,2}[0-9]{3,4}\b", texto) and any(p in texto for p in ["receitas correntes", "iptu", "impostos"]):
            resultado["disponibilidade"] = True
            justificativas.append("Classificação por natureza da receita detectada (ex: 111250).")

        # --- Atualidade ---
        match_data = re.search(r"última atualização:\s*(\d{2}/\d{2}/\d{4})", html_local, re.IGNORECASE)
        if match_data:
            try:
                data = datetime.strptime(match_data.group(1), "%d/%m/%Y")
                if datetime.now() - data <= timedelta(days=30):
                    resultado["atualidade"] = True
                    justificativas.append(f"Atualizado em {match_data.group(1)}")
                else:
                    justificativas.append(f"Desatualizado (data: {match_data.group(1)})")
            except:
                justificativas.append("Data presente mas não foi interpretada.")

        # --- Série histórica ---
        anos = re.findall(r"\b(20[0-2][0-9])\b", html_local)
        if len(set(anos)) >= 3:
            resultado["serie_historica"] = True
            justificativas.append(f"Série histórica detectada: {', '.join(sorted(set(anos)))}")

        # --- Gravação ---
        formatos = ["csv", "xls", "xlsx", "json", "xml", "txt"]
        links = soup_local.find_all("a", href=True)
        if any(any(fmt in a["href"].lower() for fmt in formatos) for a in links):
            resultado["gravacao"] = True
            justificativas.append("Botões de exportação detectados.")

        # --- Navegabilidade/filtro estrutural ---
        if any(icon in html_local for icon in ["fa-chevron-down", "fa-chevron-right", "expandir"]):
            resultado["filtro"] = True
            justificativas.append("Navegação entre níveis da classificação detectada.")

        return justificativas

    # Primeiro: analisa a página principal
    justificativas = analisar_bloco(soup, html)

    # Se classificação não for encontrada, tenta iframe externo
    if not resultado["disponibilidade"]:
        iframe = soup.find("iframe")
        if iframe and "governotransparente.com.br" in iframe.get("src", ""):
            try:
                res = requests.get(iframe["src"], timeout=20)
                res.raise_for_status()
                iframe_html = res.text
                iframe_soup = BeautifulSoup(iframe_html, "html.parser")
                justificativas = analisar_bloco(iframe_soup, iframe_html)
            except Exception as e:
                justificativas.append(f"Erro ao carregar iframe: {e}")
        else:
            justificativas.append("Iframe com classificação não encontrado.")

    resultado["justificativa"] = " | ".join(justificativas)
    return resultado
