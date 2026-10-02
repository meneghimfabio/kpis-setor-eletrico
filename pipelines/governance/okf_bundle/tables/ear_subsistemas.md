---
type: Table
title: Tabela ear_subsistemas
description: Histórico diário e semanal de Energia Armazenada (EAR) nos reservatórios hidrelétricos do SIN (ONS).
resource: bigquery:kpisetoreletrico.operacao_sin.ear_subsistemas
tags: [operacao_sin, ear_subsistemas, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `ear_subsistemas`

**Dataset:** [operacao_sin](../datasets/operacao_sin.md)  
**Recurso:** `bigquery:kpisetoreletrico.operacao_sin.ear_subsistemas`

### Descrição Executiva
Histórico diário e semanal de Energia Armazenada (EAR) nos reservatórios hidrelétricos do SIN (ONS).

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `data_referencia` | Data da apuração diária da EAR. |
| `subsistema` | Subsistema eletroenergético (SE_CO, SUL, NORDESTE, NORTE). |
| `ear_percentual` | Percentual de água estocada nos reservatórios sobre a capacidade máxima. |
| `ear_max_mwmes` | Energia máxima armazenável em MWmês. |
| `ear_atual_mwmes` | Energia atual armazenada em MWmês. |
| `meta_seguranca_percentual` | Curva guia mínima de segurança energética. |
| `status_criticidade` | Avaliação de criticidade hídrica. |
