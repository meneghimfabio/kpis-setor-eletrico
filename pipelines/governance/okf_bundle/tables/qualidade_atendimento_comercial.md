---
type: Table
title: Tabela qualidade_atendimento_comercial
description: Indicadores de qualidade de atendimento telefônico e cumprimento dos prazos comerciais da REN ANEEL 1.000/2021.
resource: bigquery:kpisetoreletrico.aneel_silver.qualidade_atendimento_comercial
tags: [aneel_silver, qualidade_atendimento_comercial, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `qualidade_atendimento_comercial`

**Dataset:** [aneel_silver](../datasets/aneel_silver.md)  
**Recurso:** `bigquery:kpisetoreletrico.aneel_silver.qualidade_atendimento_comercial`

### Descrição Executiva
Indicadores de qualidade de atendimento telefônico e cumprimento dos prazos comerciais da REN ANEEL 1.000/2021.

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `distribuidora` | Código da distribuidora perante a ANEEL. |
| `nome_concessionaria` | Razão social da empresa de distribuição. |
| `ins_pct` | Índice de Nível de Serviço do atendimento telefônico (meta >= 85%). |
| `iab_pct` | Índice de abandono de chamadas no call center (tolerância <= 2%). |
| `tma_s` | Tempo Médio de Atendimento em segundos. |
| `chamadas_totais` | Total de chamadas registradas. |
| `servico` | Nome do serviço comercial avaliado. |
| `sigla_indicador` | Sigla técnica do indicador comercial. |
| `artigo_ren_1000` | Artigo da REN 1.000/2021 que estipula o padrão. |
| `unidade_sla` | Unidade do prazo legal (Horas ou Dias Úteis). |
| `sla_regulatorio_valor` | Valor nominal do limite legal de prazo. |
| `tempo_medio_real` | Tempo médio real medido para atendimento. |
| `cumprimento_pct` | Percentual de pedidos concluídos no prazo regulamentar. |
| `total_solicitacoes` | Volume de requisições de serviço. |
| `solicitacoes_violadas` | Volume de requisições atendidas com descumprimento de prazo. |
| `compensacao_paga_rs_mm` | Valor financeiro pago em compensações aos clientes (R$ Milhões). |
| `status` | Classificação do serviço. |
| `status_geral` | Diagnóstico geral de conformidade. |
| `data_referencia` | Mês da apuração. |
