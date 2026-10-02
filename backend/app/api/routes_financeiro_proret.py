from typing import Dict, Any
from fastapi import APIRouter
from app.core.bigquery_client import bq_manager
from app.core.simulator import ProretSimulationInput, ProretSimulationResult, simulate_proret_tariff
from app.core.bcb_client import bcb_client

router = APIRouter(prefix="/financeiro-proret", tags=["Financeiro & PRORET"])

@router.get("/macro")
def get_macro_indicators():
    """Retorna os indicadores macroeconômicos oficiais vigentes (Selic e IPCA) obtidos via API do Banco Central (SGS)."""
    return bcb_client.get_macro_indicators()

@router.get("/overview")
def get_financeiro_overview():
    data = bq_manager.get_domain_data("financeiro_proret")
    macro = bcb_client.get_macro_indicators()

    # Enriquecer indicadores setoriais com o cenário macroeconômico vigente
    indicadores_setoriais = dict(data.get("indicadores_setoriais", {}))
    indicadores_setoriais["selic_vigente_pct"] = macro.get("selic_meta_anual_pct", 13.75)
    indicadores_setoriais["ipca_acumulado_12m_pct"] = macro.get("ipca_acumulado_12m_pct", 4.22)
    indicadores_setoriais["wacc_nominal_estimado_pct"] = macro.get("wacc_nominal_estimado_pct", 11.85)
    indicadores_setoriais["fonte_macro"] = macro.get("fonte", "Banco Central do Brasil (BCB SGS)")

    # Enriquecer parâmetros padrão do PRORET
    parametros_proret = dict(data.get("parametros_proret_padrao", {}))
    parametros_proret["selic_vigente_pct"] = macro.get("selic_meta_anual_pct", 13.75)
    parametros_proret["ipca_vigente_pct"] = macro.get("ipca_acumulado_12m_pct", 4.22)
    parametros_proret["wacc_nominal_pct"] = macro.get("wacc_nominal_estimado_pct", 11.85)

    return {
        "indicadores_setoriais": indicadores_setoriais,
        "macro_indicadores": macro,
        "empresas_dre": data.get("empresas_dre", []),
        "parametros_proret_padrao": parametros_proret,
        "qualidade_dados_ativos": data.get("qualidade_dados_ativos", []),
        "ranking_tarifario_aneel": data.get("ranking_tarifario_aneel", []),
        "ultima_atualizacao_aneel": data.get("ultima_atualizacao_aneel", "Dados Oficiais ANEEL PRORET / Tarifas Homologadas"),
        "_metadata": data.get("_metadata")
    }

@router.post("/simulate", response_model=ProretSimulationResult)
def run_proret_simulation(params: ProretSimulationInput):
    return simulate_proret_tariff(params)
