"""
Critério 2.2 – Divulga competências e/ou atribuições?
➢ Fundamentação: Art. 8º, §1º, I, da Lei nº 12.527/2011 – LAI e art. 6º, VI, b, da Lei 13.460/2017.
➢ Classificação: Obrigatória.
➢ Aplicável a: Executivo, Legislativo, Judiciário, Tribunal de Contas, Ministério Público,
  Defensoria, Consórcios e Estatais.

A página institucional contém seções com títulos como “Competências”,
além de referências a cargos-chave com descrição funcional.
"""

from bs4 import BeautifulSoup

def avaliar(html: str, soup: BeautifulSoup, url: str) -> dict:
    resultado = {
        "codigo": "2.2",
        "descricao": "Divulga competências e/ou atribuições?",
        "fundamento": "Art. 8º, §1º, I, da Lei nº 12.527/2011 e art. 6º, VI, b, da Lei 13.460/2017",
        "classificacao": "obrigatória",
        "aplicavel_a": "Todos",
        "disponibilidade": False,
        "atualidade": None,
        "serie_historica": None,
        "gravacao": None,
        "filtro": None,
        "justificativa": "Não foram encontradas informações claras sobre competências institucionais."
    }

    texto = soup.get_text(separator=" ", strip=True).lower()

    palavras_chave = [
        "competência", "atribuições", "responsabilidades", 
        "finalidade", "funções institucionais", "área de atuação"
    ]

    cargos_indicativos = [
        "controlador", "chefe de gabinete", "procurador geral", 
        "secretário", "secretária", "diretor", "coordenador", "gestor"
    ]

    termos_encontrados = []

    for palavra in palavras_chave + cargos_indicativos:
        if palavra in texto:
            termos_encontrados.append(palavra)

    if termos_encontrados:
        resultado["disponibilidade"] = True
        resultado["justificativa"] = (
            "Termos relacionados a competências identificados: "
            + ", ".join(set(termos_encontrados))
        )

    return resultado
