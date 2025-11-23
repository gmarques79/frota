from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from parser import processar_pdf
from sheets import enviar_google_sheets
import uuid
import os

app = FastAPI()

#Permite acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.post("/upload")
async def upload_pdf(file: UploadFile = File(...)):
    filename = f"{uuid.uuid4()}.pdf"
    filepath = os.path.join(UPLOAD_FOLDER, filename)

    with open(filepath, "wb") as f:
        f.write(await file.read())

    dados = processar_pdf(filepath)

    enviar_google_sheets(dados)

    return {
        "status": "ok",
        "mensagem": "PDF processado e enviado ao Google Sheets!",
        "registros": len(dados)
    }
