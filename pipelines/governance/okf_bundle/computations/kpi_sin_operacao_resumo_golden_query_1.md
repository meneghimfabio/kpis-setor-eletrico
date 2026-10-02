---
type: Attested Computation
title: Balanço Atual de Segurança Hídrica e CMO por Subsistema
description: Consulta atestada de referência para `kpi_sin_operacao_resumo`.
tags: [golden-query, kpi_sin_operacao_resumo, gold_kpis]
status: stable
runtime: bigquery
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:26:04Z
verified:
  by: human:diretoria.regulatoria@empresa.com.br
  at: 2026-10-02T20:26:04Z
---

# Balanço Atual de Segurança Hídrica e CMO por Subsistema

Esta consulta SQL é certificada como a forma padrão e otimizada de responder perguntas executivas sobre `kpi_sin_operacao_resumo`:

```sql
SELECT subsistema, ear_percentual, meta_seguranca_percentual, folga_seguranca_ear_pct, ena_percentual_mlt, cmo_medio_rs_mwh, status_seguranca_energetica FROM `kpisetoreletrico.gold_kpis.kpi_sin_operacao_resumo` ORDER BY folga_seguranca_ear_pct ASC;
```
