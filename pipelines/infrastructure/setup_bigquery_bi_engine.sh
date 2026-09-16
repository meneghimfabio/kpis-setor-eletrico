#!/bin/bash
set -e

PROJECT_ID=${GCP_PROJECT_ID:-"kpisetoreletrico"}
LOCATION="us-central1"
CAPACITY_GB=${1:-2} # 2 GB de reserva inicial

echo "=== Configurando Reserva do BigQuery BI Engine ==="
echo "Projeto: $PROJECT_ID"
echo "Localização: $LOCATION"
echo "Capacidade: ${CAPACITY_GB} GB"

# Habilita reserva do BI Engine usando bq CLI
bq update \
    --project_id=$PROJECT_ID \
    --bi_reservation_size=${CAPACITY_GB} \
    --location=$LOCATION || {
    echo "Tentando criação de reserva do BI Engine via gcloud bi-engine..."
    gcloud alpha bq bi-engine reservations create \
        --project=$PROJECT_ID \
        --location=$LOCATION \
        --size=${CAPACITY_GB} || echo "Reserva BI Engine pode ser configurada diretamente no BigQuery Studio > Admin > BI Engine."
}

echo "=== BI Engine configurado para aceleração em memória! ==="
