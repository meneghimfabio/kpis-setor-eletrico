---
type: Attested Computation
title: Top 5 Tarifas Mais Caras do Brasil
description: Consulta atestada de referência para `kpi_tarifas_ranking`.
tags: [golden-query, kpi_tarifas_ranking, gold_kpis]
status: stable
runtime: bigquery
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:diretoria.regulatoria@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Top 5 Tarifas Mais Caras do Brasil

Esta consulta SQL é certificada como a forma padrão e otimizada de responder perguntas executivas sobre `kpi_tarifas_ranking`:

```sql
SELECT distribuidora, concessionaria, uf, tarifa_b1_rs_kwh, share_tusd_fio_pct, share_te_energia_pct FROM `kpisetoreletrico.gold_kpis.kpi_tarifas_ranking` ORDER BY tarifa_b1_rs_kwh DESC LIMIT 5;
```
