from fastapi import APIRouter
from app.core.bigquery_client import bq_manager
from app.data.seed_data import SUBSYSTEMS, DISTRIBUTORS, TRANSMITTERS

router = APIRouter(prefix="/executive", tags=["Visão Executiva C-Level"])

@router.get("/summary")
def get_executive_summary(subsystem: str = "SIN"):
    sin_data = bq_manager.get_domain_data("operacao_sin")
    ccee_data = bq_manager.get_domain_data("mercado_ccee")
    trans_data = bq_manager.get_domain_data("transmissao")
    dist_data = bq_manager.get_domain_data("distribuicao_qualidade")
    perdas_data = bq_manager.get_domain_data("perdas_mmgd")
    fin_data = bq_manager.get_domain_data("financeiro_proret")
    alerts_data = bq_manager.get_domain_data("alertas_regulatorios")

    # High-level KPIs with regional filtering
    ear_subs = sin_data.get("ear_atual", sin_data.get("ear_subsistemas", []))
    cmo_subs = sin_data.get("cmo_atual", [])
    pld_subs = ccee_data.get("pld_atual", {}).get("subsistemas", [])
    
    if subsystem and subsystem != "SIN":
        sub_ear = next((e for e in ear_subs if e.get("subsistema") == subsystem), None)
        ear_total = sub_ear.get("ear_percentual", 65.8) if sub_ear else 65.8
        ear_status = sub_ear.get("status_criticidade", "Favorável") if sub_ear else "Favorável"
        
        sub_cmo = next((c for c in cmo_subs if c.get("subsistema") == subsystem), None)
        cmo_medio = sub_cmo.get("cmo_rs_mwh", sub_cmo.get("cmo_medio", 68.05)) if sub_cmo else 68.05
        
        sub_pld = next((p for p in pld_subs if p.get("subsistema") == subsystem), None)
        pld_medio = sub_pld.get("pld_rs_mwh", 69.45) if sub_pld else 69.45

        perda_map = {"SE_CO": 13.8, "S": 11.2, "NE": 16.5, "N": 24.8}
        perda_total_pct = perda_map.get(subsystem, 14.95)
    else:
        ear_total = 65.8
        ear_status = "Favorável"
        cmo_medio = 68.05
        pld_medio = 69.45
        perda_total_pct = perdas_data.get("balanco_nacional", {}).get("perda_total_pct", 14.95)
    gsf_atual = 0.76
    rap_total = trans_data.get("kpis_resumo", {}).get("rap_total_nacional_rs_mm", 38400.0)
    ebitda_total = fin_data.get("indicadores_setoriais", {}).get("ebitda_total_setor_rs_mm", 64800.0)
    bandeira = ccee_data.get("bandeira_vigente", {}).get("bandeira", "Verde")

    # Value chain matrix
    matrix = [
        {"categoria": "Qualidade do Fornecimento", "cadeia": ["Distribuição"], "owner": "COO", "kpis": "DEC, FEC, DIC, DRP", "status": "Atenção (Enel SP/Light)", "nivel": "alerta"},
        {"categoria": "Operação SIN & Hidrologia", "cadeia": ["Geração", "Transmissão"], "owner": "CFO", "kpis": f"EAR ({ear_total}%), ENA (88.5% MLT), CMO (R$ {cmo_medio})", "status": ear_status, "nivel": "sucesso" if ear_total >= 50 else "alerta"},
        {"categoria": "Atendimento Comercial", "cadeia": ["Distribuição"], "owner": "COO", "kpis": "IASC, INS (87.4%), Ouvidoria", "status": "Conforme", "nivel": "sucesso"},
        {"categoria": "Transmissão & Disponibilidade", "cadeia": ["Transmissão"], "owner": "COO / CFO", "kpis": "RAP (R$ 38.4B), PVd (R$ 215M), ENS", "status": "Alta Disponibilidade (99.88%)", "nivel": "sucesso"},
        {"categoria": "Perdas & Geração Distribuída", "cadeia": ["Distribuição"], "owner": "COO", "kpis": f"Perdas ({perda_total_pct}%), MMGD (31.8 GW)", "status": "Crítico (Light/PA) & Expansão GD" if perda_total_pct > 15 else "Conforme", "nivel": "critico" if perda_total_pct > 15 else "alerta"},
        {"categoria": "Comercialização & Mercado CCEE", "cadeia": ["Geração", "Comercialização"], "owner": "CFO", "kpis": "PLD (R$ 69.45), GSF (0.76), Curtailment", "status": "Alerta GSF & Curtailment NE", "nivel": "critico"},
        {"categoria": "Econômico-Financeiro & Ativos", "cadeia": ["Geração", "Transmissão", "Distribuição", "Comercialização"], "owner": "CEO / CFO", "kpis": "EBITDA, CAPEX, BRR, Ativos Órfãos", "status": "Alavancagem Saudável (2.45x)", "nivel": "sucesso"},
    ]

    return {
        "subsystem_selected": subsystem,
        "kpis_destaque": {
            "ear_sin_pct": {"valor": ear_total, "meta": 45.0, "unidade": "%", "status": ear_status, "tendencia": "estavel"},
            "cmo_medio_sin": {"valor": cmo_medio, "unidade": "R$/MWh", "status": "Normal" if cmo_medio < 150 else "Elevado", "tendencia": "baixa"},
            "pld_medio": {"valor": pld_medio, "teto": 678.85, "piso": 61.07, "unidade": "R$/MWh", "status": "Piso/Normal"},
            "gsf_risco_hidro": {"valor": gsf_atual, "alerta": "Crítico (<0.80)", "unidade": "fator", "status": "Risco Elevado"},
            "rap_nacional": {"valor": rap_total, "unidade": "R$ MM", "status": "Contratada"},
            "perdas_totais": {"valor": perda_total_pct, "meta": 12.80, "unidade": "%", "status": "Acima da Meta" if perda_total_pct > 12.8 else "Conforme"},
            "ebitda_setorial": {"valor": ebitda_total, "unidade": "R$ MM", "status": "Sólido"},
            "bandeira_tarifaria": {"valor": bandeira, "adicional": "R$ 0,00/kWh", "status": "Verde"}
        },
        "matriz_sintese": matrix,
        "subsistemas_resumo": SUBSYSTEMS,
        "alertas_recentes": alerts_data[:3]
    }
