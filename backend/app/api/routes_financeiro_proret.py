from fastapi import APIRouter
from app.core.bigquery_client import bq_manager
from app.core.simulator import ProretSimulationInput, ProretSimulationResult, simulate_proret_tariff

router = APIRouter(prefix="/financeiro-proret", tags=["Financeiro & PRORET"])

@router.get("/overview")
def get_financeiro_overview():
    data = bq_manager.get_domain_data("financeiro_proret")
    return {
        "indicadores_setoriais": data.get("indicadores_setoriais", {}),
        "empresas_dre": data.get("empresas_dre", []),
        "parametros_proret_padrao": data.get("parametros_proret_padrao", {}),
        "qualidade_dados_ativos": data.get("qualidade_dados_ativos", []),
        "ranking_tarifario_aneel": data.get("ranking_tarifario_aneel", []),
        "ultima_atualizacao_aneel": data.get("ultima_atualizacao_aneel", "Dados Oficiais ANEEL PRORET / Tarifas Homologadas"),
        "_metadata": data.get("_metadata")
    }

@router.post("/simulate", response_model=ProretSimulationResult)
def run_proret_simulation(params: ProretSimulationInput):
    return simulate_proret_tariff(params)
