---
type: Table
title: Tabela ess_encargos
description: Encargos de Serviço do Sistema (ESS) decorrentes de segurança energética e restrições de transmissão.
resource: bigquery:kpisetoreletrico.mercado_ccee.ess_encargos
tags: [mercado_ccee, ess_encargos, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `ess_encargos`

**Dataset:** [mercado_ccee](../datasets/mercado_ccee.md)  
**Recurso:** `bigquery:kpisetoreletrico.mercado_ccee.ess_encargos`

### Descrição Executiva
Encargos de Serviço do Sistema (ESS) decorrentes de segurança energética e restrições de transmissão.

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `ano_mes` | Mês de apuração da liquidação financeira da CCEE. |
| `motivo_encargo` | Razão do acionamento térmico: Restrição de Transmissão, Reserva de Potência ou Segurança Energética. |
| `valor_encargo_rs_mm` | Montante total faturado no mercado em R$ Milhões. |
| `impacto_unitario_rs_mwh` | Impacto médio rateado por Megawatt-hora de carga. |
