---
type: Attested Computation
title: Top 10 Distribuidoras com Maior Extrapolação de DEC
description: Consulta atestada de referência para `kpi_dec_fec_conformidade`.
tags: [golden-query, kpi_dec_fec_conformidade, gold_kpis]
status: stable
runtime: bigquery
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:diretoria.regulatoria@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Top 10 Distribuidoras com Maior Extrapolação de DEC

Esta consulta SQL é certificada como a forma padrão e otimizada de responder perguntas executivas sobre `kpi_dec_fec_conformidade`:

```sql
SELECT distribuidora, sigla_uf, dec_apurado_horas, dec_limite_aneel_horas, desvio_dec_horas, percentual_ultrapassagem_dec, compensacao_estimada_rs_mm FROM `kpisetoreletrico.gold_kpis.kpi_dec_fec_conformidade` WHERE NOT conformidade_dec ORDER BY desvio_dec_horas DESC LIMIT 10;
```
