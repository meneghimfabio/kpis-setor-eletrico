---
type: Table
title: Tabela cvm_dre_empresas
description: Demonstrações financeiras padronizadas (DFP e ITR) das empresas do setor elétrico arquivadas na CVM.
resource: bigquery:kpisetoreletrico.aneel_silver.cvm_dre_empresas
tags: [aneel_silver, cvm_dre_empresas, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `cvm_dre_empresas`

**Dataset:** [aneel_silver](../datasets/aneel_silver.md)  
**Recurso:** `bigquery:kpisetoreletrico.aneel_silver.cvm_dre_empresas`

### Descrição Executiva
Demonstrações financeiras padronizadas (DFP e ITR) das empresas do setor elétrico arquivadas na CVM.

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `empresa` | Razão social da companhia aberta. |
| `ticker` | Código na B3. |
| `codigo_cvm` | Número do registro CVM. |
| `cnpj` | CNPJ cadastral. |
| `segmento` | Segmento setorial. |
| `receita_liquida_rs_mm` | Receita Líquida em R$ Milhões. |
| `ebitda_rs_mm` | EBITDA contábil em R$ Milhões. |
| `margem_ebitda_pct` | Margem EBITDA percentual. |
| `lucro_liquido_rs_mm` | Lucro Líquido em R$ Milhões. |
| `divida_liquida_rs_mm` | Dívida Líquida em R$ Milhões. |
| `capex_rs_mm` | Investimentos em R$ Milhões. |
| `alavancagem` | Índice Dívida Líquida / EBITDA. |
| `ano_referencia` | Ano do exercício social. |
| `tipo_demonstrativo` | Tipo contábil do demonstrativo. |
| `status_auditoria` | Auditoria externa. |
| `auditor` | Firma de auditoria independente. |
