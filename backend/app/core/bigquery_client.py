import logging
from typing import Any, Dict, List, Optional
from google.cloud import bigquery
from google.auth.exceptions import DefaultCredentialsError
from app.core.config import settings
from app.data.seed_data import SEED_DATA
from app.data.local_cache import cache

logger = logging.getLogger("bigquery_client")

class BigQueryManager:
    def __init__(self):
        self.project_id = settings.GCP_PROJECT_ID
        self.client: Optional[bigquery.Client] = None
        self._init_client()

    def _init_client(self):
        try:
            client_candidate = bigquery.Client(project=self.project_id)
            # Test credentials
            list(client_candidate.list_datasets(max_results=1))
            self.client = client_candidate
            logger.info(f"Connected to BigQuery with default credentials: {self.project_id}")
        except Exception as e:
            try:
                import subprocess
                from google.oauth2 import credentials
                token = subprocess.check_output(["gcloud", "auth", "print-access-token"], timeout=10).decode().strip().split()[-1]
                creds = credentials.Credentials(token)
                self.client = bigquery.Client(project=self.project_id, credentials=creds)
                logger.info(f"Connected to BigQuery via active gcloud session token: {self.project_id}")
            except Exception as e2:
                logger.warning(f"Could not connect to live BigQuery for project {self.project_id} ({e} / {e2}). Operating in resilient simulated/cached mode.")
                self.client = None

    def query(self, sql: str, fallback_key: Optional[str] = None, use_cache: bool = True) -> Any:
        cache_key = f"bq_query_{hash(sql)}"
        if use_cache:
            cached_res = cache.get(cache_key)
            if cached_res is not None:
                return cached_res

        if self.client:
            try:
                query_job = self.client.query(sql)
                results = [dict(row) for row in query_job.result()]
                if use_cache:
                    cache.set(cache_key, results)
                return results
            except Exception as e:
                logger.error(f"BigQuery live query error: {e}. Utilizing fallback data.")

        # Fallback to local curated sector data
        if fallback_key and fallback_key in SEED_DATA:
            val = SEED_DATA[fallback_key]
            if use_cache:
                cache.set(cache_key, val)
            return val

        return []

    def get_domain_data(self, domain: str) -> Any:
        cache_key = f"domain_{domain}"
        cached_val = cache.get(cache_key)
        if cached_val is not None:
            return cached_val

        # Obter dados base do seed como baseline
        data = dict(SEED_DATA.get(domain, {}))
        source_mode = "seed_fallback"

        # Se o cliente BigQuery estiver ativo, sobrepõe com a Camada Gold ao vivo
        if self.client:
            try:
                if domain == "distribuicao_qualidade":
                    sql = f"""
                    SELECT 
                      distribuidora, 
                      nome_concessionaria as nome, 
                      sigla_uf as uf, 
                      dec_apurado_horas as dec, 
                      dec_limite_aneel_horas as meta_dec, 
                      fec_apurado_vezes as fec, 
                      fec_limite_aneel_vezes as meta_fec, 
                      status_regulatorio as status, 
                      compensacao_estimada_rs_mm as compensacao_rs_mm
                    FROM `{self.project_id}.gold_kpis.kpi_dec_fec_conformidade`
                    ORDER BY dec_apurado_horas ASC
                    """
                    rows = [dict(row) for row in self.client.query(sql).result()]
                    if rows:
                        data["ranking_dec_fec"] = rows
                        source_mode = "bigquery_gold"

                elif domain == "perdas_mmgd":
                    sql = f"""
                    SELECT 
                      sigla_uf as uf, 
                      potencia_instalada_mw as potencia_mw, 
                      total_conexoes as conexoes 
                    FROM `{self.project_id}.gold_kpis.kpi_mmgd_expansao_uf`
                    ORDER BY potencia_instalada_mw DESC
                    """
                    rows = [dict(row) for row in self.client.query(sql).result()]
                    if rows:
                        if "mmgd_estatisticas" in data:
                            data["mmgd_estatisticas"] = dict(data["mmgd_estatisticas"])
                            data["mmgd_estatisticas"]["ranking_estados_gd"] = rows
                            data["mmgd_estatisticas"]["top_ufs_potencia_mw"] = rows
                            total_mw = sum(r.get("potencia_mw", 0) for r in rows)
                            total_conexoes = sum(r.get("conexoes", 0) for r in rows)
                            if total_mw > 0:
                                data["mmgd_estatisticas"]["potencia_instalada_total_gw"] = round(total_mw / 1000.0, 1)
                            if total_conexoes > 0:
                                data["mmgd_estatisticas"]["qtd_unidades_consumidoras_gd"] = total_conexoes
                        source_mode = "bigquery_gold"

                elif domain == "atendimento_cliente":
                    sql = f"""
                    SELECT 
                      ranking_iasc as posicao, 
                      distribuidora, 
                      score_iasc as score,
                      total_reclamacoes,
                      procedencia_pct,
                      tempo_medio_resolucao_dias,
                      classificacao_satisfacao
                    FROM `{self.project_id}.gold_kpis.kpi_ouvidoria_satisfacao`
                    ORDER BY ranking_iasc ASC
                    """
                    rows = [dict(row) for row in self.client.query(sql).result()]
                    if rows:
                        friendly_names = {
                            "CPFL_PAULISTA": "CPFL Paulista", "ENEL_SP": "Enel São Paulo",
                            "CEMIG_D": "Cemig", "COPEL_DIS": "Copel", "CELESC": "Celesc",
                            "RGE_SUL": "RGE Sul", "LIGHT": "Light", "NEOENERGIA_COELBA": "Neoenergia Coelba",
                            "EQUATORIAL_GO": "Equatorial GO", "EQUATORIAL_PA": "Equatorial PA"
                        }
                        for r in rows:
                            r["nome_exibicao"] = friendly_names.get(r["distribuidora"], r["distribuidora"])
                            r["porte"] = "Grande"
                        data["ranking_iasc"] = rows
                        source_mode = "bigquery_gold"

                elif domain == "financeiro_proret":
                    sql = f"""
                    SELECT 
                      distribuidora, concessionaria, uf, resolucao_homologatoria, 
                      data_vigencia, tarifa_b1_rs_kwh, tusd_rs_mwh, te_rs_mwh, 
                      share_tusd_fio_pct, share_te_energia_pct,
                      tarifa_b2_rural_rs_kwh, tarifa_b3_comercial_rs_kwh,
                      a4_verde_demanda_rs_kw, a4_verde_energia_fora_ponta_rs_mwh,
                      wacc_regulatorio_pct, fator_x_pct, 
                      ranking_tarifa_mais_barata, ranking_tarifa_comercial, ranking_demanda_industrial_a4
                    FROM `{self.project_id}.gold_kpis.kpi_tarifas_ranking`
                    ORDER BY ranking_tarifa_mais_barata ASC
                    """
                    rows = [dict(row) for row in self.client.query(sql).result()]
                    if rows:
                        data["ranking_tarifario_aneel"] = rows
                        source_mode = "bigquery_gold"

            except Exception as e:
                logger.warning(f"Erro ao consultar Camada Gold para '{domain}': {e}. Mantendo dados de contingência.")
                source_mode = "seed_fallback"

        data["_metadata"] = {
            "source": source_mode,
            "project_id": self.project_id,
            "gold_dataset": "gold_kpis",
            "bi_engine_accelerated": True if source_mode == "bigquery_gold" else False
        }

        cache.set(cache_key, data)
        return data

bq_manager = BigQueryManager()
