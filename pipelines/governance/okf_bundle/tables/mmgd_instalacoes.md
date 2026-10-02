---
type: Table
title: Tabela mmgd_instalacoes
description: Empreendimentos de micro e minigeração distribuída registrados no SISGD/ANEEL sob o marco legal da Lei 14.300/2022.
resource: bigquery:kpisetoreletrico.aneel_silver.mmgd_instalacoes
tags: [aneel_silver, mmgd_instalacoes, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `mmgd_instalacoes`

**Dataset:** [aneel_silver](../datasets/aneel_silver.md)  
**Recurso:** `bigquery:kpisetoreletrico.aneel_silver.mmgd_instalacoes`

### Descrição Executiva
Empreendimentos de micro e minigeração distribuída registrados no SISGD/ANEEL sob o marco legal da Lei 14.300/2022.

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `codigo_gd` | Código único de identificação do empreendimento de geração distribuída no SISGD. |
| `sigla_uf` | Unidade Federativa de conexão do sistema. |
| `municipio` | Município de instalação do gerador solar ou biomassa. |
| `subsistema` | Subsistema elétrico de atendimento. |
| `data_conexao` | Data formal de conexão do sistema à rede da distribuidora. |
| `potencia_instalada_kw` | Potência nominal do inversor/gerador em quilowatts (kW). |
| `modalidade` | Modalidade jurídica da GD: Autoconsumo Local, Remoto, Geração Compartilhada ou EMUC. |
| `fonte_energia` | Tecnologia de geração: Solar Fotovoltaica, Hidroelétrica (CGH), Biomassa ou Eólica. |
| `qtd_conexoes` | Quantidade de unidades consumidoras beneficiárias dos créditos de energia. |
