# 🏛️ Documentação de Arquitetura da Solução

Este documento detalha a arquitetura técnica, de dados, de computação e de segurança da plataforma **Painel do Setor Elétrico Brasileiro & Data Lakehouse ANEEL**, implantada em ambiente produtivo no **Google Cloud Platform (GCP)**.

O diagrama de arquitetura oficial editável está disponível em [`docs/architecture.drawio`](architecture.drawio).

---

## 📐 Visão Geral da Arquitetura (Swimlanes End-to-End)

O sistema é desenhado segundo o padrão de raias corporativas do Google Cloud, dividindo o fluxo de dados em 5 domínios fundamentais:

```
┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐   ┌─────────────────┐
│   1. FONTES     │   │  2. INGESTÃO &  │   │ 3. LAKEHOUSE    │   │  4. SERVING &   │   │ 5. CLIENTES &   │
│   EXTERNAS      │──>│  ORQUESTRAÇÃO   │──>│    MEDALLION    │──>│    COMPUTAÇÃO   │──>│   GOVERNANÇA    │
│  (ANEEL/ONS)    │   │(Scheduler/Run)  │   │  (GCS/BigQuery) │   │   (Cloud Run)   │   │ (C-Level & BI)  │
└─────────────────┘   └─────────────────┘   └─────────────────┘   └─────────────────┘   └─────────────────┘
```

---

## 🎨 Como Abrir e Editar o Diagrama no Draw.io / diagrams.net

Você pode abrir, inspecionar e editar o arquivo [`docs/architecture.drawio`](architecture.drawio) de três formas simples:

