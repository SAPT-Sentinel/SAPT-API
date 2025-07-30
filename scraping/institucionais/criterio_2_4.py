"""
Critério 2.4 – Divulga os endereços e telefones atuais do Poder ou órgão e e-mails institucionais?
➢ Fundamentação: Art. 8º, §1º, I, da Lei nº 12.527/2011 - LAI e art. 6º, VI, b, da Lei 13.460/2017.
➢ Classificação: Obrigatória.
➢ Aplicável a: Executivo, Legislativo, Judiciário, Tribunal de Contas,
   Ministério Público, Defensoria, Consórcios Públicos, Estatais Dependentes e Independentes.

Disponibilidade:
Essas informações devem estar disponíveis no site institucional ou no portal da transparência.
São aceitas localizações no rodapé, seção “Contatos”, “Links úteis” ou página específica.

Para cumprimento mínimo, é necessário divulgar:
- Endereço físico da sede do órgão (e unidades, se aplicável);
- Número de telefone;
- E-mail institucional.
"""

import re
from bs4 import BeautifulSoup

def avaliar(html: str, soup: BeautifulSoup, url: str) -> dict:
    resultado = {
        "codigo": "2.4",
        "descricao": "Divulga os endereços e telefones atuais do Poder ou órgão e e-mails institucionais?",
        "fundamento": "Art. 8º, §1º, I, da Lei nº 12.527/2011 e art. 6º, VI, b, da Lei 13.460/2017",
        "classificacao": "obrigatória",
        "aplicavel_a": "Todos",
        "disponibilidade": False,
        "atualidade": None,
        "serie_historica": None,
        "gravacao": None,
        "filtro": None,
        "justificativa": "Não foram encontrados todos os elementos obrigatórios (endereço, telefone, e-mail)."
    }

    texto = soup.get_text(separator=" ", strip=True)

    # Expressões regulares para capturar os elementos
    padrao_telefone = re.compile(r'\(?\d{2}\)?\s?\d{4,5}[-\s]?\d{4}')
    padrao_email = re.compile(r'\b[\w\.-]+@[\w\.-]+\.\w{2,4}\b')
    padrao_endereco = re.compile(r'(rua|avenida|praça|travessa|estrada)\\s+[a-zà-ú0-9\\s,.-]{10,}', re.IGNORECASE)

    telefones = padrao_telefone.findall(texto)
    emails = padrao_email.findall(texto)
    enderecos = padrao_endereco.findall(texto)

    if telefones and emails and enderecos:
        resultado["disponibilidade"] = True
        resultado["justificativa"] = (
            f"Telefone(s) detectado(s): {len(telefones)} | "
            f"E-mail(s) detectado(s): {len(emails)} | "
            f"Endereço(s) identificado(s): {len(enderecos)}"
        )
    else:
        detalhes = []
        if not telefones:
            detalhes.append("telefone não encontrado")
        if not emails:
            detalhes.append("e-mail não encontrado")
        if not enderecos:
            detalhes.append("endereço não encontrado")
        resultado["justificativa"] = " ; ".join(detalhes)

    return resultado
