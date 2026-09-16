import os
import io
import logging
import datetime
import subprocess
import requests
import pandas as pd
from google.cloud import bigquery
from pipelines.ingestion.gcp_client import (
    PROJECT_ID,
    upload_file_to_bronze_gcs,
    get_bigquery_client
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aneel_ouvidoria_ingestor")

MANIFESTACOES_PARQUET_URL = "https://dadosabertos.aneel.gov.br/dataset/364859a2-7cb8-45ea-9c88-b4392516a6ba/resource/d0f619ef-1bbe-40d1-849c-35b47172df8e/download/manifestacoes-1-2-niveis-distribuidora-2026.parquet"
IASC_CSV_URL = "https://dadosabertos.aneel.gov.br/dataset/f216da23-4b7e-4bbe-9833-06905331a827/resource/7abd3a47-1e1a-4a33-933b-48d658a6f912/download/indice-aneel-satisfacao-consumidor.csv"

# Mapeamento para Ouvidoria (Nível 2)
OUVIDORIA_AGENTS_MAP = {
    "CPFL Paulista": "CPFL_PAULISTA",
    "Enel SP": "ENEL_SP",
    "Cemig": "CEMIG_D",
    "Copel": "COPEL_DIS",
    "Celesc": "CELESC",
    "RGE": "RGE_SUL",
    "Light": "LIGHT",
    "Neoenergia Coelba": "NEOENERGIA_COELBA",
    "Equatorial GO": "EQUATORIAL_GO",
    "Equatorial PA": "EQUATORIAL_PA"
}

# Mapeamento para IASC (Pesquisa de Satisfação ANEEL)
IASC_AGENTS_MAP = {
    "CPFL Paulista": "CPFL_PAULISTA",
    "Enel Distribuição São Paulo": "ENEL_SP",
    "Cemig-D": "CEMIG_D",
    "Copel-Dis": "COPEL_DIS",
    "Celesc-Dis": "CELESC",
    "RGE": "RGE_SUL",
    "Light": "LIGHT",
    "Neoenergia Coelba": "NEOENERGIA_COELBA",
    "Equatorial Goiás": "EQUATORIAL_GO",
    "Equatorial Pará": "EQUATORIAL_PA"
}

def download_file(url: str, dest_path: str, min_bytes: int = 100000) -> bool:
    """Baixa arquivos do portal de dados abertos da ANEEL usando curl."""
    logger.info(f"Baixando base de dados oficial da ANEEL: {url}")
    try:
        cmd = ["curl", "-sk", url, "-o", dest_path]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if res.returncode == 0 and os.path.exists(dest_path) and os.path.getsize(dest_path) >= min_bytes:
            size_mb = os.path.getsize(dest_path) / 1024 / 1024
            logger.info(f"Download concluído: {dest_path} ({size_mb:.2f} MB)")
            return True
        logger.warning(f"Download falhou para {url}: {res.stderr}")
    except Exception as e:
        logger.warning(f"Erro no download de {url}: {e}")
    return False

def run_ouvidoria_pipeline() -> dict:
    logger.info("=== Iniciando Ingestão ANEEL Ouvidoria e IASC (Bronze -> Silver) ===")
    
    local_man = "/tmp/manifestacoes_distribuidoras_2026.parquet"
    local_iasc = "/tmp/indice_aneel_satisfacao_consumidor.csv"
    
    if not os.path.exists(local_man) or os.path.getsize(local_man) < 1000000:
        if not download_file(MANIFESTACOES_PARQUET_URL, local_man, 1000000):
            raise RuntimeError("Falha ao baixar arquivo de manifestações da ANEEL.")
            
    if not os.path.exists(local_iasc) or os.path.getsize(local_iasc) < 500000:
        if not download_file(IASC_CSV_URL, local_iasc, 500000):
            raise RuntimeError("Falha ao baixar CSV do IASC da ANEEL.")

    now = datetime.datetime.now()
    blob_man = f"aneel/ouvidoria_iasc/ano={now.year}/mes={now.month:02d}/manifestacoes_distribuidoras_raw.parquet"
    blob_iasc = f"aneel/ouvidoria_iasc/ano={now.year}/mes={now.month:02d}/indice_aneel_satisfacao_consumidor_raw.csv"

    uri_man = upload_file_to_bronze_gcs(local_man, blob_man)
    uri_iasc = upload_file_to_bronze_gcs(local_iasc, blob_iasc)

    # 1. Processamento IASC
    logger.info("Processando base de satisfação IASC da ANEEL...")
    df_iasc_raw = pd.read_csv(local_iasc, sep=";", decimal=",", encoding="utf-8")
    ano_recente = df_iasc_raw["NumAno"].dropna().max()
    df_iasc = df_iasc_raw[df_iasc_raw["NumAno"] == ano_recente].copy()
    
    df_iasc["distribuidora"] = df_iasc["SigAgente"].map(IASC_AGENTS_MAP)
    df_iasc = df_iasc.dropna(subset=["distribuidora"]).copy()
    df_iasc["score_iasc"] = pd.to_numeric(df_iasc["MdaIndicadorSatisfacao"], errors="coerce").round(1)
    df_iasc["ranking_iasc"] = pd.to_numeric(df_iasc["NumOrdemIASC"], errors="coerce").astype(int)
    iasc_kpis = df_iasc[["distribuidora", "score_iasc", "ranking_iasc"]]

    # 2. Processamento Ouvidoria (Manifestações Nível 2)
    logger.info("Processando base de manifestações de Ouvidoria (Nível 2) da ANEEL...")
    df_man_raw = pd.read_parquet(local_man)
    df_ouv = df_man_raw[df_man_raw["NomCanalManifestacao"] == "Nível 2"].copy()
    
    df_ouv["distribuidora"] = df_ouv["SigAgente"].map(OUVIDORIA_AGENTS_MAP)
    df_ouv = df_ouv.dropna(subset=["distribuidora"]).copy()

    df_ouv["qtd"] = pd.to_numeric(df_ouv["QtdManifestacoesRecebidas"].astype(str).str.replace(",", "."), errors="coerce").fillna(0)
    df_ouv["proc"] = pd.to_numeric(df_ouv["QtdManifestacoesProcedentes"].astype(str).str.replace(",", "."), errors="coerce").fillna(0)
    df_ouv["prazo"] = pd.to_numeric(df_ouv["NumPrazoMedioSolucao"].astype(str).str.replace(",", "."), errors="coerce").fillna(0)

    # Normalização de horas para dias quando aplicável (>30 horas)
    df_ouv["prazo_dias"] = df_ouv["prazo"].apply(lambda p: p / 24.0 if p > 30 else p)
    df_ouv["dias_totais"] = df_ouv["prazo_dias"] * df_ouv["qtd"]
    # SLA regulatório da Ouvidoria ANEEL (15 dias corridos / 10 dias úteis)
    df_ouv["dentro_sla"] = (df_ouv["prazo_dias"] <= 15).astype(int) * df_ouv["qtd"]

    ouv_agg = df_ouv.groupby("distribuidora").agg(
        total_reclamacoes=("qtd", "sum"),
        procedentes=("proc", "sum"),
        dias_totais=("dias_totais", "sum"),
        dentro_sla=("dentro_sla", "sum")
    ).reset_index()

    ouv_agg["total_reclamacoes"] = ouv_agg["total_reclamacoes"].astype(int)
    ouv_agg["procedencia_pct"] = ((ouv_agg["procedentes"] / ouv_agg["total_reclamacoes"].replace(0, 1)) * 100).round(1)
    ouv_agg["tempo_medio_resolucao_dias"] = (ouv_agg["dias_totais"] / ouv_agg["total_reclamacoes"].replace(0, 1)).round(1)
    ouv_agg["cumprimento_sla_pct"] = ((ouv_agg["dentro_sla"] / ouv_agg["total_reclamacoes"].replace(0, 1)) * 100).round(1)

    # 3. Consolidação Final
    merged = pd.merge(ouv_agg, iasc_kpis, on="distribuidora", how="inner")
    ref_date = datetime.date(now.year, now.month, 1)
    merged["ano_mes"] = ref_date.strftime("%Y-%m-%d")
    merged["data_referencia"] = ref_date

    cols = [
        "distribuidora",
        "ano_mes",
        "score_iasc",
        "ranking_iasc",
        "total_reclamacoes",
        "procedencia_pct",
        "tempo_medio_resolucao_dias",
        "cumprimento_sla_pct",
        "data_referencia"
    ]
    df_silver = merged[cols].sort_values("ranking_iasc").reset_index(drop=True)

    # 4. Carga para BigQuery Silver
    target_table = f"{PROJECT_ID}.aneel_silver.ouvidoria_reclamacoes"
    logger.info(f"Carregando {len(df_silver)} registros reais no BigQuery Silver: {target_table}")
    
    bq_client = get_bigquery_client()
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        time_partitioning=bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.MONTH,
            field="data_referencia"
        ),
        clustering_fields=["distribuidora"]
    )
    job = bq_client.load_table_from_dataframe(df_silver, target_table, job_config=job_config)
    job.result()
    
    logger.info(f"Sucesso! Tabela Silver {target_table} populada com {len(df_silver)} registros reais da ANEEL.")
    return {
        "status": "success",
        "domain": "ouvidoria_iasc",
        "bronze_uri": f"{uri_man} ; {uri_iasc}",
        "records": len(df_silver)
    }

if __name__ == "__main__":
    run_ouvidoria_pipeline()

