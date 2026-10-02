---
type: Table
title: Tabela pld_horario
description: Preço de Liquidação das Diferenças (PLD) divulgado oficialmente em granularidade horária pela CCEE.
resource: bigquery:kpisetoreletrico.mercado_ccee.pld_horario
tags: [mercado_ccee, pld_horario, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `pld_horario`

**Dataset:** [mercado_ccee](../datasets/mercado_ccee.md)  
**Recurso:** `bigquery:kpisetoreletrico.mercado_ccee.pld_horario`

### Descrição Executiva
Preço de Liquidação das Diferenças (PLD) divulgado oficialmente em granularidade horária pela CCEE.

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `data_hora` | Timestamp da hora de apuração do preço de liquidação das diferenças. |
| `subsistema` | Submercado de comercialização (SE_CO, SUL, NE, NORTE). |
| `pld_rs_mwh` | Valor oficial do PLD para o submercado em R$/MWh. |
| `pld_teto_rs_mwh` | Teto máximo regulatório do PLD no período. |
| `pld_piso_rs_mwh` | Piso mínimo regulatório do PLD. |
| `patamar` | Patamar de consumo (Pesada, Média, Leve). |
