---
type: Metric
title: Alavancagem Financeira Setorial (Dívida Líquida / EBITDA)
description: Indicador de solvência que mensura em quantos anos de geração de caixa operacional a empresa liquidaria sua dívida líquida total.
tags: [metrica-regulatoria, cvm]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: process:regulacao-setorial
  at: 2026-10-02T20:30:20Z
---

# Métrica: Alavancagem Financeira Setorial (Dívida Líquida / EBITDA)

- **Regulador / Norma:** CVM
- **Unidade de Medida:** `Múltiplo (x)`
- **Fórmula de Cálculo:** `divida_liquida_rs_mm / NULLIF(ebitda_rs_mm, 0)`

### Definição Regulatória
Indicador de solvência que mensura em quantos anos de geração de caixa operacional a empresa liquidaria sua dívida líquida total.
