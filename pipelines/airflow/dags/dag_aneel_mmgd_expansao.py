"""
DAG Airflow para Ingestão e Processamento de Micro e Minigeração Distribuída (MMGD - Lei 14.300) da ANEEL.
Camadas: Bronze (GCS) -> Silver (BigQuery) -> Gold (Dataform/BigQuery).
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
}

def task_extract_mmgd_bronze_silver(**context):
    from pipelines.ingestion.aneel_mmgd_ingestor import run_mmgd_pipeline
    result = run_mmgd_pipeline()
    print(f"Resultado Ingestão MMGD: {result}")
    return result

def task_transform_gold_mmgd(**context):
    from pipelines.dataform.run_transformations import get_bigquery_client, SQL_MMGD
    client = get_bigquery_client()
    print("Atualizando Camada Gold kpi_mmgd_expansao_uf...")
    job = client.query(SQL_MMGD)
    job.result()
    print("Camada Gold MMGD atualizada com sucesso.")

with DAG(
    dag_id="dag_aneel_mmgd_expansao",
    default_args=default_args,
    description="Pipeline ANEEL MMGD: Coleta empreendimentos de GD, grava no GCS Bronze, limpa no Silver e agrega no Gold",
    schedule_interval="0 3 * * 1", # Toda segunda-feira às 03:00 AM UTC
    start_date=datetime.datetime(2026, 1, 1),
    catchup=False,
    tags=["aneel", "mmgd", "lei_14300", "bronze", "silver", "gold"]
) as dag:

    start = EmptyOperator(task_id="inicio")

    extract_bronze_silver = PythonOperator(
        task_id="extrair_mmgd_bronze_silver",
        python_callable=task_extract_mmgd_bronze_silver
    )

    transform_gold = PythonOperator(
        task_id="transformar_gold_kpi_mmgd",
        python_callable=task_transform_gold_mmgd
    )

    end = EmptyOperator(task_id="concluido")

    start >> extract_bronze_silver >> transform_gold >> end
