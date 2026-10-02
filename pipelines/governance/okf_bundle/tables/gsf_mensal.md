---
type: Table
title: Tabela gsf_mensal
description: Fator de Escala de Geração (GSF - Generation Scaling Factor) do Mecanismo de Realocação de Energia (MRE).
resource: bigquery:kpisetoreletrico.mercado_ccee.gsf_mensal
tags: [mercado_ccee, gsf_mensal, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `gsf_mensal`

**Dataset:** [mercado_ccee](../datasets/mercado_ccee.md)  
**Recurso:** `bigquery:kpisetoreletrico.mercado_ccee.gsf_mensal`

### Descrição Executiva
Fator de Escala de Geração (GSF - Generation Scaling Factor) do Mecanismo de Realocação de Energia (MRE).

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `ano_mes` | Mês de apuração contábil da liquidação financeira do MRE. |
| `gsf_apurado` | Razão entre a geração hidrelétrica total do MRE e a Garantia Física consolidada. |
| `deficit_geracao_pct` | Déficit percentual de geração hídrica em relação à garantia física. |
| `status_risco_hidrologico` | Classificação do risco hidrológico para geradores hidrelétricos. |
