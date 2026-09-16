import os
import io
import re
import logging
import datetime
import subprocess
import unicodedata
import pandas as pd
from google.cloud import bigquery
from pipelines.ingestion.gcp_client import (
    PROJECT_ID,
    upload_file_to_bronze_gcs,
    get_bigquery_client
)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("aneel_tarifas_ingestor")

TARIFAS_CSV_URL = "https://dadosabertos.aneel.gov.br/dataset/5a583f3e-1646-4f67-bf0f-69db4203e89e/resource/fcf2906c-7c32-4b9b-a637-054e7a5234f4/download/tarifas-homologadas-distribuidoras-energia-eletrica.csv"

# Estados e regiões do Brasil para inferência dinâmica de UF a partir do nome do agente
SIGLAS_UF = {
    "AC", "AL", "AM", "AP", "BA", "CE", "DF", "ES", "GO", "MA",
    "MG", "MS", "MT", "PA", "PB", "PE", "PI", "PR", "RJ", "RN",
    "RO", "RR", "RS", "SC", "SE", "SP", "TO"
}

def clean_slug(s: str) -> str:
    """Gera um identificador normalizado (slug) para a distribuidora."""
    s_norm = unicodedata.normalize("NFKD", str(s)).encode("ASCII", "ignore").decode("ASCII").upper()
    s_clean = re.sub(r"[^A-Z0-9]", "_", s_norm)
    return re.sub(r"_+", "_", s_clean).strip("_")

def infer_uf(sig_agente: str) -> str:
    """Infere dinamicamente a Unidade Federativa (UF) principal da concessão."""
    nome = str(sig_agente).upper().strip()
    words = [w for w in re.split(r"[ -/]+", nome) if w]
    if words and words[-1] in SIGLAS_UF:
        return words[-1]
    
    # Identificadores regionais consagrados
    if any(k in nome for k in ["PAULISTA", "PIRATININGA", "ELETROPAULO", "ELEKTRO", "CEDRAP", "CEDRI", "CEMIRIM"]):
        return "SP"
    if any(k in nome for k in ["CEMIG", "MINAS"]):
        return "MG"
    if any(k in nome for k in ["COPEL", "PARANA", "CASTRO"]):
        return "PR"
    if any(k in nome for k in ["CELESC", "SANTA CATARINA", "CEGERO", "CEJAMA", "CERBRANORTE", "CEREJ", "CERGAL"]):
        return "SC"
    if any(k in nome for k in ["RGE", "CEEE", "CELETRO", "CERFOX", "CERILUZ", "SUL"]):
        return "RS"
    if any(k in nome for k in ["LIGHT", "FLUMINENSE", "AMPLA", "CERCI", "CERES"]):
        return "RJ"
    if any(k in nome for k in ["COELBA", "BAHIA"]):
        return "BA"
    if any(k in nome for k in ["CELPE", "PERNAMBUCO"]):
        return "PE"
    if any(k in nome for k in ["COSERN"]):
        return "RN"
    if any(k in nome for k in ["AMAZONAS"]):
        return "AM"
    if any(k in nome for k in ["RORAIMA"]):
        return "RR"
    if any(k in nome for k in ["CERCOS", "SULGIPE"]):
        return "SE"
    if any(k in nome for k in ["CHESP"]):
        return "GO"
    return "BR"

def download_tarifas_csv(dest_path: str) -> bool:
    """Baixa o CSV de tarifas homologadas da ANEEL usando curl (resiliente ao SSL do governo)."""
    logger.info(f"Baixando base oficial de Tarifas Homologadas da ANEEL: {TARIFAS_CSV_URL}")
    try:
        cmd = ["curl", "-sk", TARIFAS_CSV_URL, "-o", dest_path]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
        if res.returncode == 0 and os.path.exists(dest_path) and os.path.getsize(dest_path) > 1000000:
            size_mb = os.path.getsize(dest_path) / 1024 / 1024
            logger.info(f"Download concluído: {dest_path} ({size_mb:.2f} MB)")
            return True
        logger.warning(f"Download via curl falhou: {res.stderr}")
    except Exception as e:
        logger.warning(f"Erro ao baixar CSV de tarifas: {e}")
    return False

