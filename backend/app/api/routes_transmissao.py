from fastapi import APIRouter
from app.core.bigquery_client import bq_manager

router = APIRouter(prefix="/transmissao", tags=["Transmissão"])

@router.get("/overview")
def get_transmissao_overview():
    data = bq_manager.get_domain_data("transmissao")
    return {
        "kpis_resumo": data.get("kpis_resumo", {}),
        "concessionarias": data.get("concessionarias", []),
        "desligamentos_recentes": data.get("desligamentos_recentes", [])
    }
