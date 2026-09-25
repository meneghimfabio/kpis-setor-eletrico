"""
DAG Airflow Mestre: Orquestração Unificada Diária do Data Lakehouse ANEEL.
Executa a cadeia Medallion completa:
1. Ingestão paralela dos 4 domínios da ANEEL (Bronze GCS -> Silver BigQuery)
2. Transformação e agregação analítica para os KPIs da Camada Gold (BigQuery + BI Engine)
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

def extract_prodist_task(**context):
    from pipelines.ingestion.aneel_prodist_ingestor import run_prodist_pipeline
    execution_date = context.get("execution_date", datetime.datetime.now())
    year = execution_date.year
    return run_prodist_pipeline(years=[year, year - 1])

def extract_mmgd_task(**context):
    from pipelines.ingestion.aneel_mmgd_ingestor import run_mmgd_pipeline
    return run_mmgd_pipeline()

def extract_tarifas_task(**context):
    from pipelines.ingestion.aneel_tarifas_ingestor import run_tarifas_pipeline
    return run_tarifas_pipeline()

def extract_ouvidoria_task(**context):
    from pipelines.ingestion.aneel_ouvidoria_ingestor import run_ouvidoria_pipeline
    return run_ouvidoria_pipeline()

def transform_gold_task(**context):
    from pipelines.dataform.run_transformations import run_gold_transformations
    return run_gold_transformations()

def validate_quality_task(**context):
    from pipelines.dataform.run_transformations import get_bigquery_client, PROJECT_ID
    client = get_bigquery_client()
    checks = [
        ("kpi_dec_fec_conformidade", "SELECT count(1) as total FROM `{}.gold_kpis.kpi_dec_fec_conformidade`"),
        ("kpi_mmgd_expansao_uf", "SELECT count(1) as total FROM `{}.gold_kpis.kpi_mmgd_expansao_uf`"),
        ("kpi_tarifas_ranking", "SELECT count(1) as total FROM `{}.gold_kpis.kpi_tarifas_ranking`"),
        ("kpi_ouvidoria_satisfacao", "SELECT count(1) as total FROM `{}.gold_kpis.kpi_ouvidoria_satisfacao`"),
    ]
    report = {}
    for name, sql in checks:
        query = sql.format(PROJECT_ID)
        rows = list(client.query(query).result())
        count = rows[0].total if rows else 0
        report[name] = count
        if count == 0:
            raise ValueError(f"Alerta de Qualidade: Tabela Gold '{name}' vazia após execução do pipeline!")
    print(f"Data Quality Check concluído com sucesso: {report}")
    return report

with DAG(
    dag_id="dag_aneel_datalake_master",
    default_args=default_args,
    description="DAG Mestre do Data Lakehouse ANEEL: Ingestão paralela Bronze/Silver, transformação Gold e validação de qualidade",
    schedule_interval="0 2 * * *", # Execução Diária às 02:00 AM UTC (23:00 BRT)
    start_date=datetime.datetime(2026, 1, 1),
    catchup=False,
    tags=["aneel", "datalake", "master", "medallion", "bronze", "silver", "gold"]
) as dag:

    inicio = EmptyOperator(task_id="inicio")

    # Ingestão paralela dos 4 domínios ANEEL (Bronze -> Silver)
    ingest_prodist = PythonOperator(
        task_id="ingestao_prodist_qualidade",
        python_callable=extract_prodist_task
    )

    ingest_mmgd = PythonOperator(
        task_id="ingestao_mmgd_solar",
        python_callable=extract_mmgd_task
    )

    ingest_tarifas = PythonOperator(
        task_id="ingestao_tarifas_proret",
        python_callable=extract_tarifas_task
    )

    ingest_ouvidoria = PythonOperator(
        task_id="ingestao_ouvidoria_iasc",
        python_callable=extract_ouvidoria_task
    )

    barreira_silver = EmptyOperator(task_id="barreira_camada_silver")

    # Transformação unificada para a Camada Gold (BigQuery + BI Engine)
    transform_gold = PythonOperator(
        task_id="transformacao_camada_gold",
        python_callable=transform_gold_task
    )

    # Validação de Qualidade de Dados (Sanity check)
    validar_qualidade = PythonOperator(
        task_id="validacao_qualidade_gold",
        python_callable=validate_quality_task
    )

    concluido = EmptyOperator(task_id="concluido")

    # Orquestração do Grafo de Dependências
    inicio >> [ingest_prodist, ingest_mmgd, ingest_tarifas, ingest_ouvidoria] >> barreira_silver
    barreira_silver >> transform_gold >> validar_qualidade >> concluido
