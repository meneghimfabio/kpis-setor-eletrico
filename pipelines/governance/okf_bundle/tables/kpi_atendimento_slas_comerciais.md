---
type: Table
title: Tabela kpi_atendimento_slas_comerciais
description: Cumprimento de prazos regulatórios e SLAs de serviços comerciais da Resolução Normativa ANEEL nº 1.000/2021. Acompanha solicitações de ligação nova, religação de emergência, vistorias e compensações financeiras pagas por atraso.
resource: bigquery:kpisetoreletrico.gold_kpis.kpi_atendimento_slas_comerciais
tags: [gold_kpis, kpi_atendimento_slas_comerciais, governado, producao]
status: stable
generated:
  by: agent/gcp_knowledge_catalog
  at: 2026-10-02T20:30:20Z
verified:
  by: human:engenharia.dados@empresa.com.br
  at: 2026-10-02T20:30:20Z
---

# Tabela: `kpi_atendimento_slas_comerciais`

**Dataset:** [gold_kpis](../datasets/gold_kpis.md)  
**Recurso:** `bigquery:kpisetoreletrico.gold_kpis.kpi_atendimento_slas_comerciais`

### Descrição Executiva
Cumprimento de prazos regulatórios e SLAs de serviços comerciais da Resolução Normativa ANEEL nº 1.000/2021. Acompanha solicitações de ligação nova, religação de emergência, vistorias e compensações financeiras pagas por atraso.

### Esquema e Dicionário de Dados
| Coluna | Descrição Semântica / Regulatória |
| :--- | :--- |
| `servico` | Descrição do serviço comercial regulado (ex: Religação de Urgência, Ligação Nova Urbana, Troca de Titularidade). |
| `sigla_indicador` | Sigla padronizada pela ANEEL para o indicador comercial (ex: PRAZ_RELIG, PRAZ_LIG). |
| `artigo_ren_1000` | Artigo de fundamentação legal na Resolução Normativa ANEEL nº 1.000/2021. |
| `unidade_sla` | Unidade de contagem do prazo regulatório (Horas ou Dias Úteis). |
| `sla_regulatorio_valor` | Prazo máximo tolerado pela norma regulatória. |
| `tempo_medio_real` | Prazo médio efetivamente praticado pelas concessionárias para execução do serviço. |
| `cumprimento_pct` | Taxa percentual de solicitações atendidas estritamente dentro do prazo legal. |
| `total_solicitacoes` | Volume total de protocolos comerciais abertos pelos consumidores. |
| `solicitacoes_violadas` | Quantidade absoluta de pedidos executados com atraso ou ainda pendentes fora do prazo. |
| `compensacao_paga_rs_mm` | Montante total de crédito e indenizações financeiras creditadas aos clientes por violação de prazos regulatórios (R$ MM). |
| `status` | Conformidade do SLA: Conforme, Atenção ou Crítico. |
| `data_referencia` | Mês de apuração contábil dos serviços comerciais. |
| `data_processamento` | Timestamp de atualização do modelo Gold. |
