from fastapi import APIRouter
from app.core.bigquery_client import bq_manager

router = APIRouter(prefix="/atendimento", tags=["Atendimento Comercial"])

@router.get("/overview")
def get_atendimento_overview():
    data = bq_manager.get_domain_data("atendimento_cliente")
    return {
        "ranking_iasc": data.get("ranking_iasc", []),
        "canais_atendimento": data.get("canais_atendimento", {}),
        "slas_comerciais": data.get("slas_comerciais", []),
        "ouvidoria_aneel": data.get("ouvidoria_aneel", []),
        "ultima_atualizacao_aneel": data.get("ultima_atualizacao_aneel", "Dados Oficiais ANEEL Ouvidoria & IASC"),
        "_metadata": data.get("_metadata")
    }
