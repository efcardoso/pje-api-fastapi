from fastapi import FastAPI, Query
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Consulta Comunica PJe")

# Permitir chamadas de qualquer origem (útil para o GPT personalizado)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/consultar")
def consultar_comunicacoes(
    oab: str = Query(..., description="Número da OAB sem pontos ou barras"),
    dataInicio: str = Query(..., description="Data inicial no formato YYYY-MM-DD"),
    dataFim: str = Query(..., description="Data final no formato YYYY-MM-DD")
):
    url = "https://comunica.pje.jus.br/api/v1/comunicacao"
    params = {
        "oab": oab,
        "dataInicio": dataInicio,
        "dataFim": dataFim
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        dados = response.json()
        return {
            "total": len(dados),
            "resultados": dados
        }
    except requests.exceptions.RequestException as e:
        return {"erro": str(e)}