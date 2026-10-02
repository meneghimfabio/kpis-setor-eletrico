---
type: Table
title: Tabela dec_fec_distribuidoras
description: Base tratada e padronizada de indicadores de continuidade coletiva (DEC e FEC) das distribuidoras da ANEEL (PRODIST Módulo 8).
resource: bigquery:kpisetoreletrico.aneel_silver.dec_fec_distribuidoras
tags: [aneel_silver, dec_fec_distribuidoras, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `dec_fec_distribuidoras`

**Dataset:** [aneel_silver](../datasets/aneel_silver.md)  
**Recurso:** `bigquery:kpisetoreletrico.aneel_silver.dec_fec_distribuidoras`

### Descrição Executiva
Base tratada e padronizada de indicadores de continuidade coletiva (DEC e FEC) das distribuidoras da ANEEL (PRODIST Módulo 8).

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `data_referencia` | Mês de apuração do indicador de continuidade (DATE). |
| `distribuidora` | Código identificador da concessionária regulada pela ANEEL. |
| `nome_concessionaria` | Razão social da concessionária de energia. |
| `sigla_uf` | Estado principal da área de concessão. |
| `dec_apurado_horas` | Horas totais de interrupção por consumidor apuradas no período. |
| `dec_limite_aneel_horas` | Limite contratual regulatório de DEC. |
| `conformidade_dec` | Status booleano de conformidade do DEC. |
| `fec_apurado_vezes` | Quantidade de interrupções sofridas pelo consumidor no período. |
| `fec_limite_aneel_vezes` | Limite regulatório máximo de frequência de interrupção (FEC). |
| `conformidade_fec` | Status booleano de conformidade do FEC. |
