"""
Critério 3.1 – Divulga as receitas do Poder ou órgão, evidenciando sua previsão e realização?

➢ Fundamentação: Arts. 48, §1º, II e 48-A, II, da LC nº 101/00; Art. 8º, II, do Decreto nº 10.540/20.
➢ Classificação: Essencial.
➢ Aplicável a: Executivo, Legislativo, Judiciário, Tribunal de Contas, Ministério Público,
  Defensoria, Consórcios Públicos e Estatais Dependentes.

Disponibilidade:
Deve apresentar conjuntamente:
- Valores da receita pública prevista;
- Valores da receita pública realizada (inclusive recursos extraordinários).

Para os Poderes que não arrecadam diretamente (ex: Legislativo), considerar repasses (duodécimos).

Informações devem estar na mesma tela ou arquivo.

Atualidade:
Deve estar atualizada em até 30 dias da data da análise.

Série Histórica:
Pelo menos 3 anos anteriores ao da pesquisa.

Gravação de Relatórios:
Deve permitir exportação dos dados em formatos editáveis (csv, xls, json, etc.).

Filtro de Pesquisa:
Deve permitir filtro por exercício (ano) e período (data ou mês).
"""

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def avaliar(html: str, soup: BeautifulSoup, url: str) -> dict:
    resultado = {
        "codigo": "3.1",
        "descricao": "Divulga as receitas do Poder ou órgão, evidenciando sua previsão e realização?",
        "fundamento": "Arts. 48, §1º, II e 48-A, II, da LC nº 101/00; Art. 8º, II, do Decreto nº 10.540/20",
        "classificacao": "essencial",
        "aplicavel_a": "Todos",
        "disponibilidade": False,
        "atualidade": False,
        "serie_historica": False,
        "gravacao": False,
        "filtro": False,
        "justificativa": ""
    }

    def analisar_contexto(soup_local, html_local) -> list:
        justificativas = []
        texto = soup_local.get_text(separator=" ", strip=True).lower()

        if any(p in texto for p in ["valor previsto", "valor arrecadado"]):
            resultado["disponibilidade"] = True
            justificativas.append("Colunas de valor previsto e arrecadado presentes.")

        match_data = re.search(r"última atualização:\s*(\d{2}/\d{2}/\d{4})", html_local, re.IGNORECASE)
        if match_data:
            try:
                data = datetime.strptime(match_data.group(1), "%d/%m/%Y")
                if datetime.now() - data <= timedelta(days=30):
                    resultado["atualidade"] = True
                    justificativas.append(f"Atualizado em {match_data.group(1)}")
                else:
                    justificativas.append(f"Data desatualizada: {match_data.group(1)}")
            except:
                justificativas.append("Data encontrada, mas não pôde ser interpretada.")

        anos = re.findall(r"\b(20[0-2][0-9])\b", html_local)
        if len(set(anos)) >= 3:
            resultado["serie_historica"] = True
            justificativas.append(f"Série histórica com anos: {', '.join(sorted(set(anos)))}")

        formatos = ["pdf", "csv", "xls", "xlsx", "json", "xml"]
        links = soup_local.find_all("a", href=True)
        if any(any(fmt in a["href"].lower() for fmt in formatos) for a in links):
            resultado["gravacao"] = True
            justificativas.append("Exportação de relatórios disponível.")

        if any(term in texto for term in ["ano", "data inicial", "data final", "filtrar"]):
            resultado["filtro"] = True
            justificativas.append("Filtros por período identificados.")

        return justificativas

    # Primeiro: tentar na página original
    justificativas = analisar_contexto(soup, html)

    # Se não encontrou o mínimo (previsão + realização), tenta iframe
    if not resultado["disponibilidade"]:
        iframe = soup.find("iframe")
        if iframe and "governotransparente.com.br" in iframe.get("src", ""):
            try:
                res = requests.get(iframe["src"], timeout=20)
                res.raise_for_status()
                iframe_html = res.text
                iframe_soup = BeautifulSoup(iframe_html, "html.parser")
                justificativas = analisar_contexto(iframe_soup, iframe_html)
            except Exception as e:
                justificativas.append(f"Erro ao acessar iframe: {e}")
        else:
            justificativas.append("Iframe do Governotransparente não encontrado.")

    resultado["justificativa"] = " | ".join(justificativas)
    return resultado
