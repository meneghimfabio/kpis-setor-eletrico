#!/bin/bash
set -e

PROJECT_ID=${GCP_PROJECT_ID:-"kpisetoreletrico"}
REGION="us-central1"
ENV_NAME="composer-kpisetoreletrico"

echo "=== Orquestração do Cloud Composer 3 / Apache Airflow ==="
echo "Projeto: $PROJECT_ID"
echo "Região: $REGION"
echo "Ambiente: $ENV_NAME"

# 1. Habilitar APIs necessárias
echo "Habilitando APIs do Composer e Cloud Build..."
CLOUDSDK_METRICS_ENVIRONMENT=datacloud.jetski gcloud services enable composer.googleapis.com cloudbuild.googleapis.com --project=$PROJECT_ID

# 2. Criar ambiente Composer 3 se não existir
if ! CLOUDSDK_METRICS_ENVIRONMENT=datacloud.jetski gcloud composer environments describe $ENV_NAME --location=$REGION --project=$PROJECT_ID >/dev/null 2>&1; then
    echo "Provisionando ambiente Cloud Composer 3 (Small)..."
    CLOUDSDK_METRICS_ENVIRONMENT=datacloud.jetski gcloud composer environments create $ENV_NAME \
        --location=$REGION \
        --project=$PROJECT_ID \
        --image-version="composer-3-airflow-2" \
        --environment-size=small \
        --env-variables="GCP_PROJECT_ID=$PROJECT_ID,GCS_BRONZE_BUCKET=kpisetoreletrico-datalake-bronze,BQ_LOCATION=$REGION" \
        --labels=datacloud=jetski
    echo "Ambiente Composer provisionado com sucesso!"
else
    echo "Ambiente Composer $ENV_NAME já está ativo."
fi

# 3. Obter o Bucket de DAGs do Composer
DAGS_BUCKET=$(CLOUDSDK_METRICS_ENVIRONMENT=datacloud.jetski gcloud composer environments describe $ENV_NAME --location=$REGION --project=$PROJECT_ID --format="value(config.dagGcsPrefix)")
echo "Bucket de DAGs do Composer: $DAGS_BUCKET"

# 4. Sincronizar DAGs e módulos dependentes (pipelines) para o Composer
echo "Sincronizando DAGs e código Python de ingestão/transformação..."
CLOUDSDK_METRICS_ENVIRONMENT=datacloud.jetski gcloud storage cp pipelines/airflow/dags/*.py "$DAGS_BUCKET/"
CLOUDSDK_METRICS_ENVIRONMENT=datacloud.jetski gcloud storage cp -r pipelines/ingestion "$DAGS_BUCKET/pipelines/"
CLOUDSDK_METRICS_ENVIRONMENT=datacloud.jetski gcloud storage cp -r pipelines/dataform "$DAGS_BUCKET/pipelines/"
CLOUDSDK_METRICS_ENVIRONMENT=datacloud.jetski gcloud storage cp pipelines/__init__.py "$DAGS_BUCKET/pipelines/__init__.py"

# 5. Instalar pacotes adicionais do Python (PyPI) no Composer se necessário
if [ -f "pipelines/airflow/requirements-composer.txt" ]; then
    echo "Verificando dependências PyPI no Cloud Composer..."
    CLOUDSDK_METRICS_ENVIRONMENT=datacloud.jetski gcloud composer environments update $ENV_NAME \
        --location=$REGION \
        --project=$PROJECT_ID \
        --update-pypi-packages-from-file="pipelines/airflow/requirements-composer.txt" || true
fi

echo "=== Sincronização e Orquestração do Cloud Composer 3 Finalizada! ==="
echo "Para disparar manualmente a DAG mestre:"
echo "gcloud composer environments run $ENV_NAME --location=$REGION dags trigger -- dag_aneel_datalake_master"