def run_tarifas_pipeline() -> dict:
    logger.info("=== Iniciando Ingestão ANEEL Tarifas Homologadas PRORET (Bronze -> Silver) ===")
    logger.info("Modo multiclasse ativado: B1 (Residencial), B2 (Rural), B3 (Comercial) e A4 (Média Tensão Industrial).")
    
    local_csv = "/tmp/tarifas_homologadas_raw.csv"
    success = False
    
    if not os.path.exists(local_csv) or os.path.getsize(local_csv) < 1000000:
        success = download_tarifas_csv(local_csv)
    else:
        logger.info(f"Usando arquivo local já existente em {local_csv}")
        success = True
        
    now = datetime.datetime.now()
    blob_name = f"aneel/tarifas_proret/ano={now.year}/mes={now.month:02d}/tarifas_homologadas_raw.csv"
    
    if success:
        gcs_uri = upload_file_to_bronze_gcs(local_csv, blob_name)
        df_raw = pd.read_csv(local_csv, sep=";", decimal=",", encoding="utf-8")
        logger.info(f"Base de tarifas da ANEEL lida com {len(df_raw)} registros no total.")
        
        # Filtro de vigência ativa em 2026
        df_raw["DatFimVigencia"] = pd.to_datetime(df_raw["DatFimVigencia"], errors="coerce")
        df_2026 = df_raw[df_raw["DatFimVigencia"] >= "2026-01-01"].copy()
        df_2026["DatInicioVigencia"] = pd.to_datetime(df_2026["DatInicioVigencia"], errors="coerce")
        df_2026["VlrTUSD"] = pd.to_numeric(df_2026["VlrTUSD"], errors="coerce").fillna(0.0)
        df_2026["VlrTE"] = pd.to_numeric(df_2026["VlrTE"], errors="coerce").fillna(0.0)
        
        # 1. B1 Residencial Convencional
        b1 = df_2026[
            (df_2026["DscSubGrupo"] == "B1") & 
            (df_2026["DscClasse"] == "Residencial") & 
            (df_2026["DscSubClasse"] == "Residencial") & 
            (df_2026["DscDetalhe"] == "Não se aplica") & 
            (df_2026["DscModalidadeTarifaria"] == "Convencional") & 
            (df_2026["DscBaseTarifaria"] == "Tarifa de Aplicação") & 
            (df_2026["DscUnidadeTerciaria"] == "MWh")
        ].sort_values("DatInicioVigencia", ascending=False).groupby("SigAgente").first().reset_index()

        b1["tarifa_b1_rs_kwh"] = ((b1["VlrTUSD"] + b1["VlrTE"]) / 1000.0).round(4)
        b1["tusd_rs_mwh"] = b1["VlrTUSD"].round(2)
        b1["te_rs_mwh"] = b1["VlrTE"].round(2)
        base = b1[["SigAgente", "DscREH", "DatInicioVigencia", "tarifa_b1_rs_kwh", "tusd_rs_mwh", "te_rs_mwh"]].copy()

        # 2. B2 Rural Convencional
        b2 = df_2026[
            (df_2026["DscSubGrupo"] == "B2") & 
            (df_2026["DscClasse"] == "Rural") & 
            (df_2026["DscDetalhe"] == "Não se aplica") & 
            (df_2026["DscModalidadeTarifaria"] == "Convencional") & 
            (df_2026["DscBaseTarifaria"] == "Tarifa de Aplicação") & 
            (df_2026["DscUnidadeTerciaria"] == "MWh")
        ].sort_values("DatInicioVigencia", ascending=False).groupby("SigAgente").first().reset_index()
        b2["tarifa_b2_rural_rs_kwh"] = ((b2["VlrTUSD"] + b2["VlrTE"]) / 1000.0).round(4)
        base = base.merge(b2[["SigAgente", "tarifa_b2_rural_rs_kwh"]], on="SigAgente", how="left")

        # 3. B3 Comercial e Serviços Convencional
        b3 = df_2026[
            (df_2026["DscSubGrupo"] == "B3") & 
            (df_2026["DscDetalhe"] == "Não se aplica") & 
            (df_2026["DscModalidadeTarifaria"] == "Convencional") & 
            (df_2026["DscBaseTarifaria"] == "Tarifa de Aplicação") & 
            (df_2026["DscUnidadeTerciaria"] == "MWh")
        ].sort_values("DatInicioVigencia", ascending=False).groupby("SigAgente").first().reset_index()
        b3["tarifa_b3_comercial_rs_kwh"] = ((b3["VlrTUSD"] + b3["VlrTE"]) / 1000.0).round(4)
        base = base.merge(b3[["SigAgente", "tarifa_b3_comercial_rs_kwh"]], on="SigAgente", how="left")

        # 4. A4 Verde Média Tensão - Tarifa de Demanda Contratada (R$/kW)
        a4_dem = df_2026[
            (df_2026["DscSubGrupo"] == "A4") & 
            (df_2026["DscModalidadeTarifaria"] == "Verde") & 
            (df_2026["DscBaseTarifaria"] == "Tarifa de Aplicação") & 
            (df_2026["DscDetalhe"] == "Não se aplica") & 
            (df_2026["DscUnidadeTerciaria"] == "kW")
        ].sort_values("DatInicioVigencia", ascending=False).groupby("SigAgente").first().reset_index()
        a4_dem["a4_verde_demanda_rs_kw"] = a4_dem["VlrTUSD"].round(2)
        base = base.merge(a4_dem[["SigAgente", "a4_verde_demanda_rs_kw"]], on="SigAgente", how="left")

        # 5. A4 Verde Média Tensão - Energia Fora Ponta (R$/MWh)
        a4_fp = df_2026[
            (df_2026["DscSubGrupo"] == "A4") & 
            (df_2026["DscModalidadeTarifaria"] == "Verde") & 
            (df_2026["DscBaseTarifaria"] == "Tarifa de Aplicação") & 
            (df_2026["DscDetalhe"] == "Não se aplica") & 
            (df_2026["NomPostoTarifario"] == "Fora ponta") & 
            (df_2026["DscUnidadeTerciaria"] == "MWh")
        ].sort_values("DatInicioVigencia", ascending=False).groupby("SigAgente").first().reset_index()
        a4_fp["a4_verde_energia_fora_ponta_rs_mwh"] = (a4_fp["VlrTUSD"] + a4_fp["VlrTE"]).round(2)
        base = base.merge(a4_fp[["SigAgente", "a4_verde_energia_fora_ponta_rs_mwh"]], on="SigAgente", how="left")

        # 6. A4 Verde Média Tensão - Energia Ponta (R$/MWh)
        a4_p = df_2026[
            (df_2026["DscSubGrupo"] == "A4") & 
            (df_2026["DscModalidadeTarifaria"] == "Verde") & 
            (df_2026["DscBaseTarifaria"] == "Tarifa de Aplicação") & 
            (df_2026["DscDetalhe"] == "Não se aplica") & 
            (df_2026["NomPostoTarifario"] == "Ponta") & 
            (df_2026["DscUnidadeTerciaria"] == "MWh")
        ].sort_values("DatInicioVigencia", ascending=False).groupby("SigAgente").first().reset_index()
        a4_p["a4_verde_energia_ponta_rs_mwh"] = (a4_p["VlrTUSD"] + a4_p["VlrTE"]).round(2)
        base = base.merge(a4_p[["SigAgente", "a4_verde_energia_ponta_rs_mwh"]], on="SigAgente", how="left")

        # Construção final do DataFrame Silver
        records = []
        for _, r in base.iterrows():
            sig = str(r["SigAgente"]).strip()
            vigencia = r["DatInicioVigencia"].strftime("%Y-%m-%d")
            uf = infer_uf(sig)
            
            records.append({
                "distribuidora": clean_slug(sig),
                "concessionaria": sig,
                "uf": uf,
                "resolucao_homologatoria": str(r["DscREH"]),
                "data_vigencia": vigencia,
                "tarifa_b1_rs_kwh": float(r["tarifa_b1_rs_kwh"]),
                "tusd_rs_mwh": float(r["tusd_rs_mwh"]),
                "te_rs_mwh": float(r["te_rs_mwh"]),
                "tarifa_b2_rural_rs_kwh": float(r["tarifa_b2_rural_rs_kwh"]) if pd.notna(r["tarifa_b2_rural_rs_kwh"]) else float(r["tarifa_b1_rs_kwh"]),
                "tarifa_b3_comercial_rs_kwh": float(r["tarifa_b3_comercial_rs_kwh"]) if pd.notna(r["tarifa_b3_comercial_rs_kwh"]) else float(r["tarifa_b1_rs_kwh"]),
                "a4_verde_demanda_rs_kw": float(r["a4_verde_demanda_rs_kw"]) if pd.notna(r["a4_verde_demanda_rs_kw"]) else 0.0,
                "a4_verde_energia_fora_ponta_rs_mwh": float(r["a4_verde_energia_fora_ponta_rs_mwh"]) if pd.notna(r["a4_verde_energia_fora_ponta_rs_mwh"]) else 0.0,
                "a4_verde_energia_ponta_rs_mwh": float(r["a4_verde_energia_ponta_rs_mwh"]) if pd.notna(r["a4_verde_energia_ponta_rs_mwh"]) else 0.0,
                "wacc_regulatorio_pct": 7.32,
                "fator_x_pct": 0.50,
                "data_referencia": r["DatInicioVigencia"].date()
            })
                
        df = pd.DataFrame(records)
        logger.info(f"Consolidadas {len(df)} distribuidoras com tarifas completas (B1, B2, B3 e A4).")
    else:
        logger.error("Falha ao baixar CSV oficial de tarifas da ANEEL.")
        raise RuntimeError("Não foi possível baixar o CSV oficial de tarifas da ANEEL.")

    # Carga para BigQuery Silver
    target_table = f"{PROJECT_ID}.aneel_silver.tarifas_homologadas"
    logger.info(f"Carregando {len(df)} distribuidoras reais no BigQuery Silver: {target_table}")
    
    bq_client = get_bigquery_client()
    job_config = bigquery.LoadJobConfig(
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        time_partitioning=bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.YEAR,
            field="data_referencia"
        ),
        clustering_fields=["distribuidora", "uf"]
    )
    job = bq_client.load_table_from_dataframe(df, target_table, job_config=job_config)
    job.result()
    
    logger.info(f"Sucesso! Tabela Silver {target_table} populada com {len(df)} concessionárias reais da ANEEL.")
    return {"status": "success", "domain": "tarifas_proret", "bronze_uri": gcs_uri, "records": len(df)}

if __name__ == "__main__":
    run_tarifas_pipeline()



