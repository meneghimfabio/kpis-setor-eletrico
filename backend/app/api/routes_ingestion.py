from fastapi import APIRouter, BackgroundTasks, Query
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from app.ingestion.ons_sin import ons_ingestor
from app.ingestion.ccee_market import ccee_ingestor
from app.ingestion.aneel_distribution import aneel_ingestor
from app.ingestion.aneel_perdas_mmgd import aneel_perdas_mmgd_ingestor

router = APIRouter(prefix="/ingestion", tags=["Ingestao de Dados"])

class IngestionRequest(BaseModel):
    years: Optional[List[int]] = [2025, 2026]
    async_mode: Optional[bool] = False

@router.get("/sin/status")
def get_sin_ingestion_status():
    """Retorna o status da ultima execucao do pipeline ONS (Operacao do SIN)."""
    return ons_ingestor.last_status

@router.post("/sin/run")
def trigger_sin_ingestion(payload: Optional[IngestionRequest] = None, background_tasks: BackgroundTasks = None):
    """
    Dispara a ingestao dos dados abertos do ONS (EAR, ENA, CMO) para os anos selecionados.
    """
    years = payload.years if payload and payload.years else [2025, 2026]
    async_mode = payload.async_mode if payload else False

    if async_mode and background_tasks:
        background_tasks.add_task(ons_ingestor.run_pipeline, years)
        return {
            "message": "Ingestao ONS iniciada em background.",
            "years": years,
            "status": "processing"
        }
    
    result = ons_ingestor.run_pipeline(years)
    return {
        "message": "Ingestao ONS concluida com sucesso.",
        "result": result
    }

@router.get("/ccee/status")
def get_ccee_ingestion_status():
    """Retorna o status da ultima execucao do pipeline de Mercado CCEE."""
    return ccee_ingestor.last_status

@router.post("/ccee/run")
def trigger_ccee_ingestion(background_tasks: BackgroundTasks = None):
    """
    Dispara a ingestao e atualizacao dos dados de Mercado CCEE (PLD, GSF, ESS, Bandeiras).
    """
    result = ccee_ingestor.run_pipeline()
    return {
        "message": "Ingestao Mercado CCEE concluida com sucesso.",
        "result": result
    }

@router.get("/distribuicao/status")
def get_distribuicao_ingestion_status():
    """Retorna o status da ultima execucao do pipeline ANEEL PRODIST."""
    return aneel_ingestor.last_status

@router.post("/distribuicao/run")
def trigger_distribuicao_ingestion(background_tasks: BackgroundTasks = None):
    """
    Dispara a ingestao e atualizacao dos dados de qualidade da distribuicao da ANEEL (PRODIST Modulo 8).
    """
    result = aneel_ingestor.run_pipeline()
    return {
        "message": "Ingestao ANEEL PRODIST concluida com sucesso.",
        "result": result
    }

@router.get("/perdas-mmgd/status")
def get_perdas_mmgd_ingestion_status():
    """Retorna o status da ultima execucao do pipeline ANEEL Perdas & MMGD."""
    return aneel_perdas_mmgd_ingestor.last_status

@router.post("/perdas-mmgd/run")
def trigger_perdas_mmgd_ingestion(background_tasks: BackgroundTasks = None):
    """
    Dispara a ingestao e atualizacao dos dados de Perdas de Energia e MMGD da ANEEL (Lei 14.300).
    """
    result = aneel_perdas_mmgd_ingestor.run_pipeline()
    return {
        "message": "Ingestao ANEEL Perdas & MMGD concluida com sucesso.",
        "result": result
    }

@router.get("/datalake/status")
def get_datalake_status():
    """
    Retorna o status completo das 3 camadas do Data Lakehouse da ANEEL:
    - Camada Bronze: GCS Bucket
    - Camada Silver: Datasets e tabelas tratadas
    - Camada Gold: Tabelas analíticas de KPIs com aceleração BI Engine
    """
    from app.core.bigquery_client import bq_manager
    from app.core.config import settings

    status = {
        "project_id": settings.GCP_PROJECT_ID,
        "bronze_layer": {
            "storage_type": "Google Cloud Storage",
            "bucket": "gs://kpisetoreletrico-datalake-bronze",
            "status": "active",
            "domains": ["prodist", "mmgd", "tarifas_proret", "ouvidoria_iasc"]
        },
        "silver_layer": {
            "storage_type": "Google BigQuery",
            "dataset": "aneel_silver",
            "status": "healthy",
            "tables": {}
        },
        "gold_layer": {
            "storage_type": "Google BigQuery + BI Engine",
            "dataset": "gold_kpis",
            "status": "healthy",
            "bi_engine_accelerated": True,
            "tables": {}
        }
    }

    if bq_manager.client:
        try:
            # Silver counts
            for tbl in ["dec_fec_distribuidoras", "mmgd_instalacoes", "tarifas_homologadas", "ouvidoria_reclamacoes"]:
                try:
                    q = f"SELECT count(1) as total FROM `{settings.GCP_PROJECT_ID}.aneel_silver.{tbl}`"
                    r = list(bq_manager.client.query(q).result())
                    status["silver_layer"]["tables"][tbl] = r[0].total if r else 0
                except Exception:
                    status["silver_layer"]["tables"][tbl] = "pending"

            # Gold counts
            for tbl in ["kpi_dec_fec_conformidade", "kpi_mmgd_expansao_uf", "kpi_tarifas_ranking", "kpi_ouvidoria_satisfacao"]:
                try:
                    q = f"SELECT count(1) as total FROM `{settings.GCP_PROJECT_ID}.gold_kpis.{tbl}`"
                    r = list(bq_manager.client.query(q).result())
                    status["gold_layer"]["tables"][tbl] = r[0].total if r else 0
                except Exception:
                    status["gold_layer"]["tables"][tbl] = "pending"
        except Exception as e:
            status["error"] = str(e)

    return status

