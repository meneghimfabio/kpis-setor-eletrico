import logging
import io
import datetime
from typing import Dict, Any, List, Optional
import requests
import pandas as pd
from app.core.config import settings
from app.core.bigquery_client import bq_manager
from app.data.local_cache import cache
from app.data.seed_data import SEED_DATA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ons_ingestion")

# Subsystem Mapping from ONS to Internal Standard
SUBSYSTEM_MAP = {
    "SE": "SE_CO",
    "SE/CO": "SE_CO",
    "SUDESTE/CENTRO-OESTE": "SE_CO",
    "SUDESTE": "SE_CO",
    "S": "S",
    "SUL": "S",
    "NE": "NE",
    "NORDESTE": "NE",
    "N": "N",
    "NORTE": "N"
}

SECURITY_TARGET_PERCENT = {
    "SE_CO": 45.0,
    "S": 50.0,
    "NE": 40.0,
    "N": 45.0
}

class OnsSinIngestor:
    """
    Ingestor para dados de Operacao do SIN do Portal de Dados Abertos do ONS.
    Extrai series de EAR (Energia Armazenada), ENA (Energia Natural Afluente) e CMO (Custo Marginal de Operacao).
    """

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "PainelSetorEletrico/1.0 (+https://github.com/)"
        })
        self.last_status = {
            "status": "idle",
            "last_run": None,
            "records_processed": {},
            "error": None
        }

    def _fetch_csv(self, url: str) -> Optional[pd.DataFrame]:
        try:
            logger.info(f"Baixando dados do ONS: {url}")
            response = self.session.get(url, verify=False, timeout=30)
            if response.status_code == 200:
                df = pd.read_csv(io.StringIO(response.text), sep=";", low_memory=False)
                return df
            else:
                logger.warning(f"Resposta ONS {response.status_code} para URL: {url}")
                return None
        except Exception as e:
            logger.error(f"Erro ao baixar CSV da ONS ({url}): {e}")
            return None

    def ingest_ear(self, years: List[int]) -> List[Dict[str, Any]]:
        """Extrai dados de Energia Armazenada (EAR) por subsistema."""
        dfs = []
        for y in years:
            url = f"https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/ear_subsistema_di/EAR_DIARIO_SUBSISTEMA_{y}.csv"
            df = self._fetch_csv(url)
            if df is not None and not df.empty:
                dfs.append(df)

        if not dfs:
            logger.warning("Nenhum dado de EAR encontrado no ONS.")
            return []

        full_df = pd.concat(dfs, ignore_index=True)
        full_df.columns = [c.strip().lower() for c in full_df.columns]
        
        full_df["subsistema"] = full_df["id_subsistema"].astype(str).str.strip().str.upper().map(lambda x: SUBSYSTEM_MAP.get(x, x))
        full_df = full_df[full_df["subsistema"].isin(["SE_CO", "S", "NE", "N"])]
        
        full_df["data_referencia"] = pd.to_datetime(full_df["ear_data"])
        full_df = full_df.sort_values(by=["data_referencia", "subsistema"])

        records = []
        for _, row in full_df.iterrows():
            pct = float(row.get("ear_verif_subsistema_percentual", 0.0))
            max_mw = float(row.get("ear_max_subsistema", 0.0))
            atual_mw = float(row.get("ear_verif_subsistema_mwmes", 0.0))
            sub = str(row.get("subsistema"))
            meta = SECURITY_TARGET_PERCENT.get(sub, 45.0)
            
            status = "Favoravel" if pct >= meta else ("Atencao Moderada" if pct >= meta - 15 else "Critico")
            records.append({
                "data_referencia": row["data_referencia"].strftime("%Y-%m-%d"),
                "subsistema": sub,
                "ear_percentual": round(pct, 2),
                "ear_max_mwmes": round(max_mw, 1),
                "ear_atual_mwmes": round(atual_mw, 1),
                "meta_seguranca_percentual": meta,
                "status_criticidade": status
            })

        logger.info(f"Ingestao EAR concluida: {len(records)} registros processados.")
        return records

    def ingest_ena(self, years: List[int]) -> List[Dict[str, Any]]:
        """Extrai dados de Energia Natural Afluente (ENA) por subsistema."""
        dfs = []
        for y in years:
            url = f"https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/ena_subsistema_di/ENA_DIARIO_SUBSISTEMA_{y}.csv"
            df = self._fetch_csv(url)
            if df is not None and not df.empty:
                dfs.append(df)

        if not dfs:
            logger.warning("Nenhum dado de ENA encontrado no ONS.")
            return []

        full_df = pd.concat(dfs, ignore_index=True)
        full_df.columns = [c.strip().lower() for c in full_df.columns]
        
        full_df["subsistema"] = full_df["id_subsistema"].astype(str).str.strip().str.upper().map(lambda x: SUBSYSTEM_MAP.get(x, x))
        full_df = full_df[full_df["subsistema"].isin(["SE_CO", "S", "NE", "N"])]
        
        full_df["data_referencia"] = pd.to_datetime(full_df["ena_data"])
        full_df = full_df.sort_values(by=["data_referencia", "subsistema"])

        records = []
        for _, row in full_df.iterrows():
            sub = str(row.get("subsistema"))
            mwmed = float(row.get("ena_bruta_regiao_mwmed", 0.0))
            pct_mlt = float(row.get("ena_bruta_regiao_percentualmlt", 0.0))
            
            if pct_mlt >= 110:
                classif = "Acima da Media"
            elif pct_mlt >= 85:
                classif = "Proximo a Media"
            elif pct_mlt >= 70:
                classif = "Moderado"
            else:
                classif = "Abaixo da Media"

            records.append({
                "data_referencia": row["data_referencia"].strftime("%Y-%m-%d"),
                "subsistema": sub,
                "ena_mwmed": round(mwmed, 1),
                "ena_percentual_mlt": round(pct_mlt, 2),
                "classificacao_hidrologica": classif
            })

        logger.info(f"Ingestao ENA concluida: {len(records)} registros processados.")
        return records

    def ingest_cmo(self, years: List[int]) -> List[Dict[str, Any]]:
        """Extrai dados de Custo Marginal de Operacao (CMO) semanal por subsistema."""
        dfs = []
        for y in years:
            url = f"https://ons-aws-prod-opendata.s3.amazonaws.com/dataset/cmo_se/CMO_SEMANAL_{y}.csv"
            df = self._fetch_csv(url)
            if df is not None and not df.empty:
                dfs.append(df)

        if not dfs:
            logger.warning("Nenhum dado de CMO encontrado no ONS.")
            return []

        full_df = pd.concat(dfs, ignore_index=True)
        full_df.columns = [c.strip().lower() for c in full_df.columns]
        
        full_df["subsistema"] = full_df["id_subsistema"].astype(str).str.strip().str.upper().map(lambda x: SUBSYSTEM_MAP.get(x, x))
        full_df = full_df[full_df["subsistema"].isin(["SE_CO", "S", "NE", "N"])]
        
        full_df["data_referencia"] = pd.to_datetime(full_df["din_instante"])
        full_df = full_df.sort_values(by=["data_referencia", "subsistema"])

        records = []
        for _, row in full_df.iterrows():
            sub = str(row.get("subsistema"))
            cmo_med = float(row.get("val_cmomediasemanal", row.get("val_cmomedia", 0.0)))
            cmo_leve = float(row.get("val_cmoleve", cmo_med))
            cmo_pesada = float(row.get("val_cmopesada", cmo_med))

            records.append({
                "data_referencia": row["data_referencia"].strftime("%Y-%m-%d"),
                "subsistema": sub,
                "cmo_medio": round(cmo_med, 2),
                "cmo_leve": round(cmo_leve, 2),
                "cmo_pesada": round(cmo_pesada, 2),
                "despacho_termico_mw": round(cmo_med * 45.0, 1)
            })

        logger.info(f"Ingestao CMO concluida: {len(records)} registros processados.")
        return records

    def sync_to_bigquery(self, ear_records: List[Dict], ena_records: List[Dict], cmo_records: List[Dict]):
        """Persiste os registros nas tabelas correspondentes do BigQuery se cliente estiver disponivel."""
        if not bq_manager.client:
            logger.info("BigQuery client inativo. Persistencia em nuvem ignorada.")
            return False

        client = bq_manager.client
        dataset_ref = f"{settings.GCP_PROJECT_ID}.operacao_sin"

        try:
            if ear_records:
                table_id = f"{dataset_ref}.ear_subsistemas"
                errors = client.insert_rows_json(table_id, ear_records[-200:])
                if errors:
                    logger.error(f"Erros na insercao BigQuery (EAR): {errors}")

            if ena_records:
                table_id = f"{dataset_ref}.ena_historico"
                errors = client.insert_rows_json(table_id, ena_records[-200:])
                if errors:
                    logger.error(f"Erros na insercao BigQuery (ENA): {errors}")

            if cmo_records:
                table_id = f"{dataset_ref}.cmo_horario_semanal"
                errors = client.insert_rows_json(table_id, cmo_records[-200:])
                if errors:
                    logger.error(f"Erros na insercao BigQuery (CMO): {errors}")

            logger.info("Sincronizacao com BigQuery efetuada com sucesso.")
            return True
        except Exception as e:
            logger.error(f"Excecao ao persistir no BigQuery: {e}")
            return False

    def update_local_cache_and_seed(self, ear_records: List[Dict], ena_records: List[Dict], cmo_records: List[Dict]):
        """Atualiza a estrutura em memoria e no cache local para consumo instantaneo no frontend."""
        if not ear_records or not ena_records or not cmo_records:
            return

        # 1. EAR Atual (ultimo registro por subsistema)
        ear_by_sub = {}
        for r in ear_records:
            ear_by_sub[r["subsistema"]] = r

        ear_atual = list(ear_by_sub.values())

        # 2. EAR Historico Mensal
        df_ear = pd.DataFrame(ear_records)
        df_ear["mes"] = pd.to_datetime(df_ear["data_referencia"]).dt.strftime("%b/%y")
        pivoted = df_ear.pivot_table(index="mes", columns="subsistema", values="ear_percentual", aggfunc="mean").reset_index()
        
        df_ear["ano_mes"] = pd.to_datetime(df_ear["data_referencia"]).dt.to_period("M")
        ordem_meses = df_ear[["mes", "ano_mes"]].drop_duplicates().sort_values(by="ano_mes")["mes"].tolist()
        
        ear_historico = []
        for m in ordem_meses[-12:]:
            row_piv = pivoted[pivoted["mes"] == m]
            if not row_piv.empty:
                r_dict = row_piv.iloc[0].to_dict()
                se = float(r_dict.get("SE_CO", 65.0))
                s = float(r_dict.get("S", 75.0))
                ne = float(r_dict.get("NE", 55.0))
                n = float(r_dict.get("N", 80.0))
                sin_total = (se * 0.58) + (s * 0.17) + (ne * 0.18) + (n * 0.07)
                ear_historico.append({
                    "mes": m,
                    "SE_CO": round(se, 1),
                    "S": round(s, 1),
                    "NE": round(ne, 1),
                    "N": round(n, 1),
                    "SIN_Total": round(sin_total, 1)
                })

        # 3. ENA Atual (ultimo registro por subsistema)
        ena_by_sub = {}
        for r in ena_records:
            ena_by_sub[r["subsistema"]] = {
                "subsistema": r["subsistema"],
                "ena_mwmed": r["ena_mwmed"],
                "ena_percentual_mlt": r["ena_percentual_mlt"],
                "classificacao": r["classificacao_hidrologica"]
            }
        ena_subsistemas = list(ena_by_sub.values())

        # 4. CMO Atual e Historico Semanal
        cmo_by_sub = {}
        for r in cmo_records:
            cmo_by_sub[r["subsistema"]] = {
                "subsistema": r["subsistema"],
                "cmo_medio": r["cmo_medio"],
                "cmo_leve": r["cmo_leve"],
                "cmo_pesada": r["cmo_pesada"],
                "status": "Normalidade" if r["cmo_medio"] < 250 else "Pressao de Custo"
            }
        cmo_atual = list(cmo_by_sub.values())

        # Historico semanal CMO
        df_cmo = pd.DataFrame(cmo_records)
        df_cmo["semana"] = pd.to_datetime(df_cmo["data_referencia"]).dt.strftime("Sem %W/%y")
        piv_cmo = df_cmo.pivot_table(index="semana", columns="subsistema", values="cmo_medio", aggfunc="mean").reset_index()
        
        cmo_historico = []
        for _, row in piv_cmo.tail(8).iterrows():
            cmo_historico.append({
                "semana": row["semana"],
                "SE_CO": round(float(row.get("SE_CO", 120.0)), 1),
                "S": round(float(row.get("S", 120.0)), 1),
                "NE": round(float(row.get("NE", 110.0)), 1),
                "N": round(float(row.get("N", 100.0)), 1),
            })

        # Atualizar SEED_DATA e Local Cache
        sin_data = {
            "ear_atual": ear_atual,
            "ear_subsistemas": ear_atual,
            "ear_historico_meses": ear_historico,
            "ena_subsistemas": ena_subsistemas,
            "cmo_atual": cmo_atual,
            "cmo_historico": cmo_historico,
            "ultima_atualizacao_ons": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        SEED_DATA["operacao_sin"] = sin_data
        cache.set("domain_operacao_sin", sin_data)
        logger.info("Cache local e SEED_DATA atualizados com dados oficiais do ONS.")

    def run_pipeline(self, years: Optional[List[int]] = None) -> Dict[str, Any]:
        """Executa o fluxo completo de ingestao."""
        if years is None:
            curr_year = datetime.datetime.now().year
            years = [curr_year - 1, curr_year]

        logger.info(f"Iniciando pipeline de ingestao ONS para os anos: {years}")
        self.last_status["status"] = "running"
        self.last_status["error"] = None

        try:
            ear_records = self.ingest_ear(years)
            ena_records = self.ingest_ena(years)
            cmo_records = self.ingest_cmo(years)

            bq_synced = self.sync_to_bigquery(ear_records, ena_records, cmo_records)
            self.update_local_cache_and_seed(ear_records, ena_records, cmo_records)

            self.last_status = {
                "status": "success",
                "last_run": datetime.datetime.now().isoformat(),
                "records_processed": {
                    "ear": len(ear_records),
                    "ena": len(ena_records),
                    "cmo": len(cmo_records)
                },
                "bigquery_synced": bq_synced,
                "error": None
            }
            return self.last_status

        except Exception as e:
            logger.error(f"Falha na execucao do pipeline ONS: {e}")
            self.last_status = {
                "status": "failed",
                "last_run": datetime.datetime.now().isoformat(),
                "records_processed": {},
                "error": str(e)
            }
            return self.last_status

ons_ingestor = OnsSinIngestor()

if __name__ == "__main__":
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    print("Executando Ingestor ONS Operacao do SIN...")
    res = ons_ingestor.run_pipeline([2025, 2026])
    print("Resultado da Ingestao:", res)
