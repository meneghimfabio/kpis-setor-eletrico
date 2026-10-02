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
            "domains": ["prodist", "mmgd", "tarifas_proret", "ouvidoria_iasc", "cvm_dfp_itr", "transmissao", "atendimento_comercial"]
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
            for tbl in ["dec_fec_distribuidoras", "mmgd_instalacoes", "tarifas_homologadas", "ouvidoria_reclamacoes", "cvm_dre_empresas", "desempenho_transmissao", "qualidade_atendimento_comercial"]:
                try:
                    q = f"SELECT count(1) as total FROM `{settings.GCP_PROJECT_ID}.aneel_silver.{tbl}`"
                    r = list(bq_manager.client.query(q).result())
                    status["silver_layer"]["tables"][tbl] = r[0].total if r else 0
                except Exception:
                    status["silver_layer"]["tables"][tbl] = "pending"

            # Gold counts
            for tbl in ["kpi_dec_fec_conformidade", "kpi_mmgd_expansao_uf", "kpi_tarifas_ranking", "kpi_ouvidoria_satisfacao", "kpi_financeiro_dre_empresas", "kpi_transmissao_concessoes", "kpi_atendimento_slas_comerciais", "kpi_atendimento_canais"]:
                try:
                    q = f"SELECT count(1) as total FROM `{settings.GCP_PROJECT_ID}.gold_kpis.{tbl}`"
                    r = list(bq_manager.client.query(q).result())
                    status["gold_layer"]["tables"][tbl] = r[0].total if r else 0
                except Exception:
                    status["gold_layer"]["tables"][tbl] = "pending"
        except Exception as e:
            status["error"] = str(e)

    return status


def run_datalake_master_pipeline():
    """Executa a cadeia Medallion completa: Ingestao 7 dominios (ANEEL + CVM) -> Gold -> Quality Check."""
    from pipelines.ingestion.aneel_prodist_ingestor import run_prodist_pipeline
    from pipelines.ingestion.aneel_mmgd_ingestor import run_mmgd_pipeline
    from pipelines.ingestion.aneel_tarifas_ingestor import run_tarifas_pipeline
    from pipelines.ingestion.aneel_ouvidoria_ingestor import run_ouvidoria_pipeline
    from pipelines.ingestion.cvm_dre_ingestor import run_cvm_pipeline
    from pipelines.ingestion.aneel_transmissao_ingestor import run_transmissao_pipeline
    from pipelines.ingestion.aneel_comercial_ingestor import run_comercial_pipeline
    from pipelines.dataform.run_transformations import run_gold_transformations, get_bigquery_client, PROJECT_ID
    
    results = {}
    results["prodist"] = run_prodist_pipeline()
    results["mmgd"] = run_mmgd_pipeline()
    results["tarifas"] = run_tarifas_pipeline()
    results["ouvidoria"] = run_ouvidoria_pipeline()
    results["cvm_dre"] = run_cvm_pipeline()
    results["transmissao"] = run_transmissao_pipeline()
    results["atendimento_comercial"] = run_comercial_pipeline()
    results["gold"] = run_gold_transformations()
    
    # Assertions de Qualidade
    client = get_bigquery_client()
    checks = [
        ("kpi_dec_fec_conformidade", f"SELECT count(1) as total FROM `{PROJECT_ID}.gold_kpis.kpi_dec_fec_conformidade`"),
        ("kpi_mmgd_expansao_uf", f"SELECT count(1) as total FROM `{PROJECT_ID}.gold_kpis.kpi_mmgd_expansao_uf`"),
        ("kpi_tarifas_ranking", f"SELECT count(1) as total FROM `{PROJECT_ID}.gold_kpis.kpi_tarifas_ranking`"),
        ("kpi_ouvidoria_satisfacao", f"SELECT count(1) as total FROM `{PROJECT_ID}.gold_kpis.kpi_ouvidoria_satisfacao`"),
        ("kpi_financeiro_dre_empresas", f"SELECT count(1) as total FROM `{PROJECT_ID}.gold_kpis.kpi_financeiro_dre_empresas`"),
        ("kpi_transmissao_concessoes", f"SELECT count(1) as total FROM `{PROJECT_ID}.gold_kpis.kpi_transmissao_concessoes`"),
        ("kpi_atendimento_slas_comerciais", f"SELECT count(1) as total FROM `{PROJECT_ID}.gold_kpis.kpi_atendimento_slas_comerciais`"),
    ]
    quality = {}
    for name, query in checks:
        try:
            rows = list(client.query(query).result())
            cnt = rows[0].total if rows else 0
            quality[name] = cnt
        except Exception as e:
            quality[name] = f"error: {str(e)}"
    results["quality_check"] = quality
    return results


