---
type: Metric
title: Duração Equivalente de Interrupção por Unidade Consumidora (DEC)
description: Mede o intervalo médio de tempo que, no período considerado, cada unidade consumidora atendida pela distribuidora ficou desprovida de fornecimento de energia elétrica.
tags: [metrica-regulatoria, aneel-(prodist-módulo-8)]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: process:regulacao-setorial
  at: 2026-10-02T20:30:20Z
---

# Métrica: Duração Equivalente de Interrupção por Unidade Consumidora (DEC)

- **Regulador / Norma:** ANEEL (PRODIST Módulo 8)
- **Unidade de Medida:** `Horas`
- **Fórmula de Cálculo:** `SUM(duracao_interrupcao_horas * consumidores_afetados) / total_consumidores_distribuidora`

### Definição Regulatória
Mede o intervalo médio de tempo que, no período considerado, cada unidade consumidora atendida pela distribuidora ficou desprovida de fornecimento de energia elétrica.
