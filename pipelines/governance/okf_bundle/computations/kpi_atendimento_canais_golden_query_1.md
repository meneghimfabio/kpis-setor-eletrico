---
type: Attested Computation
title: Distribuidoras com Descumprimento do Índice de Nível de Serviço (INS)
description: Consulta atestada de referência para `kpi_atendimento_canais`.
tags: [golden-query, kpi_atendimento_canais, gold_kpis]
status: stable
runtime: bigquery
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:26:04Z
verified:
  by: human:diretoria.regulatoria@empresa.com.br
  at: 2026-10-02T20:26:04Z
---

# Distribuidoras com Descumprimento do Índice de Nível de Serviço (INS)

Esta consulta SQL é certificada como a forma padrão e otimizada de responder perguntas executivas sobre `kpi_atendimento_canais`:

```sql
SELECT distribuidora, nome_concessionaria, ins_pct, iab_pct, tma_s, status_geral FROM `kpisetoreletrico.gold_kpis.kpi_atendimento_canais` WHERE ins_pct < 85.0 ORDER BY ins_pct ASC;
```
