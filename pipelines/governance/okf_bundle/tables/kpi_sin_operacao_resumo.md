---
type: Table
title: Tabela kpi_sin_operacao_resumo
description: Visão consolidada da Operação do Sistema Interligado Nacional (SIN) com dados oficiais do ONS. Integra a Energia Armazenada (EAR %), Energia Natural Afluente (ENA % MLT), Custo Marginal de Operação (CMO) e despacho de usinas termelétricas fora da ordem de mérito por subsistema eletroenergético.
resource: bigquery:kpisetoreletrico.gold_kpis.kpi_sin_operacao_resumo
tags: [gold_kpis, kpi_sin_operacao_resumo, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `kpi_sin_operacao_resumo`

**Dataset:** [gold_kpis](../datasets/gold_kpis.md)  
**Recurso:** `bigquery:kpisetoreletrico.gold_kpis.kpi_sin_operacao_resumo`

### Descrição Executiva
Visão consolidada da Operação do Sistema Interligado Nacional (SIN) com dados oficiais do ONS. Integra a Energia Armazenada (EAR %), Energia Natural Afluente (ENA % MLT), Custo Marginal de Operação (CMO) e despacho de usinas termelétricas fora da ordem de mérito por subsistema eletroenergético.

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `subsistema` | Subsistema eletroenergético do SIN (SE_CO, SUL, NORDESTE, NORTE). |
| `data_referencia` | Data de apuração dos balanços e programações diárias/semanais de operação. |
| `ear_percentual` | Nível percentual de Energia Armazenada nos reservatórios hidrelétricos em relação à capacidade máxima do subsistema. |
| `ear_max_mwmes` | Capacidade máxima de armazenamento energético do subsistema expressa em Megawatts-mês (MWmês). |
| `ear_atual_mwmes` | Volume energético atualmente estocado nos reservatórios hidrelétricos (MWmês). |
| `meta_seguranca_percentual` | Meta de curva de segurança hídrica e armazenamento mínimo recomendada pelo ONS e CMSE. |
| `folga_seguranca_ear_pct` | Margem de segurança hídrica: (ear_percentual - meta_seguranca_percentual). Valores negativos indicam estresse hídrico. |
| `status_ear` | Classificação do reservatório: Confortável, Atenção ou Crítico. |
| `ena_mwmed` | Energia Natural Afluente prevista que flui para as calhas dos rios hidrelétricos, medida em MWmédios. |
| `ena_percentual_mlt` | Afluência hídrica expressa em percentual da Média de Longo Termo histórica (ENA % MLT). |
| `classificacao_ena` | Classificação hidrológica do período (Seca Severa, Seca Moderada, Normal, Úmido). |
| `cmo_medio_rs_mwh` | Custo Marginal de Operação calculado pelo modelo DECOMP/DESSEM do ONS em Reais por MWh. |
| `despacho_termico_mw` | Montante de geração termelétrica a gás/óleo/carvão acionada por garantia de suprimento energético. |
| `status_seguranca_energetica` | Diagnóstico do subsistema: 'Condição Favorável / Segurança Energética', 'Alerta Crítico' ou 'Atenção'. |
