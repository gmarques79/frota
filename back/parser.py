import pdfplumber
import re

def ler_pdf(caminho):
    texto = ""
    with pdfplumber.open(caminho) as pdf:
        for pagina in pdf.pages:
            texto += pagina.extract_text() + "\n"
    return texto


def processar_pdf(caminho_pdf):
    texto = ler_pdf(caminho_pdf)

    linhas = texto.split("\n")

    resultados = []
    subunidade_atual = None
    placa_atual = None
    descricao_atual = None

    # Regex de captura dos abastecimentos
    regex_abastecimento = re.compile(
        r"([A-ZÁÉÍÓÚÂÊÔÃÕÇ ]+)\s+"                 
        r"([0-9,]+)\s+"                             
        r"([0-9]+)\s+"                              
        r"R\$\s*([0-9,]+)\s+"                       
        r"([0-9]+)\s+"                              
        r"([0-9/]{10})\s*([0-9:]{8})\s+"            
        r".*?\s+"                                  
        r"([A-Z0-9 ().,-/]+)\s+"                   
        r"([0-9]+)\s+"                              
        r"([0-9]+)\s+"                             
        r"([0-9]+)\s+"                              
        r"([A-Z0-9 ]+)\s+"                          
        r"R\$\s*([0-9,]+)\s+"                       
        r"([0-9,]+)\s+"                             
        r"R\$\s*([0-9,]+)\s+"                       
        r"([A-Z]+)",                                
        re.DOTALL
    )

    buffer_bloco = []

    for linha in linhas:
        linha = linha.strip()

        if linha.startswith("SUBUNIDADE:"):
            subunidade_atual = linha.replace("SUBUNIDADE:", "").strip()
            continue

        if linha.startswith("Placa:"):
            m = re.search(r"Placa:\s*([A-Z0-9\-]+).*Descricao:\s*(.*?)-", linha.replace("Descri��o", "Descrição"))
            if m:
                placa_atual = m.group(1).strip()
                descricao_atual = m.group(2).strip()
            buffer_bloco = []
            continue

        buffer_bloco.append(linha)
        bloco_texto = " ".join(buffer_bloco)

        for m in re.finditer(regex_abastecimento, bloco_texto):
            condutor = m.group(1).strip()
            km_l = float(m.group(2).replace(",", "."))
            km_rodado = int(m.group(3))
            data_hora = f"{m.group(6)} {m.group(7)}"
            estabelecimento = m.group(8).replace("  ", " ").strip()
            km_anterior = int(m.group(10))
            km_atual = int(m.group(11))
            produto = m.group(12).strip()
            valor_unitario = float(m.group(13).replace(",", "."))
            litros = float(m.group(14).replace(",", "."))
            valor_total = float(m.group(15).replace(",", "."))
            tipo_frota = m.group(16)

            resultados.append({
                "subunidade": subunidade_atual,
                "placa": placa_atual,
                "descricao": descricao_atual,
                "condutor": condutor,
                "data_hora": data_hora,
                "km_l": km_l,
                "km_rodado": km_rodado,
                "estabelecimento": estabelecimento,
                "km_anterior": km_anterior,
                "km_atual": km_atual,
                "produto": produto,
                "valor_unitario": valor_unitario,
                "litros": litros,
                "valor_total": valor_total,
                "tipo_frota": tipo_frota
            })

    return resultados


if __name__ == "__main__":
    caminho = "RelatorioConsumoSubUnidadeVeiculo-20251123125200.pdf"
    dados = processar_pdf(caminho)
    import json
    print(json.dumps(dados, indent=2, ensure_ascii=False))
