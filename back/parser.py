import pandas as pd
import re

def parse_excel_abastecimentos(path):
    print("[DEBUG] Lendo Excel:", path)

    df = pd.read_excel(path, header=None)

    registros = []
    placa_atual = None

    for i in range(len(df)):
        row = df.iloc[i]

        if isinstance(row[0], str) and row[0].startswith("Placa:"):
            m = re.search(r"Placa:\s*([A-Z0-9\-]{6,8})", row[0])
            if m:
                placa_atual = m.group(1)
                print("[DEBUG] Placa detectada:", placa_atual)
            continue

        if placa_atual is None:
            continue

        data_hora = str(row[5]).strip()

        if " " in data_hora:
            data_str, hora_str = data_hora.split(" ", 1)
        else:
            data_str = data_hora
            hora_str = None


        if isinstance(data_hora, str) and re.match(r"\d{2}/\d{2}/\d{4}", data_hora):
            try:
                condutor = row[0]
                km_l = float(row[1])
                km_rodado = float(row[2])
                produto = str(row[11])
                valor_unitario = float(row[12])
                litros = float(row[13])
                valor_total = float(row[14])

                registros.append({
                    "placa": placa_atual,
                    "data": data_str,
                    "hora": hora_str,
                    "km_rodado": km_rodado,
                    "produto": produto,
                    "valor_unitario": valor_unitario,
                    "litros": litros,
                    "valor_total": valor_total
                })

            except Exception as e:
                print("[ERRO] Linha inválida:", row.tolist())
                print("Motivo:", e)

    print("[DEBUG] Total de registros extraídos:", len(registros))
    return registros
