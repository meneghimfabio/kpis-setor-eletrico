---
type: Attested Computation
title: Último PLD por Submercado e Spread Máximo Regional
description: Consulta atestada de referência para `kpi_ccee_mercado_resumo`.
tags: [golden-query, kpi_ccee_mercado_resumo, gold_kpis]
status: stable
runtime: bigquery
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:diretoria.regulatoria@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Último PLD por Submercado e Spread Máximo Regional

Esta consulta SQL é certificada como a forma padrão e otimizada de responder perguntas executivas sobre `kpi_ccee_mercado_resumo`:

```sql
SELECT subsistema, pld_rs_mwh, pld_teto_rs_mwh, spread_maximo_regional_rs_mwh, status_integracao_sin FROM `kpisetoreletrico.gold_kpis.kpi_ccee_mercado_resumo` ORDER BY pld_rs_mwh DESC;
```
