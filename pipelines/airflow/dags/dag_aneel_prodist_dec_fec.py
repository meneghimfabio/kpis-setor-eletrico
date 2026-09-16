"""
DAG Airflow para Ingestão e Processamento Contínuo de Dados de Qualidade da Distribuição (PRODIST DEC/FEC) da ANEEL.
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
    "email_on_failure": False,
}

def task_extract_prodist_bronze_silver(**context):
    from pipelines.ingestion.aneel_prodist_ingestor import run_prodist_pipeline
    execution_date = context.get("execution_date", datetime.datetime.now())
    year = execution_date.year
    result = run_prodist_pipeline(years=[year, year - 1])
    print(f"Resultado Ingestão PRODIST: {result}")
    return result

def task_transform_gold_dec_fec(**context):
    from pipelines.dataform.run_transformations import get_bigquery_client, SQL_DEC_FEC, PROJECT_ID
    client = get_bigquery_client()
    print("Atualizando Camada Gold kpi_dec_fec_conformidade...")
    job = client.query(SQL_DEC_FEC)
    job.result()
    print("Camada Gold atualizada com sucesso.")

with DAG(
    dag_id="dag_aneel_prodist_dec_fec",
    default_args=default_args,
    description="Pipeline ANEEL PRODIST DEC/FEC: Coleta dados abertos, grava no GCS Bronze, limpa no Silver e agrega no Gold",
    schedule_interval="0 4 5 * *", # Todo dia 5 do mês às 04:00 AM UTC
    start_date=datetime.datetime(2026, 1, 1),
    catchup=False,
    tags=["aneel", "prodist", "dec_fec", "bronze", "silver", "gold"]
) as dag:

    start = EmptyOperator(task_id="inicio")

    extract_bronze_silver = PythonOperator(
        task_id="extrair_prodist_bronze_silver",
        python_callable=task_extract_prodist_bronze_silver
    )

    transform_gold = PythonOperator(
        task_id="transformar_gold_kpi_dec_fec",
        python_callable=task_transform_gold_dec_fec
    )

    end = EmptyOperator(task_id="concluido")

    start >> extract_bronze_silver >> transform_gold >> end
