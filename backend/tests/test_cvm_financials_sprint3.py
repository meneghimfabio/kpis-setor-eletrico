"""
Suíte de Testes Programáticos Automatizados (Sprint 3):
1. Ingestor CVM DFP/ITR (Bronze -> Silver -> Gold)
2. Extração de métricas auditadas (Receita, EBITDA, Margem EBITDA, Lucro Líquido, Dívida Líquida, CAPEX)
3. Conexão e contrato de dados da rota /api/v1/financeiro-proret/overview via FastAPI TestClient
4. Resiliência e Graceful Fallback para SEED_DATA na ausência do BigQuery
5. Endpoints de Ingestão CVM e Registro no Cloud Scheduler
"""

import os
import sys
import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

# Garante inclusão de diretórios no sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from app.main import app
from app.data.local_cache import cache
from app.core.bigquery_client import bq_manager
from pipelines.ingestion.cvm_dre_ingestor import (
    CVMFinancialsIngestor,
    TARGET_COMPANIES,
    AUDITED_CVM_BASELINE,
    run_cvm_pipeline
)
from pipelines.dataform.run_transformations import SQL_CVM_DRE


class TestCVMSprint3Execution(unittest.TestCase):

    def setUp(self):
        self.client = TestClient(app)
        cache.clear()

    def test_target_companies_definition(self):
        """Verifica se todas as 8 companhias solicitadas estão registradas com metadados CVM."""
        expected_keys = {"CPFL", "CEMIG", "COPEL", "TAESA", "CTEEP", "EQUATORIAL", "NEOENERGIA", "ELETROBRAS"}
        self.assertEqual(set(TARGET_COMPANIES.keys()), expected_keys)
        
        for key, meta in TARGET_COMPANIES.items():
            self.assertIn("empresa", meta)
            self.assertIn("ticker", meta)
            self.assertIn("codigo_cvm", meta)
            self.assertIn("cnpj", meta)
            self.assertIn("segmento", meta)
            self.assertIn("auditor", meta)

    def test_cvm_ingestor_dataframe_and_audited_kpis(self):
        """
        Valida que o ingestor extrai exatamente os KPIs contábeis auditados:
        Receita Líquida, EBITDA, Margem EBITDA, Lucro Líquido, Dívida Líquida e CAPEX.
        """
        ingestor = CVMFinancialsIngestor()
        df = ingestor.get_audited_financials_dataframe(year=2025)
        
        self.assertEqual(len(df), 8)
        required_cols = [
            "empresa", "ticker", "codigo_cvm", "cnpj", "segmento",
            "receita_liquida_rs_mm", "ebitda_rs_mm", "margem_ebitda_pct",
            "lucro_liquido_rs_mm", "divida_liquida_rs_mm", "capex_rs_mm",
            "alavancagem", "ano_referencia", "tipo_demonstrativo", "status_auditoria"
        ]
        for col in required_cols:
            self.assertIn(col, df.columns, f"Coluna obrigatória ausente: {col}")

        # Assertions de sanidade contábil e consistência matemática
        for _, row in df.iterrows():
            self.assertGreater(row["receita_liquida_rs_mm"], 0, f"Receita inválida para {row['empresa']}")
            self.assertGreater(row["ebitda_rs_mm"], 0, f"EBITDA inválido para {row['empresa']}")
            self.assertGreater(row["margem_ebitda_pct"], 0, f"Margem inválida para {row['empresa']}")
            self.assertLessEqual(row["margem_ebitda_pct"], 100.0, f"Margem superior a 100% para {row['empresa']}")
            self.assertGreater(row["lucro_liquido_rs_mm"], 0, f"Lucro Líquido inválido para {row['empresa']}")
            self.assertGreater(row["divida_liquida_rs_mm"], 0, f"Dívida Líquida inválida para {row['empresa']}")
            self.assertGreater(row["capex_rs_mm"], 0, f"CAPEX inválido para {row['empresa']}")
            self.assertGreater(row["alavancagem"], 0, f"Alavancagem inválida para {row['empresa']}")

        # Validação específica da Eletrobras (recém-adicionada)
        eletrobras_row = df[df["ticker"] == "ELET3"].iloc[0]
        self.assertEqual(eletrobras_row["empresa"], "Eletrobras")
        self.assertGreater(eletrobras_row["receita_liquida_rs_mm"], 30000.0)
        self.assertGreater(eletrobras_row["ebitda_rs_mm"], 15000.0)

    def test_run_cvm_pipeline_execution(self):
        """Valida a execução ponta a ponta do método run_cvm_pipeline."""
        res = run_cvm_pipeline(year=2025)
        self.assertEqual(res["status"], "success")
        self.assertEqual(res["domain"], "cvm_dre_empresas")
        self.assertEqual(res["records_processed"], 8)
        self.assertIn("gold_table", res)
        self.assertIn("kpi_financeiro_dre_empresas", res["gold_table"])
        self.assertEqual(len(res["companies"]), 8)

    def test_gold_sql_transformation_definition(self):
        """Verifica a integridade da query Dataform para criação da tabela Gold."""
        self.assertIn("gold_kpis.kpi_financeiro_dre_empresas", SQL_CVM_DRE)
        self.assertIn("aneel_silver.cvm_dre_empresas", SQL_CVM_DRE)
        self.assertIn("receita_liquida_rs_mm", SQL_CVM_DRE)
        self.assertIn("ebitda_rs_mm", SQL_CVM_DRE)
        self.assertIn("lucro_liquido_rs_mm", SQL_CVM_DRE)
        self.assertIn("divida_liquida_rs_mm", SQL_CVM_DRE)
        self.assertIn("capex_rs_mm", SQL_CVM_DRE)
        self.assertIn("alavancagem", SQL_CVM_DRE)

    def test_financeiro_overview_endpoint_contract(self):
        """
        Valida que a rota /api/v1/financeiro-proret/overview retorna:
        - As 8 companhias abertas com todas as métricas exigidas
        - Indicadores setoriais consolidados
        - Graceful Fallback para SEED_DATA se BQ offline
        """
        cache.clear()
        response = self.client.get("/api/v1/financeiro-proret/overview")
        self.assertEqual(response.status_code, 200)
        
        data = response.json()
        self.assertIn("empresas_dre", data)
        self.assertIn("indicadores_setoriais", data)
        self.assertIn("_metadata", data)
        
        empresas = data["empresas_dre"]
        self.assertEqual(len(empresas), 8)
        
        # Confere se todas as empresas alvo estão na lista
        nomes_empresas = [e["empresa"] for e in empresas]
        self.assertTrue(any("CPFL" in n for n in nomes_empresas))
        self.assertTrue(any("Cemig" in n for n in nomes_empresas))
        self.assertTrue(any("Copel" in n for n in nomes_empresas))
        self.assertTrue(any("CTEEP" in n for n in nomes_empresas))
        self.assertTrue(any("TAESA" in n for n in nomes_empresas))
        self.assertTrue(any("Equatorial" in n for n in nomes_empresas))
        self.assertTrue(any("Neoenergia" in n for n in nomes_empresas))
        self.assertTrue(any("Eletrobras" in n for n in nomes_empresas))

        # Confere campos contábeis no item
        first_emp = empresas[0]
        for field in ["receita_liquida_rs_mm", "ebitda_rs_mm", "margem_ebitda_pct", "lucro_liquido_rs_mm", "capex_rs_mm", "alavancagem"]:
            self.assertIn(field, first_emp)

        # Confere indicadores setoriais
        ind = data["indicadores_setoriais"]
        self.assertGreater(ind.get("ebitda_total_setor_rs_mm", 0), 50000)
        self.assertGreater(ind.get("receita_total_setor_rs_mm", 0), 100000)

    def test_graceful_fallback_mode(self):
        """
        Garante que quando o BigQuery não estiver disponível, o sistema opera
        transparentemente com o fallback de SEED_DATA e define source = seed_fallback.
        """
        cache.clear()
        with patch.object(bq_manager, "client", None):
            res_data = bq_manager.get_domain_data("financeiro_proret")
            self.assertEqual(len(res_data["empresas_dre"]), 8)
            self.assertEqual(res_data["_metadata"]["source"], "seed_fallback")

    def test_bigquery_gold_overlay_mode(self):
        """
        Garante que quando o BigQuery retornar dados da Camada Gold,
        eles sobrepõem os dados e atualizam source para bigquery_gold.
        """
        cache.clear()
        mock_bq = MagicMock()
        mock_row = {
            "empresa": "Eletrobras (Live Gold)",
            "ticker": "ELET3",
            "codigo_cvm": "002437",
            "receita_liquida_rs_mm": 38000.0,
            "ebitda_rs_mm": 20000.0,
            "margem_ebitda_pct": 52.6,
            "lucro_liquido_rs_mm": 4500.0,
            "divida_liquida_rs_mm": 41000.0,
            "capex_rs_mm": 6200.0,
            "alavancagem": 2.05,
            "segmento": "Maior Geradora e Transmissora do Brasil",
            "status_auditoria": "Auditado (PwC)",
            "ano_referencia": 2025
        }
        mock_bq.query.return_value.result.return_value = [mock_row]

        with patch.object(bq_manager, "client", mock_bq):
            res_data = bq_manager.get_domain_data("financeiro_proret")
            self.assertEqual(res_data["_metadata"]["source"], "bigquery_gold")
            self.assertEqual(res_data["empresas_dre"][0]["empresa"], "Eletrobras (Live Gold)")

    def test_ingestion_api_endpoints(self):
        """Testa as rotas de API da ingestão CVM."""
        # 1. Status
        res_status = self.client.get("/api/v1/ingestion/cvm/status")
        self.assertEqual(res_status.status_code, 200)

        # 2. Trigger run
        res_run = self.client.post("/api/v1/ingestion/cvm/run")
        self.assertEqual(res_run.status_code, 200)
        self.assertIn("Ingestao CVM DFP/ITR concluida com sucesso.", res_run.json()["message"])

        # 3. Trigger datalake cvm
        res_dl_cvm = self.client.post("/api/v1/ingestion/datalake/cvm/run")
        self.assertEqual(res_dl_cvm.status_code, 200)
        self.assertEqual(res_dl_cvm.json()["status"], "success")

    def test_cloud_scheduler_script_contains_cvm_job(self):
        """Valida que o job do Cloud Scheduler para a CVM está registrado no script de automação."""
        script_path = os.path.join(ROOT_DIR, "pipelines", "infrastructure", "setup_cloud_scheduler.sh")
        self.assertTrue(os.path.exists(script_path), f"Script não encontrado: {script_path}")
        
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()
            
        self.assertIn("cvm-dre-financeiro", content)
        self.assertIn("/api/v1/ingestion/cvm/run", content)
        self.assertIn("Jobs do Cloud Scheduler foram configurados com sucesso", content)


if __name__ == "__main__":
    unittest.main()
