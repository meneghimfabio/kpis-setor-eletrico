---
type: Table
title: Tabela kpi_atendimento_canais
description: Indicadores de atendimento telefônico e call center das distribuidoras conforme exigências da REN ANEEL 1.000/2021. Monitora o Índice de Nível de Serviço (INS - chamadas atendidas em até 30s), Índice de Abandono (IAb) e Tempo Médio de Atendimento (TMA).
resource: bigquery:kpisetoreletrico.gold_kpis.kpi_atendimento_canais
tags: [gold_kpis, kpi_atendimento_canais, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `kpi_atendimento_canais`

**Dataset:** [gold_kpis](../datasets/gold_kpis.md)  
**Recurso:** `bigquery:kpisetoreletrico.gold_kpis.kpi_atendimento_canais`

### Descrição Executiva
Indicadores de atendimento telefônico e call center das distribuidoras conforme exigências da REN ANEEL 1.000/2021. Monitora o Índice de Nível de Serviço (INS - chamadas atendidas em até 30s), Índice de Abandono (IAb) e Tempo Médio de Atendimento (TMA).

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `distribuidora` | Código regulatório da distribuidora perante a ANEEL. |
| `nome_concessionaria` | Nome oficial da concessionária. |
| `ins_pct` | Índice de Nível de Serviço: percentual de chamadas telefônicas atendidas pelo operador humano em até 30 segundos (meta >= 85%). |
| `iab_pct` | Índice de Abandono: percentual de chamadas em espera que foram abandonadas pelo consumidor antes do atendimento (tolerância <= 2%). |
| `tma_s` | Tempo Médio de Atendimento em segundos durante o diálogo com o operador. |
| `chamadas_totais` | Volume consolidado de ligações recebidas no canal de call center no mês. |
| `status_ins` | Conformidade regulatória do INS ('Conforme' vs 'Não Conforme'). |
| `status_iab` | Conformidade regulatória do índice de abandono. |
| `status_geral` | Status consolidado de excelência operacional nos canais de atendimento. |
| `data_referencia` | Mês de referência dos registros de teleatendimento. |
| `data_processamento` | Data de consolidação dos dados no BigQuery. |
