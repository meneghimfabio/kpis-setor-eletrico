from fastapi import APIRouter
from app.core.bigquery_client import bq_manager

router = APIRouter(prefix="/distribuicao", tags=["Distribuição & Qualidade"])

@router.get("/overview")
def get_distribuicao_overview():
    data = bq_manager.get_domain_data("distribuicao_qualidade")
    return {
        "ranking_dec_fec": data.get("ranking_dec_fec", []),
        "tensao_conformidade": data.get("tensao_conformidade", {}),
        "ultima_atualizacao_aneel": data.get("ultima_atualizacao_aneel", "Dados Oficiais ANEEL PRODIST"),
        "_metadata": data.get("_metadata")
    }
