---
type: Attested Computation
title: Ranking de Rentabilidade Operacional (Margem EBITDA) no Setor Elétrico
description: Consulta atestada de referência para `kpi_financeiro_dre_empresas`.
tags: [golden-query, kpi_financeiro_dre_empresas, gold_kpis]
status: stable
runtime: bigquery
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:diretoria.regulatoria@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Ranking de Rentabilidade Operacional (Margem EBITDA) no Setor Elétrico

Esta consulta SQL é certificada como a forma padrão e otimizada de responder perguntas executivas sobre `kpi_financeiro_dre_empresas`:

```sql
SELECT empresa, ticker, segmento, receita_liquida_rs_mm, ebitda_rs_mm, margem_ebitda_pct, alavancagem FROM `kpisetoreletrico.gold_kpis.kpi_financeiro_dre_empresas` WHERE ebitda_rs_mm > 0 ORDER BY margem_ebitda_pct DESC;
```
