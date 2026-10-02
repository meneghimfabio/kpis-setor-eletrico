-- ==============================================================================
-- Schema-Defined Grounding DDL: Constraints PK & FK (NOT ENFORCED)
-- Google Cloud BigQuery & Dataplex Knowledge Catalog
-- ==============================================================================
--
-- No BigQuery, restrições PRIMARY KEY e FOREIGN KEY declaradas com NOT ENFORCED
-- não geram overhead de escrita nem quebram pipelines de ingestão.
-- Elas fornecem metadados determinísticos para:
--   1. Otimizador de consultas (BI Engine / Join Elimination / CBO)
--   2. Dataplex Dataset Insights (Garante confidenceScore: 2.0 e proveniência TABLE_CONSTRAINTS)
--   3. Grounding anti-alucinação para Gemini e Agentes de Dados Conversacionais
--
-- ==============================================================================

-- ------------------------------------------------------------------------------
-- 1. PRIMARY KEYS NAS TABELAS DIMENSIONAIS E CONSOLIDADAS (GOLD)
-- ------------------------------------------------------------------------------

-- KPI DEC e FEC de Distribuição
ALTER TABLE `kpisetoreletrico.gold_kpis.kpi_dec_fec_conformidade`
  ADD PRIMARY KEY (distribuidora) NOT ENFORCED;

-- KPI Expansão de Micro e Minigeração Distribuída (por UF)
ALTER TABLE `kpisetoreletrico.gold_kpis.kpi_mmgd_expansao_uf`
  ADD PRIMARY KEY (sigla_uf) NOT ENFORCED;

-- KPI Ranking Tarifário
ALTER TABLE `kpisetoreletrico.gold_kpis.kpi_tarifas_ranking`
  ADD PRIMARY KEY (distribuidora) NOT ENFORCED;

-- KPI Ouvidoria e Satisfação IASC
ALTER TABLE `kpisetoreletrico.gold_kpis.kpi_ouvidoria_satisfacao`
  ADD PRIMARY KEY (distribuidora) NOT ENFORCED;

-- KPI Desempenho Concessões de Transmissão
ALTER TABLE `kpisetoreletrico.gold_kpis.kpi_transmissao_concessoes`
  ADD PRIMARY KEY (sigla, ano_ciclo) NOT ENFORCED;

-- KPI Mercado de Curto Prazo CCEE (por Subsistema)
ALTER TABLE `kpisetoreletrico.gold_kpis.kpi_ccee_mercado_resumo`
  ADD PRIMARY KEY (subsistema) NOT ENFORCED;

-- KPI Operação do SIN (por Subsistema)
ALTER TABLE `kpisetoreletrico.gold_kpis.kpi_sin_operacao_resumo`
  ADD PRIMARY KEY (subsistema) NOT ENFORCED;

-- ------------------------------------------------------------------------------
-- 2. PRIMARY KEYS NA CAMADA SILVER (TABELAS DE BASE REGULATÓRIA)
-- ------------------------------------------------------------------------------

ALTER TABLE `kpisetoreletrico.aneel_silver.dec_fec_distribuidoras`
  ADD PRIMARY KEY (distribuidora, data_referencia) NOT ENFORCED;

ALTER TABLE `kpisetoreletrico.aneel_silver.tarifas_homologadas`
  ADD PRIMARY KEY (distribuidora, data_vigencia) NOT ENFORCED;

ALTER TABLE `kpisetoreletrico.aneel_silver.ouvidoria_reclamacoes`
  ADD PRIMARY KEY (distribuidora, data_referencia) NOT ENFORCED;

ALTER TABLE `kpisetoreletrico.mercado_ccee.pld_horario`
  ADD PRIMARY KEY (subsistema, data_hora) NOT ENFORCED;

-- ------------------------------------------------------------------------------
-- 3. FOREIGN KEYS ENTRE MODELOS GOLD E SILVER (LIGAÇÕES INTER-TABELARES)
-- ------------------------------------------------------------------------------

-- Relacionamento: Ranking Tarifário referencia Ouvidoria pela Distribuidora
ALTER TABLE `kpisetoreletrico.gold_kpis.kpi_ouvidoria_satisfacao`
  ADD CONSTRAINT fk_ouvidoria_distribuidora
  FOREIGN KEY (distribuidora) 
  REFERENCES `kpisetoreletrico.gold_kpis.kpi_tarifas_ranking`(distribuidora) NOT ENFORCED;

-- Relacionamento: DEC/FEC referencia Ranking Tarifário pela Distribuidora
ALTER TABLE `kpisetoreletrico.gold_kpis.kpi_dec_fec_conformidade`
  ADD CONSTRAINT fk_decfec_distribuidora
  FOREIGN KEY (distribuidora) 
  REFERENCES `kpisetoreletrico.gold_kpis.kpi_tarifas_ranking`(distribuidora) NOT ENFORCED;

-- Relacionamento: Mercado CCEE referencia Operação do SIN pelo Subsistema
ALTER TABLE `kpisetoreletrico.gold_kpis.kpi_ccee_mercado_resumo`
  ADD CONSTRAINT fk_ccee_sin_subsistema
  FOREIGN KEY (subsistema) 
  REFERENCES `kpisetoreletrico.gold_kpis.kpi_sin_operacao_resumo`(subsistema) NOT ENFORCED;
