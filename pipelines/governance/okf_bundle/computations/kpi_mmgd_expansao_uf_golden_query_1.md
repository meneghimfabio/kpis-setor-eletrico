---
type: Attested Computation
title: Top 5 Estados em Capacidade Instalada de MMGD (MW)
description: Consulta atestada de referência para `kpi_mmgd_expansao_uf`.
tags: [golden-query, kpi_mmgd_expansao_uf, gold_kpis]
status: stable
runtime: bigquery
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:diretoria.regulatoria@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Top 5 Estados em Capacidade Instalada de MMGD (MW)

Esta consulta SQL é certificada como a forma padrão e otimizada de responder perguntas executivas sobre `kpi_mmgd_expansao_uf`:

```sql
SELECT sigla_uf, subsistema, total_conexoes, potencia_instalada_mw, market_share_nacional_pct FROM `kpisetoreletrico.gold_kpis.kpi_mmgd_expansao_uf` ORDER BY potencia_instalada_mw DESC LIMIT 5;
```