1. **No Navegador (Sem Instalação):**
   - Acesse [app.diagrams.net](https://app.diagrams.net/).
   - Clique em **Open Existing Diagram** (Abrir Diagrama Existente) e selecione o arquivo `docs/architecture.drawio` deste repositório.
2. **No VS Code:**
   - Instale a extensão **Draw.io Integration** (`hediet.vscode-drawio`).
   - Clique no arquivo `docs/architecture.drawio` para editar diretamente dentro do editor com interface gráfica interativa.
3. **No Draw.io Desktop:**
   - Baixe a versão desktop oficial em [draw.io](https://www.drawio.com/) e abra o arquivo nativamente.

---

## 🔍 Detalhamento das 5 Raias de Arquitetura

### Raia 1: Fontes Externas de Dados (Regulatório & Mercado)
- **ANEEL (Agência Nacional de Energia Elétrica):**
  - **PRODIST Módulo 8:** Indicadores de continuidade coletivos (DEC e FEC) por conjunto e distribuidora, limites regulatórios e compensações financeiras apuradas. Formato: Parquet oficial (28.8 MB).
  - **SISGD (Lei 14.300):** Base de empreendimentos de micro e minigeração distribuída, potência instalada (kW/MW), tecnologia (fotovoltaica/solar, biomassa, PCH) e municípios/UFs. Formato: Parquet oficial (100.7 MB).
  - **PRORET (Tarifas Homologadas):** Estrutura tarifária (TE - Tarifa de Energia e TUSD - Tarifa de Uso do Sistema de Distribuição) das 103 distribuidoras concessionárias para classes B1 (Residencial), B2 (Rural), B3 (Comercial) e Grupo A (A4 Industrial). Formato: CSV oficial (84.9 MB).
  - **Ouvidoria & IASC:** Volume de reclamações de Nível 2 escaladas à Ouvidoria Setorial da ANEEL, tempos médios de resposta e notas do Prêmio IASC de satisfação do consumidor residencial.
- **ONS (Operador Nacional do Sistema Elétrico):**
  - Energia Armazenada (EAR %), Energia Natural Afluente (ENA % MLT), Custo Marginal de Operação (CMO) e despacho térmico/hidro por subsistema (SE/CO, Sul, Nordeste, Norte).
- **CCEE (Câmara de Comercialização de Energia Elétrica):**
  - Preço de Liquidação das Diferenças (PLD Horário), GSF (Generation Scaling Factor / Risco Hidrológico), Encargos de Serviço do Sistema (ESS) e acionamento de Bandeiras Tarifárias.

---

### Raia 2: Ingestão & Orquestração (Serverless FinOps vs Enterprise)

A arquitetura adota um modelo de **orquestração dual**:

#### A. Orquestrador Ativo em Produção: Google Cloud Scheduler (Custo R$ 0,00)
Para manter o custo de infraestrutura em zero e eliminar o consumo de clusters ociosos, utilizamos o Cloud Scheduler para disparar chamadas HTTP POST com autenticação segura via **OIDC Token**:
- **`aneel-datalake-master-diario`**: Execução diária às 23:00 BRT (`0 23 * * *`) disparando `/api/v1/ingestion/datalake/run`. Executa a ingestão simultânea dos 4 domínios, consolida a camada Gold e executa asserções de qualidade de dados.
- **`aneel-mmgd-semanal`**: Toda segunda-feira às 00:00 BRT (`0 0 * * 1`) disparando `/api/v1/ingestion/datalake/mmgd/run`.
- **`aneel-tarifas-mensal`**: Dia 01 do mês às 02:00 BRT (`0 2 1 * *`) disparando `/api/v1/ingestion/datalake/tarifas/run`.
- **`aneel-prodist-mensal`**: Dia 05 do mês às 01:00 BRT (`0 1 5 * *`) disparando `/api/v1/ingestion/datalake/prodist/run`.
- **`aneel-ouvidoria-mensal`**: Dia 10 do mês às 03:00 BRT (`0 3 10 * *`) disparando `/api/v1/ingestion/datalake/ouvidoria/run`.

#### B. Opção Enterprise: Cloud Composer 3 / Apache Airflow
Para empresas que exigem console visual do Airflow, gráficos de Gantt e retries em nível de nó:
- DAGs prontas em `pipelines/airflow/dags/`: [`dag_aneel_datalake_master.py`](file:///Users/meneghimfabio/jetski/KPIs%20do%20Setor%20Eletrico/pipelines/airflow/dags/dag_aneel_datalake_master.py).
- Script de provisionamento idempotente: [`setup_composer_env.sh`](file:///Users/meneghimfabio/jetski/KPIs%20do%20Setor%20Eletrico/pipelines/infrastructure/setup_composer_env.sh).

---

### Raia 3: Data Lakehouse Medallion (GCS & BigQuery)

```
[Raw Parquet/CSV] ──> gs://kpisetoreletrico-datalake-bronze (Bronze)
                             │
                             ▼ (Carga tipada, deduplicação & MERGE)
                      aneel_silver (Silver BigQuery)
                             │
                             ▼ (Transformação analítica SQLX & Assertions)
                      gold_kpis + BigQuery BI Engine (Gold 2 GB In-Memory)
```

1. **Camada Bronze (Google Cloud Storage):**
   - Bucket: `gs://kpisetoreletrico-datalake-bronze`
   - Armazenamento particionado por diretórios temporais: `aneel/<dominio>/ano=YYYY/mes=MM/`
   - Políticas de Lifecycle: Migração automática de `Standard` ➔ `Nearline` (30 dias) ➔ `Coldline` (90 dias).
2. **Camada Silver (Google BigQuery - `aneel_silver`):**
   - `dec_fec_distribuidoras`: Particionado por `data_referencia`, clustered por `distribuidora`. Carga via `MERGE` garantindo idempotência.
   - `mmgd_instalacoes`: Particionado por `data_conexao`, clustered por `sig_uf, sig_modalidade`.
   - `tarifas_homologadas`: Particionado por `ano_homologacao`, clustered por `sig_agente, classe`.
   - `ouvidoria_reclamacoes`: Particionado por `data_referencia`, clustered por `distribuidora`.
3. **Camada Gold (Google BigQuery - `gold_kpis`) com Aceleração BI Engine:**
   - Tabelas analíticas agregadas com KPIs prontos para consumo:
     - `kpi_dec_fec_conformidade`: Horas de interrupção (DEC) e frequência (FEC) reais vs limites anuais regulatórios.
     - `kpi_mmgd_expansao_uf`: Potência acumulada (MW) e evolução da autogeração solar nas 27 UFs.
     - `kpi_tarifas_ranking`: Preço médio homologado (TE + TUSD) residencial e industrial.
     - `kpi_ouvidoria_satisfacao`: Índices IASC e SLAs comerciais.
   - **BigQuery BI Engine:** Reserva de memória ativa de **2 GB** provisionada na região `us-central1`, permitindo que as consultas analíticas do dashboard sejam resolvidas em menos de 200 ms sem disparar full scans no BigQuery.

---

### Raia 4: Serviços & Computação (Google Cloud Run)

- **Instância Serverless em Produção:**
  - URL Oficial: `https://kpis-setor-eletrico-623774526601.us-central1.run.app`
  - Revisão: `kpis-setor-eletrico-00002-z2f`
  - Specs: 1 vCPU, 1 GiB RAM, Concorrência de 80 requisições simultâneas, Timeout de 300 segundos, Scale-to-Zero.
- **Backend FastAPI (Python 3.11):**
  - Servidor assíncrono Uvicorn com documentação OpenAPI Swagger (`/docs`).
  - Endpoints analíticos com retorno em sub-segundo via cliente BigQuery.
  - Simulador tarifário com cálculos paramétricos de faturas (B1 vs A4, impacto de ICMS, PIS/COFINS e tarifas de injeção da Lei 14.300).
- **Frontend Single Page Application (React 18 + Vite + TailwindCSS):**
  - Empacotado via Docker multi-stage build (Node.js 22 para build do SPA ➔ Python 3.11 para servir assets estáticos em `/app/static`).
  - Gráficos responsivos de alta performance com Recharts e ícones setoriais com Lucide Icons.

---

### Raia 5: Consumidores, Segurança & Governança

1. **Perfis de Usuários:**
   - **C-Level & Diretorias:** Acesso a dashboards consolidados com alertas de conformidade regulatória.
   - **Engenheiros de Distribuição:** Diagnóstico aprofundado de conjuntos elétricos com violação de DEC/FEC.
   - **Gestores de Energia & Consultores:** Simulação de viabilidade econômica de projetos de GD solar e migração para o Mercado Livre (ACL).
2. **Matriz de Identidade & Acesso (Google Cloud IAM):**
   - Service Account: `623774526601-compute@developer.gserviceaccount.com`
   - Papéis aplicados (Least Privilege):
     - `roles/bigquery.dataViewer` (leitura dos datasets `aneel_silver` e `gold_kpis`)
     - `roles/bigquery.user` (capacidade de submeter jobs de query)
     - `roles/storage.objectAdmin` (escrita e leitura no bucket Bronze)
3. **FinOps & Otimização de Custos:**
   - **Cloud Run:** Zero instâncias quando não há tráfego (Scale-to-Zero). Custo base: **R$ 0,00** dentro do free tier.
   - **Cloud Scheduler:** Até 3 jobs gratuitos por conta; jobs adicionais custam apenas $0,10/mês. Custo base: **R$ 0,00**.
   - **BigQuery BI Engine:** Reserva de 2 GB acelerando todas as queries sem custo de bytes faturados repetidos.
   - **Armazenamento GCS & BQ:** Menos de 1 GB de dados totais compactados em Parquet colunar (centavos por mês).
   - **Custo mensal estimado da infraestrutura completa: ~R$ 0,00 a R$ 5,00/mês.**
