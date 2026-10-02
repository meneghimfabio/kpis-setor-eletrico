"""
Suíte de Testes Programáticos Automatizados - Sprint 1 do Lakehouse do Setor Elétrico:
1. Endpoint /api/v1/alerts/ - Análise sobre Camada Gold e eliminação de mocks ALT-001..ALT-005
2. Materialização e Endpoint /api/v1/sin/overview - Camada Gold kpi_sin_operacao_resumo com Fallback
3. Integração BCB SGS - Séries Selic (432) e IPCA (13522) aplicadas ao Simulador PRORET e Visão Macro
4. Verificação da configuração do Cloud Scheduler para Hidrologia do SIN
5. Resiliência e Graceful Fallback com BigQuery offline
"""
import os
import sys
import unittest
from fastapi.testclient import TestClient

# Adicionar backend ao path para importação
backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

from app.main import app
from app.core.bigquery_client import bq_manager
from app.core.bcb_client import bcb_client
from app.data.local_cache import cache


class TestSprint1Lakehouse(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)

    def setUp(self):
        # Limpar cache de domínio antes de cada teste
        cache.clear()

    def test_01_alerts_endpoint_analytical_gold_and_no_mocks(self):
        """Valida que o endpoint /alerts/ gera alertas analíticos e eliminou os mocks ALT-001 a ALT-005."""
        response = self.client.get("/api/v1/alerts/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("total", data)
        self.assertIn("alertas", data)
        self.assertIn("_metadata", data)
        self.assertGreater(data["total"], 0)
        
        alert_ids = [a["id"] for a in data["alertas"]]
        
        # Validação estrita: Nenhum dos mocks legados (ALT-001..ALT-005) pode existir
        for mock_id in ["ALT-001", "ALT-002", "ALT-003", "ALT-004", "ALT-005"]:
            self.assertNotIn(mock_id, alert_ids, f"Mock legado {mock_id} não foi eliminado!")

        # Validação dos novos IDs analíticos estruturados
        has_dec_alert = any(a["id"].startswith("ALT-DEC-") for a in data["alertas"])
        has_ccee_alert = any(a["id"].startswith("ALT-GSF-") or a["id"].startswith("ALT-PLD-") for a in data["alertas"])
        self.assertTrue(has_dec_alert, "Deve conter alerta analítico de DEC/FEC (distribuição)")
        self.assertTrue(has_ccee_alert, "Deve conter alerta analítico de CCEE (GSF ou PLD)")

        # Validação da estrutura de campos obrigatórios
        for a in data["alertas"]:
            self.assertIn("id", a)
            self.assertIn("nivel", a)
            self.assertIn(a["nivel"], ["critico", "alerta", "info"])
            self.assertIn("modulo", a)
            self.assertIn("titulo", a)
            self.assertIn("descricao", a)
            self.assertIn("data_evento", a)

    def test_02_alerts_filtering_capabilities(self):
        """Testa a filtragem por nível e módulo regulatório no endpoint de alertas."""
        resp_critico = self.client.get("/api/v1/alerts/?nivel=critico")
        self.assertEqual(resp_critico.status_code, 200)
        data_crit = resp_critico.json()
        for a in data_crit["alertas"]:
            self.assertEqual(a["nivel"], "critico")

        resp_dist = self.client.get("/api/v1/alerts/?modulo=Distribuição")
        self.assertEqual(resp_dist.status_code, 200)
        data_dist = resp_dist.json()
        for a in data_dist["alertas"]:
            self.assertIn("distribuição", a["modulo"].lower())

    def test_03_sin_overview_gold_connection_and_resumo(self):
        """Valida que o endpoint /sin/overview entrega a consolidação Gold kpi_sin_resumo."""
        response = self.client.get("/api/v1/sin/overview")
        self.assertEqual(response.status_code, 200)
        data = response.json()

        # Validação dos elementos essenciais
        self.assertIn("kpi_sin_resumo", data)
        self.assertIn("ear_atual", data)
        self.assertIn("ena_subsistemas", data)
        self.assertIn("cmo_atual", data)
        self.assertIn("ear_historico", data)
        self.assertIn("_metadata", data)

        resumo = data["kpi_sin_resumo"]
        self.assertGreater(len(resumo), 0, "kpi_sin_resumo não deve ser vazio")

        subsistemas_encontrados = {r["subsistema"] for r in resumo}
        self.assertTrue({"SE_CO", "S", "NE", "N"}.issubset(subsistemas_encontrados), 
                        f"Subsistemas incompletos em kpi_sin_resumo: {subsistemas_encontrados}")

        for r in resumo:
            self.assertIn("ear_percentual", r)
            self.assertIn("meta_seguranca_percentual", r)
            self.assertIn("folga_seguranca_ear_pct", r)
            self.assertIn("status_seguranca_energetica", r)
            self.assertIn("ena_percentual_mlt", r)
            self.assertIn("cmo_medio_rs_mwh", r)

    def test_04_bcb_sgs_client_macro_integration(self):
        """Valida o cliente BCB SGS para obtenção de Selic e IPCA em tempo real."""
        macro = bcb_client.get_macro_indicators(use_cache=False)
        self.assertIsNotNone(macro)
        self.assertIn("selic_meta_anual_pct", macro)
        self.assertIn("ipca_acumulado_12m_pct", macro)
        self.assertIn("wacc_nominal_estimado_pct", macro)
        
        self.assertGreater(macro["selic_meta_anual_pct"], 0.0)
        self.assertGreater(macro["ipca_acumulado_12m_pct"], 0.0)
        self.assertGreater(macro["wacc_nominal_estimado_pct"], 0.0)

        # Equação de Fisher: WACC nominal deve ser estritamente superior ao WACC real de 7.32%
        self.assertGreater(macro["wacc_nominal_estimado_pct"], 7.32)

    def test_05_financeiro_overview_and_macro_endpoint(self):
        """Valida a exposição dos indicadores macroeconômicos no financeiro e PRORET."""
        # Teste do endpoint /macro
        resp_macro = self.client.get("/api/v1/financeiro-proret/macro")
        self.assertEqual(resp_macro.status_code, 200)
        m_data = resp_macro.json()
        self.assertIn("selic_meta_anual_pct", m_data)
        self.assertIn("ipca_acumulado_12m_pct", m_data)

        # Teste do endpoint /overview
        resp_ov = self.client.get("/api/v1/financeiro-proret/overview")
        self.assertEqual(resp_ov.status_code, 200)
        ov_data = resp_ov.json()
        self.assertIn("macro_indicadores", ov_data)
        self.assertIn("indicadores_setoriais", ov_data)
        
        ind_setor = ov_data["indicadores_setoriais"]
        self.assertIn("selic_vigente_pct", ind_setor)
        self.assertIn("ipca_acumulado_12m_pct", ind_setor)
        self.assertIn("wacc_nominal_estimado_pct", ind_setor)

    def test_06_proret_simulation_with_macro_parameters(self):
        """Valida o cálculo do simulador tarifário PRORET integrando variáveis macroeconômicas."""
        payload = {
            "distribuidora": "CPFL Paulista",
            "brr_liquida_rs_mm": 14200.0,
            "wacc_regulatorio_pct": 7.32,
            "opex_eficiente_rs_mm": 2150.0,
            "fator_x_pct": 0.85,
            "componente_q_pct": -0.15,
            "mercado_faturado_gwh": 28500.0,
            "custos_parcela_a_rs_mm": 5800.0,
            "taxa_selic_pct": 13.75,
            "inflacao_ipca_pct": 4.22
        }
        response = self.client.post("/api/v1/financeiro-proret/simulate", json=payload)
        self.assertEqual(response.status_code, 200)
        sim = response.json()
        
        self.assertGreater(sim["receita_requerida_total_rs_mm"], 0)
        self.assertGreater(sim["tarifa_media_rs_mwh"], 0)
        self.assertIn("wacc_nominal_pct", sim)
        self.assertIn("taxa_selic_vigente_pct", sim)
        self.assertIn("inflacao_ipca_vigente_pct", sim)
        self.assertEqual(sim["taxa_selic_vigente_pct"], 13.75)
        self.assertEqual(sim["inflacao_ipca_vigente_pct"], 4.22)
        # Fisher check: (1 + 0.0732) * (1 + 0.0422) - 1 = 11.85%
        self.assertAlmostEqual(sim["wacc_nominal_pct"], 11.85, delta=0.1)

    def test_07_cloud_scheduler_hydrology_script_verification(self):
        """Valida que o job do Cloud Scheduler para a hidrologia do SIN está formalmente registrado."""
        scheduler_script_path = os.path.join(backend_dir, "..", "pipelines", "infrastructure", "setup_cloud_scheduler.sh")
        self.assertTrue(os.path.exists(scheduler_script_path), "Script setup_cloud_scheduler.sh não encontrado!")
        
        with open(scheduler_script_path, "r", encoding="utf-8") as f:
            content = f.read()

        self.assertIn("ons-sin-hidrologia-diario", content)
        self.assertIn("/api/v1/ingestion/sin/run", content)
        self.assertIn("0 5 * * *", content)

    def test_08_graceful_fallback_when_bigquery_offline(self):
        """Garante que todos os endpoints operam perfeitamente em fallback quando o BigQuery está offline."""
        original_client = bq_manager.client
        try:
            # Simular desconexão do BigQuery
            bq_manager.client = None
            cache.clear()

            # 1. Alertas
            r_alerts = self.client.get("/api/v1/alerts/")
            self.assertEqual(r_alerts.status_code, 200)
            self.assertGreater(r_alerts.json()["total"], 0)
            self.assertEqual(r_alerts.json()["_metadata"]["source"], "seed_fallback")

            # 2. SIN Overview
            r_sin = self.client.get("/api/v1/sin/overview")
            self.assertEqual(r_sin.status_code, 200)
            self.assertGreater(len(r_sin.json()["kpi_sin_resumo"]), 0)
            self.assertEqual(r_sin.json()["_metadata"]["source"], "seed_fallback")

            # 3. Financeiro PRORET
            r_fin = self.client.get("/api/v1/financeiro-proret/overview")
            self.assertEqual(r_fin.status_code, 200)
            self.assertIn("macro_indicadores", r_fin.json())

        finally:
            bq_manager.client = original_client
            cache.clear()


if __name__ == "__main__":
    unittest.main()
