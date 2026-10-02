---
type: Table
title: Tabela curtailment_renovaveis
description: Histórico de cortes e restrições de despacho de usinas eólicas e solares fotovoltaicas pelo ONS.
resource: bigquery:kpisetoreletrico.mercado_ccee.curtailment_renovaveis
tags: [mercado_ccee, curtailment_renovaveis, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `curtailment_renovaveis`

**Dataset:** [mercado_ccee](../datasets/mercado_ccee.md)  
**Recurso:** `bigquery:kpisetoreletrico.mercado_ccee.curtailment_renovaveis`

### Descrição Executiva
Histórico de cortes e restrições de despacho de usinas eólicas e solares fotovoltaicas pelo ONS.

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `data_referencia` | Data e turno da ocorrência do corte operativo de geração. |
| `subsistema` | Subsistema onde ocorreu o corte (comum no Nordeste e Norte). |
| `fonte` | Fonte afetada: Eólica ou Solar Fotovoltaica. |
| `energia_cortada_mwh` | Montante de energia elétrica limpa rejeitada na rede por restrição de transmissão (MWh). |
| `perda_financeira_estimada_rs_mm` | Estimativa de perda financeira associada ao corte de geração. |
