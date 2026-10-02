---
type: Table
title: Tabela kpi_tarifas_ranking
description: Ranking e decomposição das tarifas homologadas de energia elétrica (PRORET) para classe B1 Residencial. Apresenta a tarifa final de aplicação (R$/kWh) e sua segregação estrutural entre a parcela do fio (TUSD - Tarifa de Uso do Sistema de Distribuição) e a parcela de suprimento de energia (TE - Tarifa de Energia), além de parâmetros regulatórios como WACC e Fator X.
resource: bigquery:kpisetoreletrico.gold_kpis.kpi_tarifas_ranking
tags: [gold_kpis, kpi_tarifas_ranking, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `kpi_tarifas_ranking`

**Dataset:** [gold_kpis](../datasets/gold_kpis.md)  
**Recurso:** `bigquery:kpisetoreletrico.gold_kpis.kpi_tarifas_ranking`

### Descrição Executiva
Ranking e decomposição das tarifas homologadas de energia elétrica (PRORET) para classe B1 Residencial. Apresenta a tarifa final de aplicação (R$/kWh) e sua segregação estrutural entre a parcela do fio (TUSD - Tarifa de Uso do Sistema de Distribuição) e a parcela de suprimento de energia (TE - Tarifa de Energia), além de parâmetros regulatórios como WACC e Fator X.

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `distribuidora` | Sigla da concessionária regulada perante a ANEEL. |
| `concessionaria` | Nome empresarial da empresa distribuidora. |
| `uf` | Unidade Federativa de concessão. |
| `resolucao_homologatoria` | Número oficial da Resolução Homologatória da ANEEL que fixou as tarifas vigentes. |
| `data_vigencia` | Data formal de início de vigência do ciclo tarifário homologado. |
| `tarifa_b1_rs_kwh` | Tarifa homologada de aplicação para consumidores da classe B1 Residencial em Reais por quilowatt-hora (R$/kWh), sem impostos. |
| `tusd_rs_mwh` | Parcela TUSD em R$/MWh referente à remuneração do sistema de distribuição (fio e encargos setoriais). |
| `te_rs_mwh` | Parcela TE em R$/MWh referente à compra de energia e comercialização. |
| `share_tusd_fio_pct` | Participação percentual da parcela TUSD no custo total da tarifa: (TUSD / (TUSD + TE)) * 100. |
| `share_te_energia_pct` | Participação percentual da parcela TE de suprimento de energia no custo total: (TE / (TUSD + TE)) * 100. |
| `wacc_regulatorio_pct` | Taxa de Custo Médio Ponderado de Capital regulatório após impostos definido pela ANEEL. |
| `fator_x_pct` | Fator X de ganhos de produtividade e eficiência repassado às tarifas no reajuste/revisão periódica. |
| `ranking_tarifa_mais_barata` | Posição ordinal no ranking tarifário nacional (1º = tarifa mais barata do Brasil). |
