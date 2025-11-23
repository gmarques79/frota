import pdfplumber
import re

def ler_pdf(caminho):
    texto = ""
    with pdfplumber.open(caminho) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n"
    return texto

def dividir_blocos(texto):
    partes = texto.split("Placa:")
    return ["Placa:" + p for p in partes[1:]]

def extrair_cabecalho(bloco):
    m = re.search(r"Placa:\s*([A-Z0-9\-]+).*?Prefixo:\s*(.*?)\s*-\s*Descrição:\s*(.*?)\n", bloco)
    if not m:
        return None, None, None
    return m.group(1).strip(), m.group(2).strip(), m.group(3).strip()

def extrair_abastecimentos(bloco):
    abastecimentos = []

    padrao = re.compile(
        r"([A-ZÁÉÍÓÚÂÊÔÃÕÇ ]+)\n"
        r"([0-9,]+)\s+([0-9]+)\s+R\$\s*([0-9,]+)\s+([0-9]+)\s+([0-9/ :]+)\n"
        r".*?\n"
        r"(.*?)\n"
        r"([0-9]+)\s+([0-9]+)\s+([0-9]+)\s+([A-Z0-9 ]+)\s+R\$\s*([0-9,]+)\s+([0-9,]+)\s+R\$\s*([0-9,]+)\s+([A-Z]+)\s+([0-9]+)",
        re.DOTALL
    )

    for m in re.finditer(padrao, bloco):
        d = {
            "condutor": m.group(1).replace("\n", " ").strip(),
            "km_l": m.group(2),
            "km_rodado": m.group(3),
            "rs_km": m.group(4),
            "aut": m.group(5),
            "datahora": m.group(6),
            "estabelecimento": m.group(7),
            "registro": m.group(8),
            "km_ult": m.group(9),
            "km_atual": m.group(10),
            "produto": m.group(11),
            "vr_unit": m.group(12),
            "qtde": m.group(13),
            "valor": m.group(14),
            "tipo_frota": m.group(15),
            "patrimonio": m.group(16)
        }
        abastecimentos.append(d)

    return abastecimentos

def processar_pdf(caminho):
    texto = ler_pdf(caminho)
    blocos = dividir_blocos(texto)
    linhas = []

    for bloco in blocos:
        placa, prefixo, desc = extrair_cabecalho(bloco)
        abastecimentos = extrair_abastecimentos(bloco)

        for ab in abastecimentos:
            linhas.append({
                "placa": placa,
                "prefixo": prefixo,
                "descricao": desc,
                **ab
            })

    return linhas
