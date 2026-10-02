#!/bin/bash
set -e

PROJECT_ID=${GCP_PROJECT_ID:-"kpisetoreletrico"}
REGION="us-central1"
SERVICE_NAME="kpis-setor-eletrico"

echo "=== Orquestração Serverless: Google Cloud Scheduler (Custo Zero / Free Tier) ==="
echo "Projeto: $PROJECT_ID"
echo "Região: $REGION"
echo "Serviço Cloud Run: $SERVICE_NAME"

# 1. Habilitar API do Cloud Scheduler
echo "Habilitando cloudscheduler.googleapis.com..."
CLOUDSDK_METRICS_ENVIRONMENT=datacloud.jetski gcloud services enable cloudscheduler.googleapis.com --project=$PROJECT_ID

# 2. Obter a URL do Cloud Run
SERVICE_URL=$(CLOUDSDK_METRICS_ENVIRONMENT=datacloud.jetski gcloud run services describe $SERVICE_NAME --region=$REGION --project=$PROJECT_ID --format="value(status.url)")
if [ -z "$SERVICE_URL" ]; then
    echo "Erro: Não foi possível obter a URL do serviço Cloud Run $SERVICE_NAME."
    exit 1
fi
echo "URL do Serviço Cloud Run: $SERVICE_URL"

# 3. Obter ou definir a Service Account para autenticação OIDC
SERVICE_ACCOUNT=$(CLOUDSDK_METRICS_ENVIRONMENT=datacloud.jetski gcloud run services describe $SERVICE_NAME --region=$REGION --project=$PROJECT_ID --format="value(spec.template.spec.serviceAccountName)")
if [ -z "$SERVICE_ACCOUNT" ]; then
    SERVICE_ACCOUNT="${PROJECT_ID}@appspot.gserviceaccount.com"
fi
echo "Service Account OIDC: $SERVICE_ACCOUNT"

# Função auxiliar para criar ou atualizar cron jobs no Cloud Scheduler
create_or_update_job() {
    local JOB_NAME=$1
    local SCHEDULE=$2
    local ENDPOINT=$3
    local DESCRIPTION=$4
    local TARGET_URL="${SERVICE_URL}${ENDPOINT}"

    echo "--- Configurando Job: $JOB_NAME ---"
    echo "Agendamento: '$SCHEDULE' | Endpoint: $ENDPOINT"

    if CLOUDSDK_METRICS_ENVIRONMENT=datacloud.jetski gcloud scheduler jobs describe "$JOB_NAME" --location=$REGION --project=$PROJECT_ID >/dev/null 2>&1; then
        echo "Job já existe. Atualizando configuração..."
        CLOUDSDK_METRICS_ENVIRONMENT=datacloud.jetski gcloud scheduler jobs update http "$JOB_NAME" \
            --location=$REGION \
            --project=$PROJECT_ID \
            --schedule="$SCHEDULE" \
            --time-zone="America/Sao_Paulo" \
            --uri="$TARGET_URL" \
            --http-method=POST \
            --oidc-service-account-email="$SERVICE_ACCOUNT" \
            --oidc-token-audience="$SERVICE_URL" \
            --description="$DESCRIPTION"
    else
        echo "Criando novo Job..."
        CLOUDSDK_METRICS_ENVIRONMENT=datacloud.jetski gcloud scheduler jobs create http "$JOB_NAME" \
            --location=$REGION \
            --project=$PROJECT_ID \
            --schedule="$SCHEDULE" \
            --time-zone="America/Sao_Paulo" \
            --uri="$TARGET_URL" \
            --http-method=POST \
            --oidc-service-account-email="$SERVICE_ACCOUNT" \
            --oidc-token-audience="$SERVICE_URL" \
            --description="$DESCRIPTION"
    fi
    echo "Job $JOB_NAME configurado com sucesso!"
}

# 4. Criação dos 5 Jobs de Agendamento (Fuso Horário: America/Sao_Paulo)

# 4.1 Master Diário: Ingestão 4 domínios + Gold + Data Quality
create_or_update_job \
    "aneel-datalake-master-diario" \
    "0 23 * * *" \
    "/api/v1/ingestion/datalake/run" \
    "Disparo diário da cadeia Medallion completa da ANEEL (Bronze -> Silver -> Gold + Quality Check)"

# 4.2 MMGD Semanal: Novas conexões de geração distribuída (Lei 14.300)
create_or_update_job \
    "aneel-mmgd-semanal" \
    "0 0 * * 1" \
    "/api/v1/ingestion/datalake/mmgd/run" \
    "Atualização semanal de micro e minigeração distribuída da ANEEL por UF"

# 4.3 Tarifas Mensal: Resoluções Homologatórias PRORET (Dia 1)
create_or_update_job \
    "aneel-tarifas-mensal" \
    "0 2 1 * *" \
    "/api/v1/ingestion/datalake/tarifas/run" \
    "Atualização mensal das tarifas homologadas (B1, B2, B3, A4) das distribuidoras"

# 4.4 PRODIST Mensal: DEC/FEC e Compensações (Dia 5)
create_or_update_job \
    "aneel-prodist-mensal" \
    "0 1 5 * *" \
    "/api/v1/ingestion/datalake/prodist/run" \
    "Atualização mensal dos indicadores de continuidade DEC/FEC e compensações financeiras"

# 4.5 Ouvidoria & IASC Mensal: Reclamações e Ranking de Satisfação (Dia 10)
create_or_update_job \
    "aneel-ouvidoria-mensal" \
    "0 3 10 * *" \
    "/api/v1/ingestion/datalake/ouvidoria/run" \
    "Atualização mensal das reclamações de Nível 2 na ANEEL e notas do Prêmio IASC"

# 4.6 Mercado CCEE Diário: PLD Horário, GSF, ESS e Curtailment (Todos os dias às 06:00 BRT)
create_or_update_job \
    "ccee-mercado-diario" \
    "0 6 * * *" \
    "/api/v1/ingestion/ccee/run" \
    "Atualização diária dos dados de Mercado CCEE e ONS (PLD, Curtailment, GSF, ESS)"

echo ""
echo "=== Todos os 6 Jobs do Cloud Scheduler foram configurados com sucesso! ==="
echo "Para listar todos os agendamentos ativos:"
echo "gcloud scheduler jobs list --location=$REGION --project=$PROJECT_ID"
echo ""
echo "Para testar manualmente o job CCEE imediatamente:"
echo "gcloud scheduler jobs run ccee-mercado-diario --location=$REGION --project=$PROJECT_ID"
