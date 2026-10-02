---
type: Metric
title: Frequência Equivalente de Interrupção por Unidade Consumidora (FEC)
description: Mede o número médio de vezes que, no período considerado, cada unidade consumidora atendida pela distribuidora sofreu descontinuidade no suprimento de energia.
tags: [metrica-regulatoria, aneel-(prodist-módulo-8)]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: process:regulacao-setorial
  at: 2026-10-02T20:30:20Z
---

# Métrica: Frequência Equivalente de Interrupção por Unidade Consumidora (FEC)

- **Regulador / Norma:** ANEEL (PRODIST Módulo 8)
- **Unidade de Medida:** `Vezes`
- **Fórmula de Cálculo:** `SUM(interrupcoes * consumidores_afetados) / total_consumidores_distribuidora`

### Definição Regulatória
Mede o número médio de vezes que, no período considerado, cada unidade consumidora atendida pela distribuidora sofreu descontinuidade no suprimento de energia.
