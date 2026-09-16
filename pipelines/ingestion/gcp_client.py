import os
import io
import logging
import subprocess
from typing import Optional
from google.cloud import bigquery
from google.oauth2 import credentials

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("datalake_gcp_client")

PROJECT_ID = os.getenv("GCP_PROJECT_ID", "kpisetoreletrico")
BRONZE_BUCKET = os.getenv("GCS_BRONZE_BUCKET", "kpisetoreletrico-datalake-bronze")
LOCATION = os.getenv("BQ_LOCATION", "us-central1")

def get_gcp_credentials():
    """Obtém credenciais padrão ou fallback via gcloud print-access-token."""
    try:
        token = subprocess.check_output(["gcloud", "auth", "print-access-token"], timeout=10).decode().strip().split()[-1]
        return credentials.Credentials(token)
    except Exception as e:
        logger.warning(f"Não foi possível obter token via gcloud: {e}. Usando credenciais padrão.")
        return None

def get_bigquery_client() -> bigquery.Client:
    creds = get_gcp_credentials()
    if creds:
        return bigquery.Client(project=PROJECT_ID, credentials=creds)
    return bigquery.Client(project=PROJECT_ID)

def upload_to_bronze_gcs(data_bytes: bytes, destination_blob_name: str, content_type: str = "application/octet-stream") -> str:
    """Faz upload de arquivo bruto para a camada Bronze no GCS usando gcloud storage."""
    uri = f"gs://{BRONZE_BUCKET}/{destination_blob_name}"
    logger.info(f"Subindo {len(data_bytes)/1024/1024:.2f} MB para {uri}...")
    try:
        proc = subprocess.Popen(
            ["gcloud", "storage", "cp", "-", uri],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        stdout, stderr = proc.communicate(input=data_bytes)
        if proc.returncode != 0:
            logger.error(f"Erro no upload via gcloud storage: {stderr.decode()}")
            raise RuntimeError(f"gcloud storage failed: {stderr.decode()}")
        logger.info(f"Upload concluído com sucesso para: {uri}")
        return uri
    except Exception as e:
        logger.error(f"Falha no upload para {uri}: {e}")
        raise e

def upload_file_to_bronze_gcs(local_file_path: str, destination_blob_name: str) -> str:
    """Faz upload de arquivo local diretamente para a camada Bronze no GCS usando gcloud storage."""
    uri = f"gs://{BRONZE_BUCKET}/{destination_blob_name}"
    file_size_mb = os.path.getsize(local_file_path) / 1024 / 1024
    logger.info(f"Subindo arquivo {local_file_path} ({file_size_mb:.2f} MB) para {uri}...")
    try:
        res = subprocess.run(
            ["gcloud", "storage", "cp", local_file_path, uri],
            capture_output=True,
            text=True,
            check=True
        )
        logger.info(f"Upload concluído com sucesso para: {uri}")
        return uri
    except subprocess.CalledProcessError as e:
        logger.error(f"Erro no upload via gcloud storage: {e.stderr}")
        raise RuntimeError(f"gcloud storage failed: {e.stderr}")

