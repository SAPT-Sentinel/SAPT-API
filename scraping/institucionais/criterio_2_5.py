"""
Critério 2.5 – Divulga o horário de atendimento?
➢ Fundamentação: Art. 8º, §1º, I, da Lei nº 12.527/2011 – LAI e art. 6º, VI, b, da Lei 13.460/2017.
➢ Classificação: Obrigatória.
➢ Aplicável a: Executivo, Legislativo, Judiciário, Tribunal de Contas, Ministério Público,
   Defensoria, Consórcios Públicos, Estatais Dependentes e Independentes.

Disponibilidade:
É aceita a divulgação tanto no portal da transparência quanto no site institucional.
Deve ser referenciado o horário de atendimento ao público das unidades administrativas — 
não se confunde com horário da Ouvidoria ou do Serviço de Atendimento ao Cidadão (SIC).

Exemplos válidos:
- “Atendimento de segunda a sexta, das 08h às 14h”
- “Funcionamento: 07:30 às 13:30”
"""

import re
from bs4 import BeautifulSoup

def avaliar(html: str, soup: BeautifulSoup, url: str) -> dict:
    resultado = {
        "codigo": "2.5",
        "descricao": "Divulga o horário de atendimento?",
        "fundamento": "Art. 8º, §1º, I, da Lei nº 12.527/2011 e art. 6º, VI, b, da Lei 13.460/2017",
        "classificacao": "obrigatória",
        "aplicavel_a": "Todos",
        "disponibilidade": False,
        "atualidade": None,
        "serie_historica": None,
        "gravacao": None,
        "filtro": None,
        "justificativa": "Horário de atendimento não identificado na página."
    }

    texto = soup.get_text(separator=" ", strip=True).lower()

    # Padrões comuns de horário
    padrao_horario = re.compile(r"(das?\\s*\\d{1,2}[:h]?\\d{0,2}\\s*(às|as|a)\\s*\\d{1,2}[:h]?\\d{0,2})")
    padrao_turnos = re.compile(r"(expediente|atendimento|funcionamento):?\\s*(segunda.*sexta|segunda.*a.*sexta).*\\d{1,2}[:h]?\\d{0,2}")

    encontrou = False
    justificativas = []

    horarios = padrao_horario.findall(texto)
    if horarios:
        encontrou = True
        justificativas.append(f"Horário(s) encontrado(s): {', '.join(h[0] for h in horarios)}")

    turnos = padrao_turnos.findall(texto)
    if turnos:
        encontrou = True
        justificativas.append("Expressão típica de expediente administrativo detectada.")

    if encontrou:
        resultado["disponibilidade"] = True
        resultado["justificativa"] = " | ".join(justificativas)

    return resultado
