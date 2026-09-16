# 🌊 Data Lakehouse ANEEL: Bronze, Silver & Gold

Pipeline de engenharia de dados corporativo para coleta, padronização e disponibilização de dados regulatórios e de mercado da **ANEEL** (Agência Nacional de Energia Elétrica), utilizando a arquitetura Medallion no **Google Cloud Platform (GCP)**.

Projeto GCP: **`kpisetoreletrico`**  
Região: **`us-central1`**

---

## 🏛️ Arquitetura em 3 Camadas

```
  [APIs & Dados Abertos ANEEL]
       │
       │ (1) Ingestão Python / Airflow PythonOperator
       ▼
 ┌─────────────────────────────────────────────────────────────┐
 │  CAMADA BRONZE (Google Cloud Storage)                       │
 │  Bucket: gs://kpisetoreletrico-datalake-bronze/             │
 │  • aneel/prodist/.../indicadores_dec_fec_raw.parquet (28.8MB)│
 │  • aneel/mmgd/.../mmgd_empreendimentos_raw.parquet (100.7MB)│
 │  • aneel/tarifas_proret/.../tarifas_homologadas_raw.csv(84.9MB)
 │  • aneel/ouvidoria_iasc/.../manifestacoes_distribuidoras_raw.parquet (25.4MB)
 │  • aneel/ouvidoria_iasc/.../indice_aneel_satisfacao_consumidor_raw.csv (3.2MB)
 └─────────────────────────────────────────────────────────────┘
       │
       │ (2) Carga, Tipagem & MERGE Incremental
       ▼
 ┌─────────────────────────────────────────────────────────────┐
 │  CAMADA SILVER (Google BigQuery)                            │
 │  Dataset: kpisetoreletrico.aneel_silver                     │
 │  • dec_fec_distribuidoras (Particionado por data_referencia)│
 │  • mmgd_instalacoes       (Particionado por data_referencia)│
 │  • tarifas_homologadas    (Particionado por ano)            │
 │  • ouvidoria_reclamacoes  (Particionado por data_referencia)│
 └─────────────────────────────────────────────────────────────┘
       │
       │ (3) Transformação SQLX & Assertions de Qualidade (Dataform)
       ▼
 ┌─────────────────────────────────────────────────────────────┐
 │  CAMADA GOLD (Google BigQuery + BI Engine)                  │
 │  Dataset: kpisetoreletrico.gold_kpis                        │
 │  • kpi_dec_fec_conformidade (Métricas vs Limite ANEEL)      │
 │  • kpi_mmgd_expansao_uf     (Potência MW e ranking por UF)  │
 │  • kpi_tarifas_ranking      (Multiclasse B1/B2/B3 e Demanda/Energia A4)│
 │  • kpi_ouvidoria_satisfacao (Scores IASC e SLAs comerciais) │
 └─────────────────────────────────────────────────────────────┘
       │
       │ (4) Consultas SQL Otimizadas (Sub-segundo via BI Engine)
       ▼
 ┌─────────────────────────────────────────────────────────────┐
 │  BACKEND (FastAPI) & FRONTEND (React / Vite)                │
 │  • Endpoints com metadados de procedência (_metadata)       │
 │  • Monitoramento em tempo real: /api/v1/ingestion/datalake/status
 └─────────────────────────────────────────────────────────────┘
```

---

## 📂 Estrutura de Pastas

