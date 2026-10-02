---
type: Table
title: Tabela kpi_financeiro_dre_empresas
description: Visão financeira executiva consolidada das empresas de capital aberto do setor elétrico brasileiro (CVM). Monitora Receita Líquida, EBITDA ajustado, Margem EBITDA, Lucro Líquido, Dívida Líquida, CAPEX e alavancagem financeira (Dívida Líquida / EBITDA).
resource: bigquery:kpisetoreletrico.gold_kpis.kpi_financeiro_dre_empresas
tags: [gold_kpis, kpi_financeiro_dre_empresas, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `kpi_financeiro_dre_empresas`

**Dataset:** [gold_kpis](../datasets/gold_kpis.md)  
**Recurso:** `bigquery:kpisetoreletrico.gold_kpis.kpi_financeiro_dre_empresas`

### Descrição Executiva
Visão financeira executiva consolidada das empresas de capital aberto do setor elétrico brasileiro (CVM). Monitora Receita Líquida, EBITDA ajustado, Margem EBITDA, Lucro Líquido, Dívida Líquida, CAPEX e alavancagem financeira (Dívida Líquida / EBITDA).

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `empresa` | Razão social ou denominação comercial da holding ou transmissora/distribuidora. |
| `ticker` | Código de negociação das ações na B3 (ex: CPFE3, EGIE3, CMIG4, TAEE11). |
| `codigo_cvm` | Código oficial de registro da companhia aberta na CVM. |
| `cnpj` | CNPJ da empresa. |
| `segmento` | Segmento de atuação: Geração, Transmissão, Distribuição ou Integrada. |
| `ano_referencia` | Ano do exercício fiscal apurado. |
| `tipo_demonstrativo` | Tipo da demonstração: DFP Consolidado ou ITR. |
| `status_auditoria` | Parecer dos auditores independentes (Sem Ressalva, etc.). |
| `receita_liquida_rs_mm` | Receita operacional líquida anual ou trimestral (R$ Milhões). |
| `ebitda_rs_mm` | Lucro antes de Juros, Impostos, Depreciação e Amortização (R$ Milhões). |
| `margem_ebitda_pct` | Margem de rentabilidade operacional: (EBITDA / Receita Líquida) * 100. |
| `lucro_liquido_rs_mm` | Resultado líquido final do exercício (R$ Milhões). |
| `divida_liquida_rs_mm` | Endividamento financeiro bruto menos caixa e equivalentes (R$ Milhões). |
| `capex_rs_mm` | Investimentos de capital realizados em expansão e modernização da rede (R$ Milhões). |
| `alavancagem` | Múltiplo de endividamento financeiro: Dívida Líquida / EBITDA. |
| `data_processamento` | Timestamp de consolidação dos dados no BigQuery. |
