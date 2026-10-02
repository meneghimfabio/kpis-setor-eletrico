---
type: Table
title: Tabela kpi_dec_fec_conformidade
description: Visão executiva da conformidade de qualidade de fornecimento das distribuidoras de energia elétrica. Compara a Duração Equivalente de Interrupção por Unidade Consumidora (DEC em horas) e a Frequência Equivalente (FEC em vezes) contra os limites anuais regulatórios fixados pela ANEEL no PRODIST Módulo 8. Calcula o desvio em horas/vezes, percentual de extrapolação, ranking de qualidade e estimativa de penalidades financeiras.
resource: bigquery:kpisetoreletrico.gold_kpis.kpi_dec_fec_conformidade
tags: [gold_kpis, kpi_dec_fec_conformidade, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `kpi_dec_fec_conformidade`

**Dataset:** [gold_kpis](../datasets/gold_kpis.md)  
**Recurso:** `bigquery:kpisetoreletrico.gold_kpis.kpi_dec_fec_conformidade`

### Descrição Executiva
Visão executiva da conformidade de qualidade de fornecimento das distribuidoras de energia elétrica. Compara a Duração Equivalente de Interrupção por Unidade Consumidora (DEC em horas) e a Frequência Equivalente (FEC em vezes) contra os limites anuais regulatórios fixados pela ANEEL no PRODIST Módulo 8. Calcula o desvio em horas/vezes, percentual de extrapolação, ranking de qualidade e estimativa de penalidades financeiras.

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `data_referencia` | Mês e ano de referência da apuração contábil e regulatória (formato DATE/TIMESTAMP). |
| `distribuidora` | Sigla de identificação regulatória da distribuidora perante a ANEEL (ex: CPFL_PAULISTA, ENEL_SP, CEMIG_D). |
| `nome_concessionaria` | Razão social completa da concessionária ou permissionária de distribuição de energia elétrica. |
| `sigla_uf` | Unidade Federativa (UF) principal de atuação da área de concessão. |
| `dec_apurado_horas` | Duração Equivalente de Interrupção por Unidade Consumidora apurada no período, medida em horas contínuas. |
| `dec_limite_aneel_horas` | Meta regulatória máxima de DEC fixada em contrato de concessão pela Resolução Homologatória da ANEEL. |
| `desvio_dec_horas` | Diferença aritmética absoluta entre DEC apurado e o limite regulatório (horas). Valores positivos denotam infração. |
| `percentual_ultrapassagem_dec` | Percentual de violação do limite regulatório de DEC: ((dec_apurado / dec_limite) - 1) * 100. |
| `conformidade_dec` | Booleano indicando se a distribuidora cumpriu a meta de continuidade (TRUE = Conforme / DEC <= Limite). |
| `fec_apurado_vezes` | Frequência Equivalente de Interrupção apurada no período, medida em quantidade de interrupções. |
| `fec_limite_aneel_vezes` | Limite regulatório máximo de frequência (FEC) homologado pela ANEEL. |
| `desvio_fec_vezes` | Diferença aritmética absoluta entre FEC apurado e limite regulatório (vezes). |
| `percentual_ultrapassagem_fec` | Percentual de violação do limite de frequência de interrupção (FEC). |
| `conformidade_fec` | Booleano indicando conformidade do FEC (TRUE = Conforme / FEC <= Limite). |
| `status_regulatorio` | Classificação executiva: 'Conforme', 'Crítico (DEC e FEC)', 'Atenção (DEC Ultrapassado)' ou 'Atenção (FEC Ultrapassado)'. |
| `compensacao_estimada_rs_mm` | Estimativa paramétrica da compensação financeira obrigatória a ser creditada na fatura dos consumidores (R$ Milhões). |
| `ranking_qualidade_dec` | Posição no ranking nacional de qualidade de fornecimento (1º lugar = menor DEC / maior continuidade). |
