from fastapi import APIRouter
from app.core.bigquery_client import bq_manager

router = APIRouter(prefix="/sin", tags=["Operação do SIN"])

@router.get("/overview")
def get_sin_overview():
    data = bq_manager.get_domain_data("operacao_sin")
    return {
        "ear_atual": data.get("ear_atual", data.get("ear_subsistemas", [])),
        "ear_historico": data.get("ear_historico_meses", []),
        "ena_subsistemas": data.get("ena_subsistemas", []),
        "cmo_atual": data.get("cmo_atual", []),
        "cmo_historico": data.get("cmo_historico", []),
        "ultima_atualizacao_ons": data.get("ultima_atualizacao_ons", "Dados Oficiais ONS")
    }
