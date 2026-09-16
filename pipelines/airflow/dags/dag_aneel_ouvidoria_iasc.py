"""
DAG Airflow para Ingestão e Processamento de Ouvidoria, Reclamações e Índice IASC da ANEEL.
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

def task_extract_ouvidoria_bronze_silver(**context):
    from pipelines.ingestion.aneel_ouvidoria_ingestor import run_ouvidoria_pipeline
    result = run_ouvidoria_pipeline()
    print(f"Resultado Ingestão Ouvidoria: {result}")
    return result

def task_transform_gold_ouvidoria(**context):
    from pipelines.dataform.run_transformations import get_bigquery_client, SQL_OUVIDORIA
    client = get_bigquery_client()
    print("Atualizando Camada Gold kpi_ouvidoria_satisfacao...")
    job = client.query(SQL_OUVIDORIA)
    job.result()
    print("Camada Gold Ouvidoria atualizada com sucesso.")

with DAG(
    dag_id="dag_aneel_ouvidoria_iasc",
    default_args=default_args,
    description="Pipeline ANEEL Ouvidoria & IASC: Coleta reclamações, grava no GCS Bronze, limpa no Silver e agrega no Gold",
    schedule_interval="0 6 10 * *", # Todo dia 10 do mês às 06:00 AM UTC
    start_date=datetime.datetime(2026, 1, 1),
    catchup=False,
    tags=["aneel", "ouvidoria", "iasc", "satisfacao", "bronze", "silver", "gold"]
) as dag:

    start = EmptyOperator(task_id="inicio")

    extract_bronze_silver = PythonOperator(
        task_id="extrair_ouvidoria_bronze_silver",
        python_callable=task_extract_ouvidoria_bronze_silver
    )

    transform_gold = PythonOperator(
        task_id="transformar_gold_kpi_ouvidoria",
        python_callable=task_transform_gold_ouvidoria
    )

    end = EmptyOperator(task_id="concluido")

    start >> extract_bronze_silver >> transform_gold >> end
