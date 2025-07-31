"""
Critério 4.3 – Possibilita a consulta de empenhos com os detalhes do beneficiário do pagamento ou credor, 
o bem fornecido ou serviço prestado e a identificação do procedimento licitatório originário da despesa?

➢ Fundamentação:
- Arts. 7º, VI e 8º, §1º, III da LAI (Lei nº 12.527/2011)
- Arts. 48, §1º, II e 48-A, I da LC nº 101/2000
- Art. 8º, I, “h” do Decreto nº 10.540/2020

➢ Classificação: Obrigatória
➢ Aplicável a: Executivo, Legislativo, Judiciário, TCs, MPs, Defensorias, Consórcios, Estatais

Disponibilidade:
Deve apresentar, por empenho:
- Nome do credor (pessoa física ou jurídica)
- Objeto do gasto (bem ou serviço)
- Identificação da licitação (modalidade + número ou tipo de dispensa)

Atualidade:
Dados com atualização inferior a 30 dias.

Série Histórica:
Informações de pelo menos 3 anos anteriores.

Gravação de Relatórios:
Exportação da base completa em formatos estruturados (CSV, XLS, etc.)

Filtro de Pesquisa:
Deve permitir busca por número do empenho, nome/CPF/CNPJ do credor, mês, ano.
"""

import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

def avaliar(html: str, soup: BeautifulSoup, url: str) -> dict:
    resultado = {
        "codigo": "4.3",
        "descricao": "Consulta de empenhos com detalhes do credor, objeto e licitação?",
        "fundamento": "LAI, LC 101/2000, Decreto 10.540/2020 art. 8º-I-h",
        "classificacao": "obrigatória",
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

    # Verifica presença dos elementos obrigatórios em qualquer parte da tabela ou detalhe
    if all(t in texto for t in ["credor", "objeto", "modalidade", "nº", "licitacao"]) or "procedimento licitatorio" in texto:
        resultado["disponibilidade"] = True
        justificativas.append("Informações de credor, objeto e licitação identificadas.")

    # Atualidade
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

    # Série histórica
    anos = re.findall(r"\b(20[0-2][0-9])\b", html)
    if len(set(anos)) >= 3:
        resultado["serie_historica"] = True
        justificativas.append(f"Série histórica com anos: {', '.join(sorted(set(anos)))}")

    # Exportação
    formatos = ["csv", "xls", "xlsx", "json", "xml"]
    links = soup.find_all("a", href=True)
    if any(any(fmt in a["href"].lower() for fmt in formatos) for a in links):
        resultado["gravacao"] = True
        justificativas.append("Exportação de relatórios disponível.")

    # Filtros
    if any(t in texto for t in ["buscar", "cpf", "cnpj", "credor", "empenho", "ano", "mês", "filtro"]):
        resultado["filtro"] = True
        justificativas.append("Filtros por empenho, credor, mês ou ano identificados.")

    resultado["justificativa"] = " | ".join(justificativas)
    return resultado
