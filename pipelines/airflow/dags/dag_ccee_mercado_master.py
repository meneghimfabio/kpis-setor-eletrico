"""
DAG Airflow: Orquestração Diária do Mercado CCEE & ONS.
Executa a cadeia Medallion:
1. Ingestão Live CCEE e ONS (Bronze GCS -> Silver BigQuery)
2. Transformação e cálculo de spread/risco para a Camada Gold (kpi_ccee_mercado_resumo)
3. Validação de qualidade de dados (Data Quality Assertions)
"""
import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator

default_args = {
    "owner": "kpisetoreletrico",
    "depends_on_past": False,
    "retries": 2,
    "retry_delay": datetime.timedelta(minutes=5),
    "email_on_failure": False,
}

def extract_ccee_live_task(**context):
    from pipelines.ingestion.ccee_live_ingestor import ccee_live_ingestor
    res = ccee_live_ingestor.run_pipeline()
    if res.get("status") != "success":
        raise RuntimeError(f"Falha na ingestão CCEE Live: {res.get('error')}")
    return res

def transform_gold_ccee_task(**context):
    from pipelines.dataform.run_transformations import get_bigquery_client, PROJECT_ID, SQL_CCEE
    client = get_bigquery_client()
    job = client.query(SQL_CCEE)
    job.result()
    print("Tabela Gold kpi_ccee_mercado_resumo materializada com sucesso.")

def validate_quality_ccee_task(**context):
    from pipelines.dataform.run_transformations import get_bigquery_client, PROJECT_ID
    client = get_bigquery_client()
    sql = f"SELECT count(1) as total FROM `{PROJECT_ID}.gold_kpis.kpi_ccee_mercado_resumo`"
    rows = list(client.query(sql).result())
    count = rows[0].total if rows else 0
    if count == 0:
        raise ValueError("Alerta de Qualidade: Tabela Gold kpi_ccee_mercado_resumo vazia após execução!")
    print(f"Data Quality Check CCEE OK: {count} registros consolidados.")
    return {"records_gold": count}

with DAG(
    dag_id="dag_ccee_mercado_master",
    default_args=default_args,
    description="Pipeline Diário Live de Mercado CCEE (PLD, Curtailment, GSF, ESS) -> Gold Lakehouse",
    schedule_interval="0 6 * * *", # Todos os dias às 06:00 UTC (03:00 BRT)
    start_date=datetime.datetime(2025, 1, 1),
    catchup=False,
    tags=["ccee", "mercado", "pld", "lakehouse", "gold"],
) as dag:

    start = EmptyOperator(task_id="start_ccee_pipeline")

    ingest_live = PythonOperator(
        task_id="ingest_ccee_live_bronze_silver",
        python_callable=extract_ccee_live_task,
    )

    transform_gold = PythonOperator(
        task_id="transform_gold_ccee_mercado",
        python_callable=transform_gold_ccee_task,
    )

    validate_quality = PythonOperator(
        task_id="validate_quality_ccee_gold",
        python_callable=validate_quality_ccee_task,
    )

    end = EmptyOperator(task_id="end_ccee_pipeline")

    start >> ingest_live >> transform_gold >> validate_quality >> end
