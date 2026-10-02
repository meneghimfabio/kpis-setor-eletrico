---
type: Table
title: Tabela tarifas_homologadas
description: Série histórica de resoluções homologatórias de tarifas de distribuição de energia elétrica (PRORET).
resource: bigquery:kpisetoreletrico.aneel_silver.tarifas_homologadas
tags: [aneel_silver, tarifas_homologadas, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `tarifas_homologadas`

**Dataset:** [aneel_silver](../datasets/aneel_silver.md)  
**Recurso:** `bigquery:kpisetoreletrico.aneel_silver.tarifas_homologadas`

### Descrição Executiva
Série histórica de resoluções homologatórias de tarifas de distribuição de energia elétrica (PRORET).

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `distribuidora` | Sigla da distribuidora regulada. |
| `concessionaria` | Nome empresarial da concessionária. |
| `uf` | Estado da concessão. |
| `resolucao_homologatoria` | Número da resolução normativa ou homologatória ANEEL. |
| `data_vigencia` | Data de vigência do novo ciclo tarifário. |
| `tarifa_b1_rs_kwh` | Tarifa de energia para residencial (B1) em R$/kWh. |
| `tusd_rs_mwh` | Componente tarifária de remuneração da rede de distribuição (R$/MWh). |
| `te_rs_mwh` | Componente tarifária de compra de energia gerada (R$/MWh). |
| `wacc_regulatorio_pct` | Taxa de retorno do capital aprovada no ciclo de revisão. |
| `fator_x_pct` | Ganhos de eficiência capturados no processo tarifário. |
