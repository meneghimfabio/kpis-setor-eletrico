---
type: Table
title: Tabela ena_historico
description: Série histórica de Energia Natural Afluente (ENA) e afluências hídricas por subsistema (ONS).
resource: bigquery:kpisetoreletrico.operacao_sin.ena_historico
tags: [operacao_sin, ena_historico, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `ena_historico`

**Dataset:** [operacao_sin](../datasets/operacao_sin.md)  
**Recurso:** `bigquery:kpisetoreletrico.operacao_sin.ena_historico`

### Descrição Executiva
Série histórica de Energia Natural Afluente (ENA) e afluências hídricas por subsistema (ONS).

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `data_referencia` | Data de consolidação das afluências. |
| `subsistema` | Subsistema eletroenergético. |
| `ena_mwmed` | Volume afluente em Megawatts médios. |
| `ena_percentual_mlt` | Afluência em relação à Média de Longo Termo histórica (% MLT). |
| `classificacao_hidrologica` | Classificação: Seca Severa, Moderada, Normal ou Úmido. |
