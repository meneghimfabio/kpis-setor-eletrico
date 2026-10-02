---
type: Table
title: Tabela kpi_mmgd_expansao_uf
description: Indicadores executivos agregados de Micro e Minigeração Distribuída (MMGD) por Estado brasileiro. Consolida o total de conexões ativas na rede, potência instalada acumulada (MW), projeção de geração de energia mensal (GWh), market share estadual sobre o parque nacional e subsistema elétrico associado (SIN).
resource: bigquery:kpisetoreletrico.gold_kpis.kpi_mmgd_expansao_uf
tags: [gold_kpis, kpi_mmgd_expansao_uf, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `kpi_mmgd_expansao_uf`

**Dataset:** [gold_kpis](../datasets/gold_kpis.md)  
**Recurso:** `bigquery:kpisetoreletrico.gold_kpis.kpi_mmgd_expansao_uf`

### Descrição Executiva
Indicadores executivos agregados de Micro e Minigeração Distribuída (MMGD) por Estado brasileiro. Consolida o total de conexões ativas na rede, potência instalada acumulada (MW), projeção de geração de energia mensal (GWh), market share estadual sobre o parque nacional e subsistema elétrico associado (SIN).

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `sigla_uf` | Unidade Federativa de localização dos empreendimentos de MMGD (27 estados e DF). |
| `subsistema` | Subsistema do Sistema Interligado Nacional (SE_CO, SUL, NORDESTE, NORTE). |
| `ultima_data_referencia` | Data mais recente de atualização da base de dados do SISGD/ANEEL. |
| `total_conexoes` | Quantidade acumulada de unidades geradoras conectadas à rede de distribuição de baixa e média tensão. |
| `potencia_instalada_mw` | Potência operacional instalada de geração distribuída no estado, convertida para Megawatts (MW). |
| `energia_autogerada_gwh_mes` | Estimativa paramétrica de geração de energia elétrica mensal (GWh) baseada em fator de capacidade fotovoltaico médio (~19%). |
| `market_share_nacional_pct` | Participação percentual da potência instalada do estado em relação ao total nacional de MMGD. |
| `ranking_nacional_potencia` | Posição ordinal no ranking brasileiro de capacidade instalada de geração distribuída (1º = maior capacidade instalada). |
