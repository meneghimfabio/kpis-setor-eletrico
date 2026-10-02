import os
import logging
from google.cloud import bigquery
from pipelines.ingestion.gcp_client import PROJECT_ID, get_bigquery_client

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("dataform_runner")

SQL_DEC_FEC = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.gold_kpis.kpi_dec_fec_conformidade` AS
WITH latest_records AS (
  SELECT
    data_referencia,
    distribuidora,
    nome_concessionaria,
    sigla_uf,
    dec_apurado_horas,
    dec_limite_aneel_horas,
    conformidade_dec,
    fec_apurado_vezes,
    fec_limite_aneel_vezes,
    conformidade_fec,
    ROW_NUMBER() OVER (
      PARTITION BY distribuidora 
      ORDER BY data_referencia DESC
    ) as rn
  FROM
    `{PROJECT_ID}.aneel_silver.dec_fec_distribuidoras`
)
SELECT
  data_referencia,
  distribuidora,
  nome_concessionaria,
  sigla_uf,
  dec_apurado_horas,
  dec_limite_aneel_horas,
  ROUND((dec_apurado_horas - dec_limite_aneel_horas), 2) AS desvio_dec_horas,
  ROUND(((dec_apurado_horas / NULLIF(dec_limite_aneel_horas, 0)) - 1.0) * 100, 1) AS percentual_ultrapassagem_dec,
  conformidade_dec,
  fec_apurado_vezes,
  fec_limite_aneel_vezes,
  ROUND((fec_apurado_vezes - fec_limite_aneel_vezes), 2) AS desvio_fec_vezes,
  ROUND(((fec_apurado_vezes / NULLIF(fec_limite_aneel_vezes, 0)) - 1.0) * 100, 1) AS percentual_ultrapassagem_fec,
  conformidade_fec,
  CASE
    WHEN conformidade_dec AND conformidade_fec THEN "Conforme"
    WHEN NOT conformidade_dec AND NOT conformidade_fec THEN "Crítico (DEC e FEC)"
    WHEN NOT conformidade_dec THEN "Atenção (DEC Ultrapassado)"
    ELSE "Atenção (FEC Ultrapassado)"
  END AS status_regulatorio,
  ROUND(
    CASE 
      WHEN dec_apurado_horas > dec_limite_aneel_horas 
      THEN (dec_apurado_horas - dec_limite_aneel_horas) * 4.5 
      ELSE 0.0 
    END, 2
  ) AS compensacao_estimada_rs_mm,
  RANK() OVER (ORDER BY dec_apurado_horas ASC) AS ranking_qualidade_dec
FROM
  latest_records
WHERE
  rn = 1
ORDER BY
  dec_apurado_horas ASC;
"""

SQL_MMGD = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.gold_kpis.kpi_mmgd_expansao_uf` AS
WITH base_agg AS (
  SELECT
    sigla_uf,
    COALESCE(subsistema, "SE_CO") AS subsistema,
    MAX(data_referencia) AS ultima_data_referencia,
    SUM(qtd_conexoes) AS total_conexoes,
    ROUND(SUM(potencia_instalada_kw) / 1000.0, 2) AS potencia_instalada_mw,
    ROUND((SUM(potencia_instalada_kw) / 1000.0) * 720 * 0.19 / 1000.0, 2) AS energia_autogerada_gwh_mes
  FROM
    `{PROJECT_ID}.aneel_silver.mmgd_instalacoes`
  GROUP BY
    sigla_uf, subsistema
),
totals AS (
  SELECT
    SUM(potencia_instalada_mw) AS total_mw_brasil,
    SUM(total_conexoes) AS total_conexoes_brasil
  FROM
    base_agg
)
SELECT
  b.sigla_uf,
  b.subsistema,
  b.ultima_data_referencia,
  b.total_conexoes,
  b.potencia_instalada_mw,
  b.energia_autogerada_gwh_mes,
  ROUND((b.potencia_instalada_mw / NULLIF(t.total_mw_brasil, 0)) * 100, 2) AS market_share_nacional_pct,
  RANK() OVER (ORDER BY b.potencia_instalada_mw DESC) AS ranking_nacional_potencia
FROM
  base_agg b
CROSS JOIN
  totals t
ORDER BY
  b.potencia_instalada_mw DESC;
