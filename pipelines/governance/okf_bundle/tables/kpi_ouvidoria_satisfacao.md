---
type: Table
title: Tabela kpi_ouvidoria_satisfacao
description: Consolidação de Ouvidoria, Reclamações de Nível 2 escaladas à ANEEL e Índice IASC de Satisfação do Consumidor. Mede o tempo médio de resolução de conflitos, índice de procedência das reclamações e conformidade de SLAs comerciais.
resource: bigquery:kpisetoreletrico.gold_kpis.kpi_ouvidoria_satisfacao
tags: [gold_kpis, kpi_ouvidoria_satisfacao, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `kpi_ouvidoria_satisfacao`

**Dataset:** [gold_kpis](../datasets/gold_kpis.md)  
**Recurso:** `bigquery:kpisetoreletrico.gold_kpis.kpi_ouvidoria_satisfacao`

### Descrição Executiva
Consolidação de Ouvidoria, Reclamações de Nível 2 escaladas à ANEEL e Índice IASC de Satisfação do Consumidor. Mede o tempo médio de resolução de conflitos, índice de procedência das reclamações e conformidade de SLAs comerciais.

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `distribuidora` | Sigla da concessionária avaliada. |
| `data_referencia` | Mês/ano de apuração dos indicadores de ouvidoria. |
| `score_iasc` | Pontuação oficial no Índice ANEEL de Satisfação do Consumidor (escala de 0 a 100 pontos). |
| `ranking_iasc` | Posição no ranking nacional de satisfação IASC. |
| `total_reclamacoes` | Volume total de reclamações protocoladas na Ouvidoria Setorial da ANEEL. |
| `procedencia_pct` | Percentual de reclamações julgadas procedentes a favor do consumidor. |
| `tempo_medio_resolucao_dias` | Prazo médio em dias corridos para resolução definitiva do chamado. |
| `cumprimento_sla_pct` | Percentual de reclamações resolvidas dentro do prazo regulatório estipulado. |
| `classificacao_satisfacao` | Classificação da distribuidora: Alta Satisfação (Excelente), Satisfação Moderada ou Baixa Satisfação. |
