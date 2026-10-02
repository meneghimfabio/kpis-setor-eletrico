---
type: Attested Computation
title: Top 5 Melhores Concessionárias no Índice IASC
description: Consulta atestada de referência para `kpi_ouvidoria_satisfacao`.
tags: [golden-query, kpi_ouvidoria_satisfacao, gold_kpis]
status: stable
runtime: bigquery
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:diretoria.regulatoria@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Top 5 Melhores Concessionárias no Índice IASC

Esta consulta SQL é certificada como a forma padrão e otimizada de responder perguntas executivas sobre `kpi_ouvidoria_satisfacao`:

```sql
SELECT distribuidora, score_iasc, ranking_iasc, tempo_medio_resolucao_dias, classificacao_satisfacao FROM `kpisetoreletrico.gold_kpis.kpi_ouvidoria_satisfacao` WHERE score_iasc IS NOT NULL ORDER BY score_iasc DESC LIMIT 5;
```
