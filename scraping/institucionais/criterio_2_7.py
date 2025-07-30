"""
Critério 2.7 – Divulga as perguntas e respostas mais frequentes relacionadas às atividades desenvolvidas?
➢ Fundamentação: Art. 8º, §1º, I, da Lei nº 12.527/2011 – LAI.
➢ Classificação: Obrigatória.
➢ Aplicável a: Executivo, Legislativo, Judiciário, Tribunal de Contas,
   Ministério Público, Consórcios Públicos, Estatais Dependentes e Independentes.

Requisitos:
- Página específica com título ou seção clara como “Perguntas Frequentes” ou “FAQ”
- Conteúdo voltado às atividades reais do órgão (não apenas perguntas genéricas)
- Estrutura de perguntas + respostas, preferencialmente em formato expandível
- Respostas devem trazer informações práticas ao cidadão
"""

from bs4 import BeautifulSoup

def avaliar(html: str, soup: BeautifulSoup, url: str) -> dict:
    resultado = {
        "codigo": "2.7",
        "descricao": "Divulga perguntas e respostas mais frequentes?",
        "fundamento": "Art. 8º, §1º, I, da Lei nº 12.527/2011",
        "classificacao": "obrigatória",
        "aplicavel_a": "Todos",
        "disponibilidade": False,
        "atualidade": None,
        "serie_historica": None,
        "gravacao": None,
        "filtro": None,
        "justificativa": "Não foram encontradas perguntas e respostas frequentes com conteúdo relevante."
    }

    texto = soup.get_text(separator=" ", strip=True).lower()

    if "sem perguntas frequentes" in texto:
        resultado["justificativa"] = "Página exibe mensagem padrão de ausência: 'Sem perguntas frequentes'."
        return resultado

    # Busca blocos de perguntas com formatação comum
    perguntas = [tag for tag in soup.find_all("a") if tag.get_text(strip=True).startswith("1.")]
    respostas = soup.find_all("div", class_="resposta")

    if len(perguntas) >= 3 and len(respostas) >= 3:
        resultado["disponibilidade"] = True
        resultado["justificativa"] = (
            f"Página contém {len(perguntas)} perguntas numeradas e {len(respostas)} respostas visíveis."
        )

    return resultado
