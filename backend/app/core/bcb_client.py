import logging
import datetime
from typing import Dict, Any, Optional
import requests
from app.data.local_cache import cache

logger = logging.getLogger("bcb_sgs_client")

# Códigos de séries temporais do Banco Central do Brasil (SGS)
BCB_SERIES = {
    "selic_meta": 432,      # Taxa de juros - Meta Selic definida pelo Copom (% a.a.)
    "selic_diaria": 11,     # Taxa de juros - Selic acumulada no dia (% a.a.)
    "ipca_mensal": 433,     # Índice nacional de preços ao consumidor-amplo (IPCA) - variação mensal (%)
    "ipca_12m": 13522,      # IPCA - Variação acumulada nos últimos 12 meses (%)
}

# Valores de contingência (fallback) calibrados com o cenário macroeconômico vigente
FALLBACK_MACRO = {
    "selic_meta_anual_pct": 13.75,
    "selic_data_referencia": "01/10/2026",
    "ipca_acumulado_12m_pct": 4.22,
    "ipca_mensal_pct": 0.38,
    "ipca_data_referencia": "01/09/2026",
    "fonte": "Banco Central do Brasil (BCB SGS - Fallback Local)",
    "status": "fallback"
}


class BCBSGSClient:
    """
    Cliente para consulta à API pública de dados abertos do Banco Central do Brasil (SGS).
    Fornece séries macroeconômicas oficiais (Selic e IPCA) para o simulador tarifário PRORET
    e a visão executiva macroeconômica.
    """

    BASE_URL = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{series_code}/dados/ultimos/{n}?formato=json"

    def __init__(self, timeout_seconds: int = 5):
        self.timeout = timeout_seconds
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "PainelSetorEletrico/1.0 (+https://github.com/)",
            "Accept": "application/json"
        })

    def fetch_series_latest(self, series_code: int, count: int = 1) -> Optional[list]:
        """Consulta os últimos N valores de uma série temporal no BCB SGS."""
        cache_key = f"bcb_sgs_series_{series_code}_{count}"
        cached = cache.get(cache_key)
        if cached is not None:
            return cached

        url = self.BASE_URL.format(series_code=series_code, n=count)
        try:
            resp = self.session.get(url, timeout=self.timeout)
            if resp.status_code == 200:
                data = resp.json()
                cache.set(cache_key, data, ttl=3600)
                return data
            else:
                logger.warning(f"BCB SGS HTTP {resp.status_code} para série {series_code}: {resp.text[:100]}")
                return None
        except Exception as e:
            logger.warning(f"Falha ao consultar BCB SGS série {series_code}: {e}")
            return None

    def get_macro_indicators(self, use_cache: bool = True) -> Dict[str, Any]:
        """
        Retorna os indicadores macroeconômicos consolidados (Selic Meta e IPCA 12M).
        Garante graceful fallback se a API do BCB estiver fora do ar.
        """
        cache_key = "bcb_macro_indicators_consolidated"
        if use_cache:
            cached_macro = cache.get(cache_key)
            if cached_macro is not None:
                return cached_macro

        selic_data = self.fetch_series_latest(BCB_SERIES["selic_meta"], count=1)
        ipca_12m_data = self.fetch_series_latest(BCB_SERIES["ipca_12m"], count=1)
        ipca_mensal_data = self.fetch_series_latest(BCB_SERIES["ipca_mensal"], count=1)

        result = dict(FALLBACK_MACRO)
        result["data_consulta"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        is_live = False

        if selic_data and len(selic_data) > 0:
            try:
                result["selic_meta_anual_pct"] = float(selic_data[-1]["valor"])
                result["selic_data_referencia"] = selic_data[-1]["data"]
                is_live = True
            except (ValueError, KeyError) as e:
                logger.warning(f"Erro ao processar valor Selic BCB: {e}")

        if ipca_12m_data and len(ipca_12m_data) > 0:
            try:
                result["ipca_acumulado_12m_pct"] = float(ipca_12m_data[-1]["valor"])
                result["ipca_data_referencia"] = ipca_12m_data[-1]["data"]
                is_live = True
            except (ValueError, KeyError) as e:
                logger.warning(f"Erro ao processar valor IPCA 12M BCB: {e}")

        if ipca_mensal_data and len(ipca_mensal_data) > 0:
            try:
                result["ipca_mensal_pct"] = float(ipca_mensal_data[-1]["valor"])
            except (ValueError, KeyError):
                pass

        if is_live:
            result["fonte"] = "Banco Central do Brasil - Sistema Gerenciador de Séries Temporais (SGS)"
            result["status"] = "online"

        # WACC Regulatório Real padrão ANEEL: 7.32%
        wacc_real = 7.32 / 100.0
        ipca_decimal = result["ipca_acumulado_12m_pct"] / 100.0
        # Equação de Fisher: (1 + i_nominal) = (1 + r_real) * (1 + inflacao)
        wacc_nominal = ((1.0 + wacc_real) * (1.0 + ipca_decimal) - 1.0) * 100.0
        result["wacc_nominal_estimado_pct"] = round(wacc_nominal, 2)

        cache.set(cache_key, result, ttl=3600)
        return result


bcb_client = BCBSGSClient()
