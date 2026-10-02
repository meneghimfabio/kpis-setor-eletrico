---
type: Table
title: Tabela cmo_horario_semanal
description: Custo Marginal de Operação (CMO) calculado pelos modelos computacionais do ONS.
resource: bigquery:kpisetoreletrico.operacao_sin.cmo_horario_semanal
tags: [operacao_sin, cmo_horario_semanal, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `cmo_horario_semanal`

**Dataset:** [operacao_sin](../datasets/operacao_sin.md)  
**Recurso:** `bigquery:kpisetoreletrico.operacao_sin.cmo_horario_semanal`

### Descrição Executiva
Custo Marginal de Operação (CMO) calculado pelos modelos computacionais do ONS.

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `data_referencia` | Semana operativa ou hora de apuração do CMO. |
| `patamar_carga` | Patamar de carga: Leve, Média ou Pesada. |
| `subsistema` | Subsistema do SIN. |
| `cmo_rs_mwh` | Custo marginal de suprimento em R$/MWh. |
| `despacho_termico_mw` | Potência térmica acionada por restrição de rede ou segurança energética (MW). |
