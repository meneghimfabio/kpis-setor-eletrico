-- ==============================================================================
-- SATI (Sistema Agêntico de Tesouraria Inteligente)
-- DDL para Armazenamento e Auditoria de Propostas de Garantias CCEE
-- ==============================================================================

CREATE SCHEMA IF NOT EXISTS `kpisetoreletrico.trm_ccee`
OPTIONS(
  location="southamerica-east1",
  description="Dados de liquidação financeira CCEE, cálculo de garantias e conciliação SAP TRM"
);

CREATE TABLE IF NOT EXISTS `kpisetoreletrico.trm_ccee.ccee_guarantee_proposals` (
  proposal_id STRING NOT NULL OPTIONS(description="Identificador único da proposta gerada pelo Agente SATI"),
  agent_ccee_code STRING NOT NULL OPTIONS(description="Código do Agente de Mercado na CCEE"),
  subsystem STRING NOT NULL OPTIONS(description="Submercado do SIN: SE, S, NE, N"),
  assessment_date DATE NOT NULL OPTIONS(description="Data de referência da apuração da garantia"),
  net_exposure_mwh NUMERIC OPTIONS(description="Exposição física líquida estimada (MWh)"),
  total_exposure_brl NUMERIC OPTIONS(description="Valor bruto da exposição ao PLD horário (R$)"),
  prudential_margin_brl NUMERIC OPTIONS(description="Margem prudencial regulatória calculada (R$)"),
  existing_guarantees_brl NUMERIC OPTIONS(description="Total de garantias financeiras já aportadas e ativas (R$)"),
  required_additional_guarantee_brl NUMERIC OPTIONS(description="Montante adicional líquido a provisionar no SAP (R$)"),
  sap_parked_doc_number STRING OPTIONS(description="Número do Documento Estacionado (Parked) criado no SAP FI/TRM"),
  status STRING NOT NULL OPTIONS(description="Status Maker-Checker: PENDING_APPROVAL, APPROVED, REJECTED, EXPIRED"),
  approved_by STRING OPTIONS(description="Identificação funcional do Tesoureiro responsável pela aprovação"),
  approval_timestamp TIMESTAMP OPTIONS(description="Timestamp da aprovação humana no SAP Fiori"),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP() OPTIONS(description="Timestamp de geração pelo Agente CCEE")
)
PARTITION BY assessment_date
CLUSTER BY agent_ccee_code, status;
