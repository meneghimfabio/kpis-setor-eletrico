---
type: Attested Computation
title: Transmissoras com Menor Taxa de Desconto de PVd sobre RAP
description: Consulta atestada de referência para `kpi_transmissao_concessoes`.
tags: [golden-query, kpi_transmissao_concessoes, gold_kpis]
status: stable
runtime: bigquery
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:diretoria.regulatoria@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Transmissoras com Menor Taxa de Desconto de PVd sobre RAP

Esta consulta SQL é certificada como a forma padrão e otimizada de responder perguntas executivas sobre `kpi_transmissao_concessoes`:

```sql
SELECT sigla, holding, rap_homologada_rs_mm, pvd_rs_mm, pvd_sobre_rap_pct, disponibilidade_pct FROM `kpisetoreletrico.gold_kpis.kpi_transmissao_concessoes` ORDER BY pvd_sobre_rap_pct ASC LIMIT 5;
```
