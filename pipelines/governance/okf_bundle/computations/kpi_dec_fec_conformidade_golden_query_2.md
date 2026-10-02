---
type: Attested Computation
title: Distribuição de Concessionárias por Status Regulatório
description: Consulta atestada de referência para `kpi_dec_fec_conformidade`.
tags: [golden-query, kpi_dec_fec_conformidade, gold_kpis]
status: stable
runtime: bigquery
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:26:04Z
verified:
  by: human:diretoria.regulatoria@empresa.com.br
  at: 2026-10-02T20:26:04Z
---

# Distribuição de Concessionárias por Status Regulatório

Esta consulta SQL é certificada como a forma padrão e otimizada de responder perguntas executivas sobre `kpi_dec_fec_conformidade`:

```sql
SELECT status_regulatorio, COUNT(1) AS total_concessionarias, ROUND(SUM(compensacao_estimada_rs_mm), 2) AS compensacao_total_estimada_rs_mm FROM `kpisetoreletrico.gold_kpis.kpi_dec_fec_conformidade` GROUP BY status_regulatorio ORDER BY total_concessionarias DESC;
```
