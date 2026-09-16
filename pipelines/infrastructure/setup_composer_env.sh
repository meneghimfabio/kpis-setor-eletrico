#!/bin/bash
set -e

PROJECT_ID=${GCP_PROJECT_ID:-"kpisetoreletrico"}
REGION="us-central1"
ENV_NAME="composer-kpisetoreletrico"

echo "=== Automação do Cloud Composer 3 (GCP) ==="
echo "Projeto: $PROJECT_ID"
echo "Região: $REGION"
echo "Ambiente: $ENV_NAME"

# 1. Habilitar APIs necessárias
echo "Habilitando APIs do Composer e Cloud Build..."
gcloud services enable composer.googleapis.com cloudbuild.googleapis.com --project=$PROJECT_ID

# 2. Criar ambiente Composer 3 se não existir
if ! gcloud composer environments describe $ENV_NAME --location=$REGION --project=$PROJECT_ID >/dev/null 2>&1; then
    echo "Criando ambiente Cloud Composer 3 (Small)..."
    gcloud composer environments create $ENV_NAME \
        --location=$REGION \
        --project=$PROJECT_ID \
        --image-version="composer-3-airflow-2" \
        --environment-size=small \
        --env-variables="GCP_PROJECT_ID=$PROJECT_ID,GCS_BRONZE_BUCKET=kpisetoreletrico-datalake-bronze,BQ_LOCATION=$REGION"
    echo "Ambiente Composer criado com sucesso!"
else
    echo "Ambiente Composer $ENV_NAME já existe."
fi

# 3. Obter o Bucket de DAGs do Composer
DAGS_BUCKET=$(gcloud composer environments describe $ENV_NAME --location=$REGION --project=$PROJECT_ID --format="value(config.dagGcsPrefix)")
echo "Bucket de DAGs do Composer: $DAGS_BUCKET"

# 4. Sincronizar DAGs locais com o Composer
echo "Sincronizando DAGs para o Composer..."
gcloud storage rsync pipelines/airflow/dags/ "$DAGS_BUCKET" --recursive

echo "=== Sincronização do Cloud Composer finalizada! ==="
