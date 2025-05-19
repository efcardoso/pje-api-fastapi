from fastapi import FastAPI, Query
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Consulta Comunica PJe")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/consultar")
def consultar_comunicacoes(
    numeroOab: str = Query(..., description="Número da OAB (ex: 443447)"),
    ufOab: str = Query(..., description="UF da OAB (ex: SP)"),
    dataInicio: str = Query(..., description="Data inicial no formato YYYY-MM-DD"),
    dataFim: str = Query(..., description="Data final no formato YYYY-MM-DD")
):
    url = "https://comunicaapi.pje.jus.br/api/v1/comunicacao"
    params = {
        "numeroOab": numeroOab,
        "ufOab": ufOab,
        "dataDisponibilizacaoInicio": dataInicio,
        "dataDisponibilizacaoFim": dataFim
    }
    try:
        headers = {
    "Authorization": "Bearer teste"
}

response = requests.get(url, params=params, headers=headers, timeout=20)

        response.raise_for_status()
        dados = response.json()
        return {
            "total": len(dados),
            "resultados": dados
        }
    except requests.exceptions.RequestException as e:
        return {"erro": str(e)}
