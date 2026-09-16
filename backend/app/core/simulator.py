from pydantic import BaseModel, Field
from typing import Dict, Any

class ProretSimulationInput(BaseModel):
    distribuidora: str = "CPFL Paulista"
    brr_liquida_rs_mm: float = Field(default=14200.0, description="Base de Remuneração Regulatória Líquida em R$ Milhões")
    wacc_regulatorio_pct: float = Field(default=7.32, description="Custo Médio Ponderado de Capital (WACC real após impostos) em %")
    opex_eficiente_rs_mm: float = Field(default=2150.0, description="Custos Operacionais Eficientes (PMSO + Quotas) em R$ Milhões")
    fator_x_pct: float = Field(default=0.85, description="Ganhos de produtividade e eficiência da distribuidora em %")
    componente_q_pct: float = Field(default=-0.15, description="Fator de incentivo à qualidade DEC/FEC (negativo = bônus, positivo = penalidade) em %")
    mercado_faturado_gwh: float = Field(default=28500.0, description="Mercado de energia faturado em GWh")
    custos_parcela_a_rs_mm: float = Field(default=5800.0, description="Custos não-gerenciáveis de energia comprada e encargos setoriais em R$ Milhões")

class ProretSimulationResult(BaseModel):
    remuneracao_capital_rs_mm: float
    opex_eficiente_rs_mm: float
    deducao_fator_x_rs_mm: float
    ajuste_componente_q_rs_mm: float
    parcela_b_rs_mm: float
    parcela_a_rs_mm: float
    receita_requerida_total_rs_mm: float
    tarifa_media_rs_mwh: float
    tarifa_media_rs_kwh: float
    impacto_tarifa_percentual: float
    analise_qualidade_dec_fec: str
    detalhes_calculo: Dict[str, Any]

def simulate_proret_tariff(params: ProretSimulationInput) -> ProretSimulationResult:
    # 1. Remuneração do Capital = BRR * WACC
    wacc_decimal = params.wacc_regulatorio_pct / 100.0
    remuneracao_capital = params.brr_liquida_rs_mm * wacc_decimal
    
    # 2. Custos Operacionais
    opex = params.opex_eficiente_rs_mm
    
    # 3. Dedução de Produtividade (Fator X) e Componente Q
    # No PRORET, o Fator X reduz a Parcela B, e o Componente Q premia ou penaliza com base no cumprimento de DEC/FEC
    fator_x_impacto = (params.fator_x_pct / 100.0) * opex
    componente_q_impacto = (params.componente_q_pct / 100.0) * opex
    
    # 4. Parcela B (Custos Gerenciáveis + Remuneração)
    parcela_b = remuneracao_capital + opex - fator_x_impacto - componente_q_impacto
    
    # 5. Receita Requerida Total = Parcela A + Parcela B
    receita_requerida = params.custos_parcela_a_rs_mm + parcela_b
    
    # 6. Tarifa Resultante
    # Mercado em GWh = MWh * 1000
    mercado_mwh = params.mercado_faturado_gwh * 1000.0
    receita_rs = receita_requerida * 1_000_000.0
    tarifa_mwh = receita_rs / mercado_mwh if mercado_mwh > 0 else 0
    tarifa_kwh = tarifa_mwh / 1000.0
    
    # Base de referência para cálculo de variação (Tarifa base de 315.00 R$/MWh)
    tarifa_base_referencia = 315.00
    impacto_pct = ((tarifa_mwh - tarifa_base_referencia) / tarifa_base_referencia) * 100.0
    
    if params.componente_q_pct < 0:
        analise_q = f"Bônus de Qualidade: A distribuidora superou as metas de DEC/FEC da ANEEL, gerando benefício de R$ {abs(componente_q_impacto):.2f} MM."
    elif params.componente_q_pct > 0:
        analise_q = f"Penalidade de Qualidade: Desvios nos limites de interrupção (DEC/FEC) geraram redutor tarifário de R$ {componente_q_impacto:.2f} MM."
    else:
        analise_q = "Neutro: Indicadores de continuidade aderentes aos limites regulatórios."
        
    return ProretSimulationResult(
        remuneracao_capital_rs_mm=round(remuneracao_capital, 2),
        opex_eficiente_rs_mm=round(opex, 2),
        deducao_fator_x_rs_mm=round(fator_x_impacto, 2),
        ajuste_componente_q_rs_mm=round(componente_q_impacto, 2),
        parcela_b_rs_mm=round(parcela_b, 2),
        parcela_a_rs_mm=round(params.custos_parcela_a_rs_mm, 2),
        receita_requerida_total_rs_mm=round(receita_requerida, 2),
        tarifa_media_rs_mwh=round(tarifa_mwh, 2),
        tarifa_media_rs_kwh=round(tarifa_kwh, 4),
        impacto_tarifa_percentual=round(impacto_pct, 2),
        analise_qualidade_dec_fec=analise_q,
        detalhes_calculo={
            "formula": "Receita Requerida = Parcela A + [ (BRR * WACC) + OPEX - Fator_X - Comp_Q ]",
            "wacc_utilizado_pct": params.wacc_regulatorio_pct,
            "brr_utilizada_rs_mm": params.brr_liquida_rs_mm
        }
    )
