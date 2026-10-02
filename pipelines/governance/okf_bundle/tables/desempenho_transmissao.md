---
type: Table
title: Tabela desempenho_transmissao
description: Indicadores regulatórios de desempenho das concessionárias de transmissão de energia (CKAN ANEEL).
resource: bigquery:kpisetoreletrico.aneel_silver.desempenho_transmissao
tags: [aneel_silver, desempenho_transmissao, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `desempenho_transmissao`

**Dataset:** [aneel_silver](../datasets/aneel_silver.md)  
**Recurso:** `bigquery:kpisetoreletrico.aneel_silver.desempenho_transmissao`

### Descrição Executiva
Indicadores regulatórios de desempenho das concessionárias de transmissão de energia (CKAN ANEEL).

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `concessionaria` | Razão social da transmissora. |
| `sigla` | Identificador de mercado da empresa transmissora. |
| `holding` | Grupo empresarial controlador. |
| `ano_ciclo` | Ciclo anual da receita da transmissão. |
| `rap_homologada_rs_mm` | Receita Anual Permitida em R$ Milhões. |
| `pvd_rs_mm` | Parcela Variável por Indisponibilidade descontada (R$ Milhões). |
| `pvd_sobre_rap_pct` | Relação percentual PVd/RAP. |
| `disponibilidade_pct` | Percentual de disponibilidade das instalações. |
| `ens_mwh` | Energia Não Suprida decorrente de eventos operacionais. |
| `extensao_km` | Malha total de linhas sob concessão (km). |
| `status` | Classificação de conformidade operacional. |
| `data_referencia` | Mês da apuração regulatória. |