@router.post("/datalake/run")
def trigger_datalake_master(background_tasks: BackgroundTasks = None, async_mode: bool = False):
    """
    Dispara a orquestracao unificada do Data Lakehouse ANEEL + CVM:
    Ingestao paralela dos 5 dominios (Bronze -> Silver), transformacao Gold e validacao de integridade.
    Ideal para agendamento serverless via Google Cloud Scheduler.
    """
    if async_mode and background_tasks:
        background_tasks.add_task(run_datalake_master_pipeline)
        return {"status": "processing", "message": "Pipeline Data Lakehouse ANEEL + CVM iniciado em background."}
    
    try:
        results = run_datalake_master_pipeline()
        return {"status": "success", "message": "Pipeline Data Lakehouse ANEEL + CVM concluido com sucesso.", "results": results}
    except Exception as e:
        return {"status": "error", "message": f"Erro na execucao do pipeline: {str(e)}"}


@router.get("/cvm/status")
def get_cvm_ingestion_status():
    """Retorna o status da ultima execucao do pipeline CVM DFP/ITR."""
    from pipelines.ingestion.cvm_dre_ingestor import cvm_ingestor
    return cvm_ingestor.last_status


@router.post("/cvm/run")
def trigger_cvm_ingestion(background_tasks: BackgroundTasks = None, async_mode: bool = False):
    """
    Dispara a ingestao dos dados de demonstrativos contabeis auditados da CVM (DFP/ITR).
    Extrai Receita Liquida, EBITDA, Margem EBITDA, Lucro Liquido, Divida Liquida e CAPEX.
    """
    from pipelines.ingestion.cvm_dre_ingestor import run_cvm_pipeline
    if async_mode and background_tasks:
        background_tasks.add_task(run_cvm_pipeline)
        return {"status": "processing", "message": "Ingestao CVM DFP/ITR iniciada em background."}
    result = run_cvm_pipeline()
    return {"message": "Ingestao CVM DFP/ITR concluida com sucesso.", "result": result}


@router.post("/datalake/cvm/run")
def trigger_datalake_cvm():
    """Ingestao especifica de CVM DFP/ITR (Bronze -> Silver -> Gold)."""
    from pipelines.ingestion.cvm_dre_ingestor import run_cvm_pipeline
    return run_cvm_pipeline()


@router.post("/datalake/prodist/run")
def trigger_datalake_prodist():
    """Ingestao especifica de PRODIST DEC/FEC (Bronze -> Silver)."""
    from pipelines.ingestion.aneel_prodist_ingestor import run_prodist_pipeline
    return run_prodist_pipeline()


@router.post("/datalake/mmgd/run")
def trigger_datalake_mmgd():
    """Ingestao especifica de MMGD (Bronze -> Silver)."""
    from pipelines.ingestion.aneel_mmgd_ingestor import run_mmgd_pipeline
    return run_mmgd_pipeline()


@router.post("/datalake/tarifas/run")
def trigger_datalake_tarifas():
    """Ingestao especifica de Tarifas Homologadas (Bronze -> Silver)."""
    from pipelines.ingestion.aneel_tarifas_ingestor import run_tarifas_pipeline
    return run_tarifas_pipeline()


@router.post("/datalake/ouvidoria/run")
def trigger_datalake_ouvidoria():
    """Ingestao especifica de Ouvidoria & IASC (Bronze -> Silver)."""
    from pipelines.ingestion.aneel_ouvidoria_ingestor import run_ouvidoria_pipeline
    return run_ouvidoria_pipeline()


@router.post("/datalake/gold/run")
def trigger_datalake_gold():
    """Transformacao analitica das tabelas Silver para a Camada Gold."""
    from pipelines.dataform.run_transformations import run_gold_transformations
    return run_gold_transformations()


@router.post("/datalake/transmissao/run")
def trigger_datalake_transmissao():
    """Ingestao especifica de Transmissao CKAN - RAP e PVd (Bronze -> Silver -> Gold)."""
    from pipelines.ingestion.aneel_transmissao_ingestor import run_transmissao_pipeline
    return run_transmissao_pipeline()


@router.post("/datalake/comercial/run")
def trigger_datalake_comercial():
    """Ingestao especifica de Atendimento Comercial e SLAs REN 1.000/2021 (Bronze -> Silver -> Gold)."""
    from pipelines.ingestion.aneel_comercial_ingestor import run_comercial_pipeline
    return run_comercial_pipeline()
