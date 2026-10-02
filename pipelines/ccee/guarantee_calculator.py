"""
Módulo determinístico de cálculo de garantias financeiras CCEE.
Isolado de LLMs para garantir acurácia matemática absoluta e conformidade regulatória.
"""
from dataclasses import dataclass
from decimal import Decimal, ROUND_HALF_UP
from typing import List, Dict, Any

@dataclass(frozen=True)
class HourlyPosition:
    hour: int
    consumption_mwh: Decimal
    generation_mwh: Decimal
    bilateral_contracts_mwh: Decimal
    pld_brl_mwh: Decimal

@dataclass
class GuaranteeAssessment:
    agent_ccee_code: str
    assessment_date: str
    net_exposure_mwh: Decimal
    total_exposure_brl: Decimal
    prudential_margin_brl: Decimal
    existing_guarantees_brl: Decimal
    required_additional_guarantee_brl: Decimal
    recommendation: str

class CCEEGuaranteeEngine:
    def __init__(self, prudential_margin_rate: Decimal = Decimal("0.05")):
        self.margin_rate = prudential_margin_rate

    def calculate_daily_requirement(
        self,
        ccee_code: str,
        assessment_date: str,
        hourly_data: List[HourlyPosition],
        existing_guarantees: Decimal
    ) -> GuaranteeAssessment:
        total_exposure = Decimal("0.00")
        total_net_mwh = Decimal("0.00")

        for pos in hourly_data:
            # Posição Líquida: Consumo - Geração - Contratos Bilaterais
            net_hourly_mwh = pos.consumption_mwh - pos.generation_mwh - pos.bilateral_contracts_mwh
            total_net_mwh += net_hourly_mwh
            
            # Custo monetário no PLD da hora e submercado
            hourly_cost = net_hourly_mwh * pos.pld_brl_mwh
            total_exposure += hourly_cost

        # Se for credor líquido (total_exposure <= 0), nenhuma garantia adicional é exigida
        if total_exposure <= Decimal("0.00"):
            required_additional = Decimal("0.00")
            margin = Decimal("0.00")
            rec = "CREDOR_LIQUIDO - Nenhuma garantia adicional requerida."
        else:
            margin = (total_exposure * self.margin_rate).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
            gross_required = total_exposure + margin
            required_additional = max(Decimal("0.00"), gross_required - existing_guarantees)
            
            if required_additional > Decimal("0.00"):
                rec = f"APORTE_OBRIGATORIO - Provisionar R$ {required_additional:,.2f} antes das 09:30 BRT."
            else:
                rec = "GARANTIA_SUFICIENTE - Garantias atuais cobrem a exposição estimada."

        return GuaranteeAssessment(
            agent_ccee_code=ccee_code,
            assessment_date=assessment_date,
            net_exposure_mwh=total_net_mwh.quantize(Decimal("0.001")),
            total_exposure_brl=total_exposure.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP),
            prudential_margin_brl=margin,
            existing_guarantees_brl=existing_guarantees,
            required_additional_guarantee_brl=required_additional,
            recommendation=rec
        )
