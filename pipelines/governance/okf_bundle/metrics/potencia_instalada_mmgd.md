---
type: Metric
title: Capacidade Instalada de Micro e Minigeração Distribuída (MMGD)
description: Soma da potência instalada dos sistemas de microgeração (<= 75 kW) e minigeração (> 75 kW até 5 MW) conectados à rede de distribuição.
tags: [metrica-regulatoria, aneel-(lei-14.300/2022-e-ren-1.000/2021)]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: process:regulacao-setorial
  at: 2026-10-02T20:30:20Z
---

# Métrica: Capacidade Instalada de Micro e Minigeração Distribuída (MMGD)

- **Regulador / Norma:** ANEEL (Lei 14.300/2022 e REN 1.000/2021)
- **Unidade de Medida:** `Megawatts (MW)`
- **Fórmula de Cálculo:** `SUM(potencia_nominal_inversor_kw) / 1000.0`

### Definição Regulatória
Soma da potência instalada dos sistemas de microgeração (<= 75 kW) e minigeração (> 75 kW até 5 MW) conectados à rede de distribuição.
