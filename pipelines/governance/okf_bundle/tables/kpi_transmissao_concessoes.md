---
type: Table
title: Tabela kpi_transmissao_concessoes
description: Desempenho operacional e regulatório das concessões de transmissão de energia elétrica. Acompanha a Receita Anual Permitida (RAP homologada), a Parcela Variável por Indisponibilidade (PVd aplicada), o percentual de desconto sobre a receita (PVd/RAP) e o índice de disponibilidade da malha em quilômetros.
resource: bigquery:kpisetoreletrico.gold_kpis.kpi_transmissao_concessoes
tags: [gold_kpis, kpi_transmissao_concessoes, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `kpi_transmissao_concessoes`

**Dataset:** [gold_kpis](../datasets/gold_kpis.md)  
**Recurso:** `bigquery:kpisetoreletrico.gold_kpis.kpi_transmissao_concessoes`

### Descrição Executiva
Desempenho operacional e regulatório das concessões de transmissão de energia elétrica. Acompanha a Receita Anual Permitida (RAP homologada), a Parcela Variável por Indisponibilidade (PVd aplicada), o percentual de desconto sobre a receita (PVd/RAP) e o índice de disponibilidade da malha em quilômetros.

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `concessionaria` | Nome empresarial da concessionária de transmissão (ex: TAESA, ISA_CTEEP, ELETROBRAS). |
| `sigla` | Sigla de mercado do transmissor. |
| `holding` | Grupo econômico controlador da concessionária. |
| `ano_ciclo` | Ano do ciclo tarifário regulatório da transmissão (ex: 2024/2025). |
| `rap_homologada_rs_mm` | Receita Anual Permitida homologada pela Resolução da ANEEL (R$ Milhões). |
| `pvd_rs_mm` | Parcela Variável por Indisponibilidade deduzida da receita devido a desligamentos de linhas e transformadores (R$ Milhões). |
| `pvd_sobre_rap_pct` | Percentual de perda de receita por indisponibilidade: (PVd / RAP) * 100. |
| `disponibilidade_pct` | Índice de disponibilidade física das Funções Transmissão (%) monitorado pelo ONS. |
| `ens_mwh` | Energia Não Suprida decorrente de perturbações na rede básica da transmissora (MWh). |
| `extensao_km` | Extensão total das linhas de transmissão sob concessão em quilômetros. |
| `status` | Classificação de eficiência da concessão. |
| `ranking_eficiencia` | Posição no ranking de menor penalidade PVd (1º = menor desconto proporcional de receita). |
| `data_referencia` | Mês de apuração dos indicadores da transmissão. |
| `data_processamento` | Timestamp de execução da carga na camada Gold. |
