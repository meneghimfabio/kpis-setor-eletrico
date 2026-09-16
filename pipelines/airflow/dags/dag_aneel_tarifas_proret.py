"""
DAG Airflow para Ingestão e Processamento de Tarifas Homologadas (PRORET - TE/TUSD) da ANEEL.
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

def task_extract_tarifas_bronze_silver(**context):
    from pipelines.ingestion.aneel_tarifas_ingestor import run_tarifas_pipeline
    result = run_tarifas_pipeline()
    print(f"Resultado Ingestão Tarifas: {result}")
    return result

def task_transform_gold_tarifas(**context):
    from pipelines.dataform.run_transformations import get_bigquery_client, SQL_TARIFAS
    client = get_bigquery_client()
    print("Atualizando Camada Gold kpi_tarifas_ranking...")
    job = client.query(SQL_TARIFAS)
    job.result()
    print("Camada Gold Tarifas atualizada com sucesso.")

with DAG(
    dag_id="dag_aneel_tarifas_proret",
    default_args=default_args,
    description="Pipeline ANEEL Tarifas: Coleta resoluções homologatórias, grava no GCS Bronze, limpa no Silver e agrega no Gold",
    schedule_interval="0 5 1 * *", # Todo dia 1 do mês às 05:00 AM UTC
    start_date=datetime.datetime(2026, 1, 1),
    catchup=False,
    tags=["aneel", "tarifas", "proret", "bronze", "silver", "gold"]
) as dag:

    start = EmptyOperator(task_id="inicio")

    extract_bronze_silver = PythonOperator(
        task_id="extrair_tarifas_bronze_silver",
        python_callable=task_extract_tarifas_bronze_silver
    )

    transform_gold = PythonOperator(
        task_id="transformar_gold_kpi_tarifas",
        python_callable=task_transform_gold_tarifas
    )

    end = EmptyOperator(task_id="concluido")

    start >> extract_bronze_silver >> transform_gold >> end
