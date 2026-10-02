"""
Suíte de Testes Programáticos - Sprint 2: Lakehouse do Setor Elétrico Brasileiro.

Validações:
1. Ingestor oficial de Transmissão ANEEL (pipelines/ingestion/aneel_transmissao_ingestor.py):
   - Ingestão, cálculo de RAP homologada, PVd e status regulatório
   - Concessionárias de referência: ISA CTEEP, TAESA, Furnas, Alupar, etc.
   - Tabela Silver e Gold (kpi_transmissao_concessoes)
2. Ingestor de Atendimento Comercial ANEEL (pipelines/ingestion/aneel_comercial_ingestor.py):
   - Cumprimento de SLAs da REN nº 1.000/2021 (ligação, religação, ressarcimento)
   - Canais de atendimento telefônico (INS, Abandono IAb, TMA)
3. Endpoints da API FastAPI com TestClient:
   - GET /api/v1/transmissao/overview (com e sem BigQuery live / Graceful Fallback)
   - GET /api/v1/atendimento/overview (com e sem BigQuery live / Graceful Fallback)
   - POST /api/v1/ingestion/datalake/transmissao/run
   - POST /api/v1/ingestion/datalake/comercial/run
   - GET /api/v1/ingestion/datalake/status
4. Orquestração Serverless:
   - Configuração dos Jobs no Cloud Scheduler (setup_cloud_scheduler.sh)
"""

import os
import unittest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient

# Certifica que o PYTHONPATH alcança backend e pipelines
import sys
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)
BACKEND_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BACKEND_DIR not in sys.path:
    sys.path.insert(0, BACKEND_DIR)

from app.main import app
from app.core.bigquery_client import bq_manager
from app.data.local_cache import cache
from pipelines.ingestion.aneel_transmissao_ingestor import run_transmissao_pipeline, compute_status_operacional
from pipelines.ingestion.aneel_comercial_ingestor import run_comercial_pipeline


