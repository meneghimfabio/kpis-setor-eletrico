#!/bin/bash
# ==============================================================================
# Setup Google Cloud Knowledge Catalog (Dataplex) - Setor Elétrico
# Criação de Aspect Types, Entry Groups e Filesets para o Lakehouse ANEEL
# ==============================================================================

set -euo pipefail

PROJECT_ID="${GCP_PROJECT_ID:-kpisetoreletrico}"
LOCATION="${GCP_REGION:-us-central1}"
ENTRY_GROUP_ID="aneel-lakehouse-bronze"
ASPECT_TYPE_ID="governanca_setor_eletrico"
BUCKET_NAME="kpisetoreletrico-datalake-bronze"

echo "=============================================================================="
echo "Configurando Knowledge Catalog no projeto: ${PROJECT_ID} (${LOCATION})"
echo "=============================================================================="

# 1. Habilitar APIs necessárias
echo "[1/4] Verificando e habilitando APIs do Dataplex e Data Catalog..."
gcloud services enable \
  dataplex.googleapis.com \
  datacatalog.googleapis.com \
  datalineage.googleapis.com \
  bigquery.googleapis.com \
  storage.googleapis.com \
  --project="${PROJECT_ID}"

# 2. Criar Aspect Type customizado para Governança do Setor Elétrico
echo "[2/4] Criando/Atualizando Aspect Type: ${ASPECT_TYPE_ID}..."
cat << 'EOF' > /tmp/aspect_schema.json
{
  "fields": [
    {
      "name": "regulador_origem",
      "type": "string",
      "annotations": {
        "description": "Órgão regulador ou entidade setorial de origem (ex: ANEEL, CCEE, ONS, CVM)."
      }
    },
    {
      "name": "modulo_regulatorio",
      "type": "string",
      "annotations": {
        "description": "Fundamento regulatório (ex: PRODIST Módulo 8, PRORET, Lei 14.300/2022, REN 1.000/2021)."
      }
    },
    {
      "name": "periodicidade_atualizacao",
      "type": "string",
      "annotations": {
        "description": "Frequência de atualização dos dados (Diário, Semanal, Mensal, Anual)."
      }
    },
    {
      "name": "criticidade_c_level",
      "type": "string",
      "annotations": {
        "description": "Nível de criticidade executiva (Alta, Média, Baixa)."
      }
    },
    {
      "name": "data_owner",
      "type": "string",
      "annotations": {
        "description": "E-mail ou time responsável pela integridade dos dados."
      }
    }
  ]
}
EOF

if gcloud dataplex aspect-types describe "${ASPECT_TYPE_ID}" --location="${LOCATION}" --project="${PROJECT_ID}" &>/dev/null; then
  echo "Aspect Type ${ASPECT_TYPE_ID} já existe."
else
  gcloud dataplex aspect-types create "${ASPECT_TYPE_ID}" \
    --location="${LOCATION}" \
    --project="${PROJECT_ID}" \
    --schema-file="/tmp/aspect_schema.json" \
    --description="Aspecto de Governança e Conformidade Regulatória do Setor Elétrico Brasileiro"
  echo "✔️ Aspect Type ${ASPECT_TYPE_ID} criado com sucesso!"
fi
rm -f /tmp/aspect_schema.json

# 3. Criar Entry Group para a Camada Bronze (Google Cloud Storage)
echo "[3/4] Criando Entry Group para camada Bronze: ${ENTRY_GROUP_ID}..."
if gcloud dataplex entry-groups describe "${ENTRY_GROUP_ID}" --location="${LOCATION}" --project="${PROJECT_ID}" &>/dev/null; then
  echo "Entry Group ${ENTRY_GROUP_ID} já existe."
else
  gcloud dataplex entry-groups create "${ENTRY_GROUP_ID}" \
    --location="${LOCATION}" \
    --project="${PROJECT_ID}" \
    --description="Entry Group para arquivos brutos Parquet/CSV da Camada Bronze no GCS"
  echo "✔️ Entry Group ${ENTRY_GROUP_ID} criado com sucesso!"
fi

# 4. Criar Entry para os arquivos brutos da ANEEL no bucket GCS
echo "[4/4] Registrando Fileset Entry no Knowledge Catalog para gs://${BUCKET_NAME}..."
ENTRY_ID="aneel-bronze-fileset"

cat << EOF > /tmp/entry_definition.json
{
  "entryType": "projects/${PROJECT_ID}/locations/${LOCATION}/entryTypes/generic-fileset",
  "fullyQualifiedName": "dataplex:${PROJECT_ID}.${LOCATION}.${ENTRY_GROUP_ID}.${ENTRY_ID}",
  "userSpecifiedSystem": "Cloud Storage Bronze Lakehouse",
  "aspects": {
    "projects/${PROJECT_ID}/locations/${LOCATION}/aspectTypes/${ASPECT_TYPE_ID}": {
      "aspectType": "projects/${PROJECT_ID}/locations/${LOCATION}/aspectTypes/${ASPECT_TYPE_ID}",
      "data": {
        "regulador_origem": "ANEEL / CCEE / ONS",
        "modulo_regulatorio": "PRODIST, PRORET, SISGD, CCEE MCP",
        "periodicidade_atualizacao": "Diário e Mensal",
        "criticidade_c_level": "Alta",
        "data_owner": "engenharia-de-dados@empresa.com.br"
      }
    }
  }
}
EOF

echo "Definição do Fileset pronta em /tmp/entry_definition.json."
echo "Para aplicar a Entry via Dataplex API ou gcloud, use:"
echo "  gcloud dataplex entries create ${ENTRY_ID} --entry-group=${ENTRY_GROUP_ID} --location=${LOCATION} --project=${PROJECT_ID} --entry-file=/tmp/entry_definition.json"
echo ""
echo "✔️ Configuração dos Aspect Types e Entry Groups concluída!"