```
pipelines/
├── infrastructure/
│   ├── setup_gcs_buckets.sh       # Criação do bucket GCS Bronze e ciclo de vida
│   ├── setup_bigquery_bi_engine.sh # Ativação da reserva de memória do BI Engine
│   └── setup_composer_env.sh      # Provisionamento e deploy no Cloud Composer 3
├── ingestion/
│   ├── gcp_client.py              # Utilitário de autenticação e upload GCS/BQ
│   ├── aneel_prodist_ingestor.py  # Ingestão de DEC/FEC (Parquet oficial)
│   ├── aneel_mmgd_ingestor.py     # Ingestão de GD / SISGD (Lei 14.300)
│   ├── aneel_tarifas_ingestor.py  # Ingestão de Tarifas Homologadas (PRORET)
│   └── aneel_ouvidoria_ingestor.py# Ingestão de Ouvidoria e IASC
├── airflow/
│   └── dags/
│       ├── dag_aneel_prodist_dec_fec.py # Orquestração Mensal PRODIST
│       ├── dag_aneel_mmgd_expansao.py   # Orquestração Semanal MMGD
│       ├── dag_aneel_tarifas_proret.py  # Orquestração Mensal Tarifas
│       └── dag_aneel_ouvidoria_iasc.py  # Orquestração Mensal Ouvidoria
└── dataform/
    ├── workflow_settings.yaml     # Configuração do projeto Dataform no GCP
    ├── run_transformations.py     # Executor de compilação Silver -> Gold
    └── definitions/
        ├── sources/
        │   └── declarations_silver.sqlx # Mapeamento das fontes Silver
        └── gold/
            ├── kpi_dec_fec_conformidade.sqlx # Modelo Gold DEC/FEC
            ├── kpi_mmgd_expansao_uf.sqlx     # Modelo Gold MMGD
            ├── kpi_tarifas_ranking.sqlx      # Modelo Gold Tarifas
            └── kpi_ouvidoria_satisfacao.sqlx # Modelo Gold Ouvidoria
```

---

## 🚀 Como Executar

### 1. Rodar a Ingestão Completa (Bronze -> Silver)
```bash
# A partir da raiz do projeto:
PYTHONPATH=. ./backend/venv/bin/python -c "
from pipelines.ingestion.aneel_prodist_ingestor import run_prodist_pipeline
from pipelines.ingestion.aneel_mmgd_ingestor import run_mmgd_pipeline
from pipelines.ingestion.aneel_tarifas_ingestor import run_tarifas_pipeline
from pipelines.ingestion.aneel_ouvidoria_ingestor import run_ouvidoria_pipeline

run_prodist_pipeline()
run_mmgd_pipeline()
run_tarifas_pipeline()
run_ouvidoria_pipeline()
"
```

### 2. Rodar as Transformações (Silver -> Gold)
```bash
PYTHONPATH=. ./backend/venv/bin/python pipelines/dataform/run_transformations.py
```

### 3. Verificar o Status das 3 Camadas via API
Acesse:
`http://localhost:8000/api/v1/ingestion/datalake/status` ou em produção no Cloud Run.

Retorno esperado:
```json
{
  "project_id": "kpisetoreletrico",
  "bronze_layer": {
    "storage_type": "Google Cloud Storage",
    "bucket": "gs://kpisetoreletrico-datalake-bronze",
    "status": "active"
  },
  "silver_layer": {
    "storage_type": "Google BigQuery",
    "dataset": "aneel_silver",
    "status": "healthy",
    "tables": {
      "dec_fec_distribuidoras": 340,
      "mmgd_instalacoes": 96,
      "tarifas_homologadas": 10,
      "ouvidoria_reclamacoes": 10
    }
  },
  "gold_layer": {
    "storage_type": "Google BigQuery + BI Engine",
    "dataset": "gold_kpis",
    "status": "healthy",
    "bi_engine_accelerated": true,
    "tables": {
      "kpi_dec_fec_conformidade": 11,
      "kpi_mmgd_expansao_uf": 12,
      "kpi_tarifas_ranking": 10,
      "kpi_ouvidoria_satisfacao": 10
    }
  }
}
```

---

## ⚡ BigQuery BI Engine

Para ativar ou ajustar a capacidade de aceleração em memória:
```bash
./pipelines/infrastructure/setup_bigquery_bi_engine.sh 2 # 2 GB
```

---

## ☁️ Deploy no Cloud Composer (Apache Airflow)

Quando desejar provisionar o ambiente Composer e sincronizar as DAGs:
```bash
./pipelines/infrastructure/setup_composer_env.sh
```
