"""
Agente Especialista CCEE e Garantias (SATI).
Orquestra o ciclo de abertura de mercado:
1. Conecta aos dados operacionais e de mercado (PLD e medições horárias)
2. Invoca o motor determinístico de cálculo de garantia regulatória
3. Gera o Documento Pré-editado (Parked Document) no SAP TRM/FI via Apigee
4. Registra a trilha de auditoria e emite síntese executiva
"""
import uuid
from typing import Dict, Any, List
from decimal import Decimal
from pipelines.ccee.guarantee_calculator import CCEEGuaranteeEngine, HourlyPosition
from backend.integrations.sap_trm_apigee import SapTrmApigeeClient

SYSTEM_INSTRUCTION = """
Você é o Agente Especialista CCEE e Garantias do SATI (Sistema Agêntico de Tesouraria Inteligente).
Sua missão é dimensionar com rigor analítico a necessidade de garantias financeiras no Mercado de Curto Prazo (MCP)
e propor o provisionamento adequado no SAP TRM / FI antes da abertura do mercado.

DIRETRIZES CRÍTICAS DE SEGURANÇA E NEGÓCIO:
1. NUNCA faça contas matemáticas de garantias ou exposições por conta própria. Use SEMPRE o motor determinístico.
2. NUNCA tente efetivar ou pagar transações diretamente. Utilize SEMPRE a rotina de pré-edição (Parked Documents).
3. Todo documento pré-editado no SAP deve conter justificativa técnica e código do agente CCEE.
4. O Tesoureiro Humano (Maker-Checker) é a autoridade exclusiva para efetivação contábil e liquidação bancária.
"""

class CCEEGuaranteeAgent:
    def __init__(self, prudential_margin_rate: float = 0.05):
        self.calc_engine = CCEEGuaranteeEngine(prudential_margin_rate=Decimal(str(prudential_margin_rate)))
        self.sap_client = SapTrmApigeeClient()

    def run_pre_market_cycle(
        self,
        ccee_code: str,
        company_code: str,
        assessment_date: str,
        subsystem: str,
        hourly_positions: List[Dict[str, Any]],
        existing_guarantees: float
    ) -> Dict[str, Any]:
        """
        Executa o ciclo pre-market de apuração e provisionamento de garantias CCEE.
        """
        proposal_id = f"PROP-{assessment_date.replace('-', '')}-{uuid.uuid4().hex[:8].upper()}"

        # 1. Parsing com precisão decimal
        positions = [
            HourlyPosition(
                hour=p["hour"],
                consumption_mwh=Decimal(str(p["consumption_mwh"])),
                generation_mwh=Decimal(str(p["generation_mwh"])),
                bilateral_contracts_mwh=Decimal(str(p["bilateral_contracts_mwh"])),
                pld_brl_mwh=Decimal(str(p["pld_brl_mwh"]))
            ) for p in hourly_positions
        ]

        # 2. Execução do cálculo determinístico
        assessment = self.calc_engine.calculate_daily_requirement(
            ccee_code=ccee_code,
            assessment_date=assessment_date,
            hourly_data=positions,
            existing_guarantees=Decimal(str(existing_guarantees))
        )

        # 3. Interação com SAP TRM/FI via Apigee (Somente Parked Document)
        sap_result = None
        if assessment.required_additional_guarantee_brl > Decimal("0.00"):
            sap_result = self.sap_client.create_parked_guarantee_document(
                company_code=company_code,
                ccee_agent_code=ccee_code,
                amount=assessment.required_additional_guarantee_brl,
                text_memo=f"Aporte MCP CCEE {assessment_date} Submercado {subsystem}"
            )

        # 4. Formatação do payload estruturado e auditável (BigQuery & Cockpit)
        record = {
            "proposal_id": proposal_id,
            "ccee_code": assessment.agent_ccee_code,
            "subsystem": subsystem,
            "assessment_date": assessment.assessment_date,
            "net_exposure_mwh": float(assessment.net_exposure_mwh),
            "total_exposure_brl": float(assessment.total_exposure_brl),
            "prudential_margin_brl": float(assessment.prudential_margin_brl),
            "existing_guarantees_brl": float(assessment.existing_guarantees_brl),
            "required_additional_guarantee_brl": float(assessment.required_additional_guarantee_brl),
            "recommendation": assessment.recommendation,
            "sap_parked_document": sap_result.get("sap_document_number") if sap_result else None,
            "maker_checker_status": "PENDING_APPROVAL" if sap_result else "EXEMPT",
            "executive_summary": self._generate_executive_summary(assessment, sap_result, subsystem)
        }

        return record

    def _generate_executive_summary(self, assessment, sap_result, subsystem: str) -> str:
        """Gera síntese narrativa em formato executivo para o Tesoureiro / CFO."""
        if assessment.required_additional_guarantee_brl > Decimal("0.00"):
            doc_info = sap_result.get("sap_document_number") if sap_result else "N/A"
            return (
                f"🚨 **Atenção Tesouraria (Abertura de Mercado CCEE):**\n"
                f"Para a data {assessment.assessment_date} (Submercado {subsystem}), foi apurada uma exposição líquida "
                f"devedora de {assessment.net_exposure_mwh:,.2f} MWh, totalizando R$ {assessment.total_exposure_brl:,.2f} em PLD, "
                f"com margem prudencial de R$ {assessment.prudential_margin_brl:,.2f}.\n"
                f"Considerando garantias ativas de R$ {assessment.existing_guarantees_brl:,.2f}, é exigido aporte adicional de "
                f"**R$ {assessment.required_additional_guarantee_brl:,.2f}** até as 09:30 BRT.\n"
                f"✅ **Ação Realizada:** Documento Pré-editado (Parked) `{doc_info}` criado no SAP TRM/FI. "
                f"Aguardando liberação humana no Fiori para emissão de carta de fiança ou trava de saldo."
            )
        else:
            return (
                f"🟢 **Posição Confortável (CCEE):**\n"
                f"Para a data {assessment.assessment_date} (Submercado {subsystem}), a posição líquida apurada "
                f"não requer aporte adicional de garantia. As garantias ativas cobrem a totalidade da exposição estimada."
            )
