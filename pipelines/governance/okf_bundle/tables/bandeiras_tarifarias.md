---
type: Table
title: Tabela bandeiras_tarifarias
description: Histórico de acionamento do Sistema de Bandeiras Tarifárias homologado pela ANEEL e CCEE.
resource: bigquery:kpisetoreletrico.mercado_ccee.bandeiras_tarifarias
tags: [mercado_ccee, bandeiras_tarifarias, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `bandeiras_tarifarias`

**Dataset:** [mercado_ccee](../datasets/mercado_ccee.md)  
**Recurso:** `bigquery:kpisetoreletrico.mercado_ccee.bandeiras_tarifarias`

### Descrição Executiva
Histórico de acionamento do Sistema de Bandeiras Tarifárias homologado pela ANEEL e CCEE.

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `mes_ano` | Mês/ano de referência de aplicação da bandeira tarifária. |
| `bandeira_acionada` | Bandeira vigente: Verde, Amarela, Vermelha Patamar 1, Vermelha Patamar 2 ou Escassez Hídrica. |
| `adicional_rs_kwh` | Custo adicional repassado à tarifa de consumo (R$/kWh). |
| `justificativa_ons_ccee` | Motivação técnico-energética para acionamento (CMO e GSF). |
