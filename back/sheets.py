import gspread
import os
import json
from google.oauth2.service_account import Credentials

# agora esse codigo compartilha a planilha com meu drive

SPREADSHEET_NAME = "Relatorio SecLog Base"
SHEET_TAB = "Base"

SEU_EMAIL = os.getenv("EMAIL") 

def get_credentials(scopes):
    cred_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

    if not cred_json:
        raise Exception("Variável GOOGLE_CREDENTIALS_JSON não configurada.")

    cred_dict = json.loads(cred_json)
    return Credentials.from_service_account_info(cred_dict, scopes=scopes)

def get_or_create_spreadsheet(client):
    try:
        sh = client.open(SPREADSHEET_NAME)
        print(f"[INFO] Planilha encontrada: {SPREADSHEET_NAME}")
    except gspread.SpreadsheetNotFound:
        sh = client.create(SPREADSHEET_NAME)
        print(f"[INFO] Planilha criada: {SPREADSHEET_NAME}")

        try:
            sh.share(SEU_EMAIL, perm_type="user", role="writer")
            print(f"[INFO] Planilha compartilhada com {SEU_EMAIL}")
        except Exception as e:
            print("[ERRO] Falha ao compartilhar planilha:", e)

    return sh


def get_or_create_worksheet(sh):
    try:
        ws = sh.worksheet(SHEET_TAB)
        print(f"[INFO] Aba encontrada: {SHEET_TAB}")
    except gspread.WorksheetNotFound:
        ws = sh.add_worksheet(SHEET_TAB, rows="500", cols="30")
        print(f"[INFO] Aba criada: {SHEET_TAB}")

    return ws

def enviar_google_sheets(dados):
    print("[INFO] Iniciando envio ao Google Sheets...")

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    creds = get_credentials(scopes)
    client = gspread.authorize(creds)

    sh = get_or_create_spreadsheet(client)

    ws = get_or_create_worksheet(sh)

    valores_existentes = ws.get_all_values()
    if len(valores_existentes) == 0:
        cabecalho = list(dados[0].keys())
        ws.append_row(cabecalho)
        print("[INFO] Cabeçalho criado.")

    matriz = []
    for item in dados:
        matriz.append(list(item.values()))

    ws.append_rows(matriz, value_input_option="USER_ENTERED")

    print(f"[INFO] {len(matriz)} registros enviados com sucesso.")
