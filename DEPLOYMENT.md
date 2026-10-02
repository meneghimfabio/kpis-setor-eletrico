# Guia de Deploy & Infraestrutura Cloud ☁️

Este documento descreve como realizar o deploy do **Painel do Setor Elétrico Brasileiro** e de suas pipelines de dados no **Google Cloud Platform (GCP)**.

---

## 🏗️ Pré-requisitos no Google Cloud

1. **Projeto GCP Ativo**:
   - Projeto padrão: `kpisetoreletrico`
   - Região padrão: `us-central1`

2. **APIs Necessárias Habilitadas**:
   ```bash
   gcloud services enable \
     bigquery.googleapis.com \
     storage.googleapis.com \
     run.googleapis.com \
     cloudbuild.googleapis.com \
     dataform.googleapis.com \
     composer.googleapis.com \
     artifactregistry.googleapis.com
   ```

3. **Autenticação CLI**:
   ```bash
   gcloud auth login
   gcloud config set project kpisetoreletrico
   gcloud auth application-default login
   ```

---

## 1. Deploy da Infraestrutura de Dados (Lakehouse)

Execute os scripts automatizados disponíveis em `pipelines/infrastructure/`:

### A. Bucket Bronze no Google Cloud Storage
```bash
bash pipelines/infrastructure/setup_gcs_buckets.sh
```
- Cria o bucket `gs://kpisetoreletrico-datalake-bronze`
- Configura regras de ciclo de vida (transição para Nearline após 90 dias).

### B. Aceleração BigQuery BI Engine
```bash
bash pipelines/infrastructure/setup_bigquery_bi_engine.sh
```
- Reserva 1 GB a 10 GB de memória in-memory na região `us-central1` para responder consultas da camada Gold em milissegundos.

### C. Orquestrador Cloud Composer 3 / Apache Airflow
```bash
bash pipelines/infrastructure/setup_composer_env.sh
```
- Provisiona o ambiente Composer 3 e sincroniza as DAGs de `pipelines/airflow/dags/`.

---

## 2. Deploy da Aplicação Fullstack no Google Cloud Run

A aplicação utiliza um **Dockerfile multi-stage** que compila o frontend React/Vite com Node 22 e o serve em conjunto com o backend FastAPI em Python 3.11.

### Opção A: Deploy Direto via Cloud Build & Cloud Run
```bash
gcloud run deploy kpis-setor-eletrico \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars GCP_PROJECT_ID=kpisetoreletrico \
  --memory 1Gi \
  --cpu 1 \
  --min-instances 0 \
  --max-instances 5
```

### Opção B: Build Local com Docker
```bash
# 1. Build da imagem
docker build -t kpis-setor-eletrico:latest .

# 2. Execução local do container
docker run -p 8080:8080 \
  -e GCP_PROJECT_ID=kpisetoreletrico \
  -v ~/.config/gcloud:/root/.config/gcloud \
  kpis-setor-eletrico:latest
```
Acesse a aplicação em: `http://localhost:8080`.
