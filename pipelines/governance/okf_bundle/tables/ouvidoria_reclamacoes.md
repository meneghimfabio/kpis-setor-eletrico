---
type: Table
title: Tabela ouvidoria_reclamacoes
description: Registros de ouvidoria setorial da ANEEL e pesquisas de satisfação residencial do IASC.
resource: bigquery:kpisetoreletrico.aneel_silver.ouvidoria_reclamacoes
tags: [aneel_silver, ouvidoria_reclamacoes, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `ouvidoria_reclamacoes`

**Dataset:** [aneel_silver](../datasets/aneel_silver.md)  
**Recurso:** `bigquery:kpisetoreletrico.aneel_silver.ouvidoria_reclamacoes`

### Descrição Executiva
Registros de ouvidoria setorial da ANEEL e pesquisas de satisfação residencial do IASC.

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `distribuidora` | Sigla da concessionária. |
| `data_referencia` | Mês de referência das reclamações. |
| `score_iasc` | Nota obtida no Índice ANEEL de Satisfação do Consumidor (0-100). |
| `ranking_iasc` | Posição no ranking nacional de satisfação. |
| `total_reclamacoes` | Total de reclamações recebidas no período. |
| `procedencia_pct` | Percentual de procedência em favor do consumidor. |
| `tempo_medio_resolucao_dias` | Média de dias para resposta e saneamento. |
| `cumprimento_sla_pct` | Taxa de cumprimento do prazo regulatório de resposta. |