"""

SQL_TARIFAS = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.gold_kpis.kpi_tarifas_ranking` AS
SELECT
  distribuidora,
  concessionaria,
  uf,
  resolucao_homologatoria,
  data_vigencia,
  tarifa_b1_rs_kwh,
  tusd_rs_mwh,
  te_rs_mwh,
  ROUND((tusd_rs_mwh / NULLIF(tusd_rs_mwh + te_rs_mwh, 0)) * 100, 1) AS share_tusd_fio_pct,
  ROUND((te_rs_mwh / NULLIF(tusd_rs_mwh + te_rs_mwh, 0)) * 100, 1) AS share_te_energia_pct,
  tarifa_b2_rural_rs_kwh,
  tarifa_b3_comercial_rs_kwh,
  a4_verde_demanda_rs_kw,
  a4_verde_energia_fora_ponta_rs_mwh,
  a4_verde_energia_ponta_rs_mwh,
  wacc_regulatorio_pct,
  fator_x_pct,
  RANK() OVER (ORDER BY tarifa_b1_rs_kwh ASC) AS ranking_tarifa_mais_barata,
  RANK() OVER (ORDER BY tarifa_b3_comercial_rs_kwh ASC) AS ranking_tarifa_comercial,
  RANK() OVER (ORDER BY a4_verde_demanda_rs_kw ASC) AS ranking_demanda_industrial_a4
FROM
  `{PROJECT_ID}.aneel_silver.tarifas_homologadas`
ORDER BY
  tarifa_b1_rs_kwh ASC;
"""

SQL_OUVIDORIA = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.gold_kpis.kpi_ouvidoria_satisfacao` AS
SELECT
  distribuidora,
  data_referencia,
  score_iasc,
  ranking_iasc,
  total_reclamacoes,
  procedencia_pct,
  tempo_medio_resolucao_dias,
  cumprimento_sla_pct,
  CASE
    WHEN score_iasc >= 72.0 THEN "Alta Satisfação (Excelente)"
    WHEN score_iasc >= 65.0 THEN "Satisfação Moderada"
    ELSE "Baixa Satisfação (Alerta Regulatório)"
  END AS classificacao_satisfacao
FROM
  `{PROJECT_ID}.aneel_silver.ouvidoria_reclamacoes`
ORDER BY
  ranking_iasc ASC;
"""

SQL_CCEE = f"""
CREATE OR REPLACE TABLE `{PROJECT_ID}.gold_kpis.kpi_ccee_mercado_resumo` AS
WITH latest_pld AS (
  SELECT
    data_hora,
    subsistema,
    pld_rs_mwh,
    pld_teto_rs_mwh,
    pld_piso_rs_mwh,
    patamar,
    ROW_NUMBER() OVER (PARTITION BY subsistema ORDER BY data_hora DESC) as rn
  FROM
    `{PROJECT_ID}.mercado_ccee.pld_horario`
),
pld_filtrado AS (
  SELECT
    subsistema,
    pld_rs_mwh,
    pld_teto_rs_mwh,
    pld_piso_rs_mwh,
    patamar,
    data_hora as data_apuracao
  FROM
    latest_pld
  WHERE
    rn = 1
),
pld_stats AS (
  SELECT
    ROUND(AVG(pld_rs_mwh), 2) as pld_medio_nacional_rs_mwh,
    ROUND(MAX(pld_rs_mwh) - MIN(pld_rs_mwh), 2) as spread_maximo_regional_rs_mwh,
    CASE 
      WHEN (MAX(pld_rs_mwh) - MIN(pld_rs_mwh)) > 15.0 THEN "Alerta: Descolamento Estrutural entre Submercados"
      ELSE "Equilíbrio Inter-regional"
    END as status_integracao_sin
  FROM
    pld_filtrado
)
SELECT
  p.subsistema,
  p.pld_rs_mwh,
  p.pld_teto_rs_mwh,
  p.pld_piso_rs_mwh,
  p.patamar,
  p.data_apuracao,
  s.pld_medio_nacional_rs_mwh,
  s.spread_maximo_regional_rs_mwh,
  s.status_integracao_sin,
  ROUND((p.pld_rs_mwh - s.pld_medio_nacional_rs_mwh), 2) as diferenca_vs_media_nacional
FROM
  pld_filtrado p
CROSS JOIN
  pld_stats s
ORDER BY
  p.pld_rs_mwh DESC;
"""

def run_gold_transformations():
    client = get_bigquery_client()
    logger.info("=== Executando Transformações Silver -> Gold (Dataform / BigQuery) ===")
    
    queries = [
        ("kpi_dec_fec_conformidade", SQL_DEC_FEC),
        ("kpi_mmgd_expansao_uf", SQL_MMGD),
        ("kpi_tarifas_ranking", SQL_TARIFAS),
        ("kpi_ouvidoria_satisfacao", SQL_OUVIDORIA),
        ("kpi_ccee_mercado_resumo", SQL_CCEE)
    ]
    
    for name, sql in queries:
        logger.info(f"Materializando tabela Gold: {PROJECT_ID}.gold_kpis.{name}...")
        try:
            job = client.query(sql)
            job.result()
            logger.info(f"Tabela Gold {name} criada e atualizada com sucesso.")
        except Exception as e:
            logger.warning(f"Aviso ao materializar {name} no BigQuery: {e}")
        
    logger.info("=== Transformações Gold processadas! ===")

if __name__ == "__main__":
    run_gold_transformations()
