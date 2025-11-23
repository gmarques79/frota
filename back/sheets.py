import gspread
import os
import json

from google.oauth2.service_account import Credentials

SPREADSHEET_NAME = "Relatorio SecLog Base"  
SHEET_TAB = "Base"                          

def get_credentials(scopes):
    cred_json = os.getenv("GOOGLE_CREDENTIALS_JSON")

    if not cred_json:
        raise Exception("Variável GOOGLE_CREDENTIALS_JSON não configurada.")

    cred_dict = json.loads(cred_json)

    return Credentials.from_service_account_info(cred_dict, scopes=scopes)

def enviar_google_sheets(dados):
    scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

    creds = get_credentials(scopes)
    client = gspread.authorize(creds)

    try:
        sh = client.open(SPREADSHEET_NAME)
    except:
        sh = client.create(SPREADSHEET_NAME)

    ws = None
    try:
        ws = sh.worksheet(SHEET_TAB)
    except:
        ws = sh.add_worksheet(SHEET_TAB, rows="100", cols="30")

    # cria cabeçalho se estiver vazio
    if ws.row_count == 0 or ws.get_all_values() == []:
        cabecalho = list(dados[0].keys())
        ws.append_row(cabecalho)

    # adiciona registros
    for item in dados:
        ws.append_row(list(item.values()))
