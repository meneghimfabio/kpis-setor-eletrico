from typing import Optional
from fastapi import APIRouter, Query
from app.core.bigquery_client import bq_manager

router = APIRouter(prefix="/alerts", tags=["Alertas & Semáforo"])

@router.get("/")
def get_alerts(
    nivel: Optional[str] = Query(None, description="Filtrar por nível: critico, alerta, info"),
    modulo: Optional[str] = Query(None, description="Filtrar por módulo regulatório (ex: Distribuição, CCEE, SIN, Perdas)")
):
    """
    Retorna os alertas regulatórios calculados analiticamente a partir das tabelas da Camada Gold
    do BigQuery (kpi_dec_fec_conformidade, kpi_ccee_mercado_resumo, kpi_sin_operacao_resumo, etc.).
    Possui graceful fallback com motor analítico determinístico caso o BigQuery esteja indisponível.
    """
    raw_alerts = bq_manager.get_domain_data("alertas_regulatorios")
    alerts_list = raw_alerts if isinstance(raw_alerts, list) else raw_alerts.get("alertas", [])

    if nivel and nivel != "todos":
        alerts_list = [a for a in alerts_list if a.get("nivel") == nivel.lower()]

    if modulo:
        alerts_list = [a for a in alerts_list if modulo.lower() in a.get("modulo", "").lower()]

    source_info = "bigquery_gold" if bq_manager.client else "seed_fallback"

    return {
        "total": len(alerts_list),
        "alertas": alerts_list,
        "_metadata": {
            "source": source_info,
            "engine": "BigQuery Gold Analytical Engine" if bq_manager.client else "Analytical Seed Fallback Engine",
            "bi_engine_accelerated": True if bq_manager.client else False
        }
    }
