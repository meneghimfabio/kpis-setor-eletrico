from fastapi import APIRouter
from app.core.bigquery_client import bq_manager

router = APIRouter(prefix="/ccee", tags=["Mercado CCEE"])

@router.get("/overview")
def get_ccee_overview():
    data = bq_manager.get_domain_data("mercado_ccee")
    return {
        "pld_atual": data.get("pld_atual", {}),
        "gsf_historico": data.get("gsf_historico", []),
        "ess_encargos": data.get("ess_encargos", {}),
        "bandeira_vigente": data.get("bandeira_vigente", {}),
        "curtailment": data.get("curtailment", []),
        "ultima_atualizacao_ccee": data.get("ultima_atualizacao_ccee", "Dados Oficiais CCEE")
    }
