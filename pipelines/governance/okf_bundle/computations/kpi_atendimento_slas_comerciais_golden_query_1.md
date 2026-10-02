---
type: Attested Computation
title: Serviços Comerciais com Maior Volume de Violações e Compensações Pagas
description: Consulta atestada de referência para `kpi_atendimento_slas_comerciais`.
tags: [golden-query, kpi_atendimento_slas_comerciais, gold_kpis]
status: stable
runtime: bigquery
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:26:04Z
verified:
  by: human:diretoria.regulatoria@empresa.com.br
  at: 2026-10-02T20:26:04Z
---

# Serviços Comerciais com Maior Volume de Violações e Compensações Pagas

Esta consulta SQL é certificada como a forma padrão e otimizada de responder perguntas executivas sobre `kpi_atendimento_slas_comerciais`:

```sql
SELECT servico, artigo_ren_1000, cumprimento_pct, total_solicitacoes, solicitacoes_violadas, compensacao_paga_rs_mm FROM `kpisetoreletrico.gold_kpis.kpi_atendimento_slas_comerciais` ORDER BY compensacao_paga_rs_mm DESC;
```