class TestSprint2Lakehouse(unittest.TestCase):
    def setUp(self):
        cache.clear()
        self.client = TestClient(app)

    def tearDown(self):
        cache.clear()

    # =========================================================================
    # 1. TESTES DO INGESTOR DE TRANSMISSÃO (CKAN ANEEL)
    # =========================================================================
    def test_transmissao_ingestor_execution(self):
        """Valida execução da pipeline de transmissão, gerando Silver e Gold."""
        result = run_transmissao_pipeline()
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["domain"], "transmissao")
        self.assertIn("kpi_transmissao_concessoes", result["gold_table"])
        self.assertGreaterEqual(result["records"], 6)

        concessionarias = result["concessionarias"]
        nomes = [c["concessionaria"] for c in concessionarias]
        
        # Validar grandes players nacionais
        self.assertIn("ISA CTEEP", nomes)
        self.assertIn("TAESA", nomes)
        self.assertIn("ELETROBRAS FURNAS", nomes)
        self.assertIn("ALUPAR", nomes)

        # Validar campos regulatórios essenciais
        for c in concessionarias:
            self.assertIn("rap_homologada_rs_mm", c)
            self.assertIn("pvd_rs_mm", c)
            self.assertIn("disponibilidade_pct", c)
            self.assertIn("status", c)
            self.assertGreater(c["rap_homologada_rs_mm"], 0.0)
            self.assertGreaterEqual(c["disponibilidade_pct"], 99.0)

        # Validar KPIs resumo nacionais
        resumo = result["kpis_resumo"]
        self.assertGreater(resumo["rap_total_nacional_rs_mm"], 20000.0)
        self.assertGreater(resumo["pvd_total_ano_rs_mm"], 50.0)
        self.assertGreaterEqual(resumo["disponibilidade_media_linhas_pct"], 99.8)

    def test_transmissao_status_operacional_logic(self):
        """Valida a regra de negócio regulatória de status operacional de transmissão."""
        self.assertEqual(compute_status_operacional(0.25, 99.95), "Excelente")
        self.assertEqual(compute_status_operacional(0.60, 99.88), "Conforme")
        self.assertEqual(compute_status_operacional(1.10, 99.80), "Atenção")
        self.assertEqual(compute_status_operacional(2.50, 99.70), "Crítico")

    # =========================================================================
    # 2. TESTES DO INGESTOR DE ATENDIMENTO COMERCIAL (REN 1.000/2021)
    # =========================================================================
    def test_comercial_ingestor_execution(self):
        """Valida execução da pipeline de atendimento comercial e cumprimento de SLAs."""
        result = run_comercial_pipeline()
        
        self.assertEqual(result["status"], "success")
        self.assertEqual(result["domain"], "atendimento_comercial")
        self.assertGreaterEqual(result["records_slas"], 5)
        self.assertGreaterEqual(result["records_canais"], 5)

        # Validar SLAs da REN 1.000
        slas = result["slas_comerciais"]
        servicos = [s["servico"] for s in slas]
        self.assertTrue(any("Ligação Nova Urbana" in s for s in servicos))
        self.assertTrue(any("Religação Normal Urbana" in s for s in servicos))
        self.assertTrue(any("Religação de Urgência" in s for s in servicos))
        self.assertTrue(any("Ressarcimento" in s for s in servicos))

        for s in slas:
            self.assertIn("cumprimento_pct", s)
            self.assertIn("sla_regulatorio_valor", s)
            self.assertGreater(s["cumprimento_pct"], 80.0)

        # Validar Canais de Atendimento
        canais = result["canais_atendimento"]
        self.assertIn("ins_medio_nacional_pct", canais)
        self.assertIn("iab_medio_nacional_pct", canais)
        self.assertIn("tma_medio_segundos", canais)
        self.assertGreater(canais["ins_medio_nacional_pct"], 80.0)

    # =========================================================================
    # 3. TESTES DOS ENDPOINTS DA API & GRACEFUL FALLBACK
    # =========================================================================
    def test_endpoint_transmissao_overview_fallback(self):
        """Valida que /api/v1/transmissao/overview responde com sucesso em modo fallback SEED_DATA."""
        cache.clear()
        response = self.client.get("/api/v1/transmissao/overview")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("kpis_resumo", data)
        self.assertIn("concessionarias", data)
        self.assertIn("desligamentos_recentes", data)
        self.assertIn("_metadata", data)
        self.assertGreaterEqual(len(data["concessionarias"]), 4)
        
        # Validar integridade dos dados da CTEEP e TAESA
        nomes = [c["nome"] for c in data["concessionarias"]]
        self.assertTrue(any("CTEEP" in n for n in nomes))
        self.assertTrue(any("TAESA" in n for n in nomes))

    def test_endpoint_transmissao_overview_with_gold_mock(self):
        """Valida a conexão viva do endpoint /api/v1/transmissao/overview à Camada Gold do BigQuery."""
        cache.clear()
        mock_gold_rows = [
            {
                "nome": "ISA CTEEP MOCK",
                "sigla": "ISA_CTEEP",
                "holding": "CTEEP",
                "ano_ciclo": "2025-2026",
                "rap_homologada_rs_mm": 5420.0,
                "pvd_rs_mm": 24.5,
                "pvd_sobre_rap_pct": 0.452,
                "disponibilidade_pct": 99.91,
                "ens_mwh": 180.2,
                "extensao_km": 21800.0,
                "status": "Excelente",
                "ranking_eficiencia": 1
            },
            {
                "nome": "TAESA MOCK",
                "sigla": "TAESA",
                "holding": "Transmissora Aliança",
                "ano_ciclo": "2025-2026",
                "rap_homologada_rs_mm": 3890.0,
                "pvd_rs_mm": 14.2,
                "pvd_sobre_rap_pct": 0.365,
                "disponibilidade_pct": 99.94,
                "ens_mwh": 95.0,
                "extensao_km": 14500.0,
                "status": "Excelente",
                "ranking_eficiencia": 2
            }
        ]

        mock_query_job = MagicMock()
        mock_query_job.result.return_value = mock_gold_rows
        
        mock_bq_client = MagicMock()
        mock_bq_client.query.return_value = mock_query_job

        orig_client = bq_manager.client
        try:
            bq_manager.client = mock_bq_client
            response = self.client.get("/api/v1/transmissao/overview")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            
            self.assertEqual(data["_metadata"]["source"], "bigquery_gold")
            self.assertEqual(len(data["concessionarias"]), 2)
            self.assertEqual(data["concessionarias"][0]["nome"], "ISA CTEEP MOCK")
            self.assertEqual(data["kpis_resumo"]["rap_total_nacional_rs_mm"], 9310.0)
            self.assertEqual(data["kpis_resumo"]["pvd_total_ano_rs_mm"], 38.7)
        finally:
            bq_manager.client = orig_client
            cache.clear()

    def test_endpoint_atendimento_overview_fallback(self):
        """Valida que /api/v1/atendimento/overview responde com sucesso em modo fallback."""
        cache.clear()
        response = self.client.get("/api/v1/atendimento/overview")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        self.assertIn("ranking_iasc", data)
        self.assertIn("canais_atendimento", data)
        self.assertIn("slas_comerciais", data)
        self.assertIn("ouvidoria_aneel", data)
        self.assertIn("_metadata", data)
        self.assertGreaterEqual(len(data["slas_comerciais"]), 3)

    def test_endpoint_atendimento_overview_with_gold_mock(self):
        """Valida a conexão viva do endpoint /api/v1/atendimento/overview com as tabelas Gold."""
        cache.clear()
        mock_slas_rows = [
            {
                "servico": "Ligação Nova Urbana (Grupo B)",
                "sigla_indicador": "LIG_URB_B",
                "artigo_ren_1000": "Art. 31",
                "unidade_sla": "dias",
                "sla_aneel_valor": 2.0,
                "tempo_medio": 1.5,
                "cumprimento_pct": 97.5,
                "total_solicitacoes": 100000,
                "solicitacoes_violadas": 2500,
                "compensacao_paga_rs_mm": 0.90,
                "status": "Conforme"
            }
        ]
        mock_canais_rows = [
            {
                "distribuidora": "CPFL_PAULISTA",
                "nome_concessionaria": "CPFL Paulista",
                "ins_pct": 93.0,
                "iab_pct": 1.5,
                "tma_s": 120.0,
                "status": "Conforme"
            }
        ]
        mock_iasc_rows = [
            {
                "posicao": 1,
                "distribuidora": "CPFL_PAULISTA",
                "score": 85.0,
                "total_reclamacoes": 1200,
                "procedencia_pct": 12.0,
                "tempo_medio_resolucao_dias": 3.5,
                "classificacao_satisfacao": "Alta Satisfação (Excelente)"
            }
        ]

        def query_side_effect(sql):
            mock_res = MagicMock()
            if "kpi_ouvidoria_satisfacao" in sql:
                mock_res.result.return_value = mock_iasc_rows
            elif "kpi_atendimento_slas_comerciais" in sql:
                mock_res.result.return_value = mock_slas_rows
            elif "kpi_atendimento_canais" in sql:
                mock_res.result.return_value = mock_canais_rows
            else:
                mock_res.result.return_value = []
            return mock_res

        mock_bq_client = MagicMock()
        mock_bq_client.query.side_effect = query_side_effect

        orig_client = bq_manager.client
        try:
            bq_manager.client = mock_bq_client
            response = self.client.get("/api/v1/atendimento/overview")
            self.assertEqual(response.status_code, 200)
            data = response.json()
            
            self.assertEqual(data["_metadata"]["source"], "bigquery_gold")
            self.assertEqual(len(data["slas_comerciais"]), 1)
            self.assertEqual(data["slas_comerciais"][0]["sla_aneel_dias"], 2.0)
            self.assertEqual(data["canais_atendimento"]["ins_medio_nacional_pct"], 93.0)
        finally:
            bq_manager.client = orig_client
            cache.clear()

    # =========================================================================
    # 4. TESTES DE ROTAS DE INGESTÃO (DATA LAKEHOUSE)
    # =========================================================================
    def test_ingestion_datalake_transmissao_run(self):
        """Valida o endpoint POST /api/v1/ingestion/datalake/transmissao/run."""
        response = self.client.post("/api/v1/ingestion/datalake/transmissao/run")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["domain"], "transmissao")
        self.assertGreaterEqual(data["records"], 6)

    def test_ingestion_datalake_comercial_run(self):
        """Valida o endpoint POST /api/v1/ingestion/datalake/comercial/run."""
        response = self.client.post("/api/v1/ingestion/datalake/comercial/run")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["domain"], "atendimento_comercial")
        self.assertGreaterEqual(data["records_slas"], 5)

    def test_ingestion_datalake_status_includes_transmissao_and_comercial(self):
        """Valida que o status do lakehouse inclui domínios e tabelas da Sprint 2."""
        response = self.client.get("/api/v1/ingestion/datalake/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        bronze_domains = data["bronze_layer"]["domains"]
        self.assertIn("transmissao", bronze_domains)
        self.assertIn("atendimento_comercial", bronze_domains)

    # =========================================================================
    # 5. TESTES DE CONFIGURAÇÃO DO CLOUD SCHEDULER
    # =========================================================================
    def test_cloud_scheduler_script_has_all_jobs(self):
        """Verifica se setup_cloud_scheduler.sh registra os novos jobs no Cloud Scheduler."""
        script_path = os.path.join(BASE_DIR, "pipelines", "infrastructure", "setup_cloud_scheduler.sh")
        self.assertTrue(os.path.exists(script_path), "Arquivo setup_cloud_scheduler.sh não encontrado.")
        
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Job Transmissão
        self.assertIn("aneel-transmissao-mensal", content)
        self.assertIn("/api/v1/ingestion/datalake/transmissao/run", content)

        # Job Atendimento Comercial
        self.assertIn("aneel-comercial-mensal", content)
        self.assertIn("/api/v1/ingestion/datalake/comercial/run", content)

        # 10 Jobs
        self.assertIn("10 Jobs do Cloud Scheduler", content)


if __name__ == "__main__":
    unittest.main()
