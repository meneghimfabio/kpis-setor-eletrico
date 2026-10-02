"""
Suíte de testes nativa (unittest) para validação do Agente CCEE e Garantias (SATI):
1. Teste de precisão do motor matemático determinístico
2. Teste de conformidade com a regra SoR (Somente Parked Documents)
3. Teste de cenários de exposições devedoras, credoras e margens prudenciais
"""
import unittest
from decimal import Decimal
from pipelines.ccee.guarantee_calculator import CCEEGuaranteeEngine, HourlyPosition
from backend.integrations.sap_trm_apigee import SapTrmApigeeClient
from backend.agents.ccee_guarantee_agent import CCEEGuaranteeAgent

class TestCCEEGuarantees(unittest.TestCase):
    def test_engine_debtor_position_triggers_guarantee(self):
        engine = CCEEGuaranteeEngine(prudential_margin_rate=Decimal("0.05"))
        
        # Simulação de 2 horas de déficit (consumo > geração + contratos)
        hourly_positions = [
            HourlyPosition(hour=1, consumption_mwh=Decimal("100.0"), generation_mwh=Decimal("50.0"), bilateral_contracts_mwh=Decimal("30.0"), pld_brl_mwh=Decimal("200.0")), # net 20 MWh * 200 = R$ 4,000
            HourlyPosition(hour=2, consumption_mwh=Decimal("150.0"), generation_mwh=Decimal("80.0"), bilateral_contracts_mwh=Decimal("40.0"), pld_brl_mwh=Decimal("300.0")), # net 30 MWh * 300 = R$ 9,000
        ]
        
        # Exposição total = 13,000. Margem prudencial (5%) = 650. Total bruto = 13,650.
        existing_guarantees = Decimal("5000.00")
        
        res = engine.calculate_daily_requirement(
            ccee_code="AG_ENER_01",
            assessment_date="2026-10-02",
            hourly_data=hourly_positions,
            existing_guarantees=existing_guarantees
        )
        
        self.assertEqual(res.total_exposure_brl, Decimal("13000.00"))
        self.assertEqual(res.prudential_margin_brl, Decimal("650.00"))
        self.assertEqual(res.required_additional_guarantee_brl, Decimal("8650.00"))
        self.assertIn("APORTE_OBRIGATORIO", res.recommendation)

    def test_engine_creditor_position_requires_zero_guarantee(self):
        engine = CCEEGuaranteeEngine()
        
        # Simulação de agente com sobra de geração (credor no MCP)
        hourly_positions = [
            HourlyPosition(hour=1, consumption_mwh=Decimal("50.0"), generation_mwh=Decimal("100.0"), bilateral_contracts_mwh=Decimal("0.0"), pld_brl_mwh=Decimal("250.0")),
        ]
        
        res = engine.calculate_daily_requirement(
            ccee_code="AG_GERADOR_02",
            assessment_date="2026-10-02",
            hourly_data=hourly_positions,
            existing_guarantees=Decimal("0.00")
        )
        
        self.assertLessEqual(res.total_exposure_brl, Decimal("0.00"))
        self.assertEqual(res.required_additional_guarantee_brl, Decimal("0.00"))
        self.assertIn("CREDOR_LIQUIDO", res.recommendation)

    def test_sap_client_only_parks_document(self):
        client = SapTrmApigeeClient()
        res = client.create_parked_guarantee_document(
            company_code="1000",
            ccee_agent_code="AG_ENER_01",
            amount=Decimal("150000.50"),
            text_memo="Teste de Garantia"
        )
        
        # Regra estrita: status deve ser PARKED_SUCCESS e maker_checker deve ser PENDING_APPROVAL
        self.assertEqual(res["status"], "PARKED_SUCCESS")
        self.assertEqual(res["maker_checker_status"], "PENDING_APPROVAL")
        self.assertTrue(res["sap_document_number"].startswith("PARK-2026-"))

    def test_agent_end_to_end_pre_market_cycle(self):
        agent = CCEEGuaranteeAgent()
        
        hourly_input = [
            {"hour": 1, "consumption_mwh": 200.0, "generation_mwh": 100.0, "bilateral_contracts_mwh": 50.0, "pld_brl_mwh": 350.0},
            {"hour": 2, "consumption_mwh": 250.0, "generation_mwh": 120.0, "bilateral_contracts_mwh": 60.0, "pld_brl_mwh": 400.0}
        ]
        
        cycle_res = agent.run_pre_market_cycle(
            ccee_code="AG_ALPHA",
            company_code="1000",
            assessment_date="2026-10-02",
            subsystem="SE/CO",
            hourly_positions=hourly_input,
            existing_guarantees=10000.0
        )
        
        self.assertEqual(cycle_res["maker_checker_status"], "PENDING_APPROVAL")
        self.assertIsNotNone(cycle_res["sap_parked_document"])
        self.assertGreater(cycle_res["required_additional_guarantee_brl"], 0)
        self.assertIn("Atenção Tesouraria", cycle_res["executive_summary"])

if __name__ == "__main__":
    unittest.main()
