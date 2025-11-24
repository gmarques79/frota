from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from parser import parse_excel_abastecimentos
from sheets import enviar_google_sheets
import uuid
import os

app = FastAPI()

# Permitir qualquer frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload")
async def upload_excel(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in [".xlsx", ".xls"]:
        return {"erro": "Envie um arquivo Excel (.xlsx)"}

    filename = f"{uuid.uuid4()}{ext}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, "wb") as f:
        f.write(await file.read())

    print(f"[DEBUG] Arquivo recebido: {filepath}")

    dados = parse_excel_abastecimentos(filepath)

    print(f"[DEBUG] Registros extraídos: {len(dados)}")

    enviar_google_sheets(dados)

    return {
        "status": "ok",
        "mensagem": "Excel processado e enviado ao Google Sheets!",
        "registros": len(dados)
    }
