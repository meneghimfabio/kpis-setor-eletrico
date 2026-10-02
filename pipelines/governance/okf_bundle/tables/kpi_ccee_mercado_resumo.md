---
type: Table
title: Tabela kpi_ccee_mercado_resumo
description: Visão executiva e analítica do Mercado de Curto Prazo (MCP) operado pela CCEE. Acompanha o Preço de Liquidação das Diferenças (PLD) horário mais recente por submercado (SE/CO, SUL, NE, NORTE), comparações contra piso e teto regulatórios, spread regional máximo e diagnóstico de desacoplamento do SIN.
resource: bigquery:kpisetoreletrico.gold_kpis.kpi_ccee_mercado_resumo
tags: [gold_kpis, kpi_ccee_mercado_resumo, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `kpi_ccee_mercado_resumo`

**Dataset:** [gold_kpis](../datasets/gold_kpis.md)  
**Recurso:** `bigquery:kpisetoreletrico.gold_kpis.kpi_ccee_mercado_resumo`

### Descrição Executiva
Visão executiva e analítica do Mercado de Curto Prazo (MCP) operado pela CCEE. Acompanha o Preço de Liquidação das Diferenças (PLD) horário mais recente por submercado (SE/CO, SUL, NE, NORTE), comparações contra piso e teto regulatórios, spread regional máximo e diagnóstico de desacoplamento do SIN.

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `subsistema` | Submercado de comercialização do SIN (SE/CO, SUL, NORDESTE, NORTE). |
| `pld_rs_mwh` | Preço de Liquidação das Diferenças apurado para o submercado em Reais por Megawatt-hora (R$/MWh). |
| `pld_teto_rs_mwh` | Teto estrutural do PLD fixado anualmente pela ANEEL. |
| `pld_piso_rs_mwh` | Piso estrutural mínimo do PLD regulatório. |
| `patamar` | Patamar de carga horária (Carga Pesada, Média ou Leve). |
| `data_apuracao` | Timestamp da hora de apuração do PLD horário. |
| `pld_medio_nacional_rs_mwh` | Média aritmética do PLD entre os quatro submercados interligados no SIN. |
| `spread_maximo_regional_rs_mwh` | Maior descolamento de preço verificado entre dois submercados (Max(PLD) - Min(PLD)). |
| `status_integracao_sin` | Indicador de transmissão: 'Equilíbrio Inter-regional' ou 'Alerta: Descolamento Estrutural entre Submercados'. |
| `diferenca_vs_media_nacional` | Desvio do PLD do submercado em relação à média nacional (R$/MWh). |
