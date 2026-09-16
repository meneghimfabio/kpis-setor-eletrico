from fastapi import APIRouter
from app.core.bigquery_client import bq_manager

router = APIRouter(prefix="/perdas-mmgd", tags=["Perdas & MMGD"])

@router.get("/overview")
def get_perdas_mmgd_overview():
    data = bq_manager.get_domain_data("perdas_mmgd")
    return {
        "balanco_nacional": data.get("balanco_nacional", {}),
        "perdas_distribuidoras": data.get("perdas_por_distribuidora", []),
        "mmgd_estatisticas": data.get("mmgd_estatisticas", {}),
        "inadimplencia_pdd": data.get("inadimplencia_pdd", []),
        "ultima_atualizacao_aneel": data.get("ultima_atualizacao_aneel", "Dados Oficiais ANEEL / MMGD"),
        "_metadata": data.get("_metadata")
    }
