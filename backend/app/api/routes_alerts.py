from fastapi import APIRouter
from app.core.bigquery_client import bq_manager

router = APIRouter(prefix="/alerts", tags=["Alertas & Semáforo"])

@router.get("/")
def get_alerts():
    alerts = bq_manager.get_domain_data("alertas_regulatorios")
    return {"total": len(alerts), "alertas": alerts}
