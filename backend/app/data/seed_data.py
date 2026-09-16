import datetime

SUBSYSTEMS = [
    {"id": "SE_CO", "name": "Sudeste / Centro-Oeste", "uf_list": ["SP", "RJ", "MG", "ES", "GO", "MT", "MS", "DF"], "peso_carga": 0.58},
    {"id": "S", "name": "Sul", "uf_list": ["RS", "SC", "PR"], "peso_carga": 0.17},
    {"id": "NE", "name": "Nordeste", "uf_list": ["BA", "PE", "CE", "MA", "PB", "RN", "AL", "SE", "PI"], "peso_carga": 0.18},
    {"id": "N", "name": "Norte", "uf_list": ["PA", "AM", "TO", "RO", "AP", "AC", "RR"], "peso_carga": 0.07},
]

DISTRIBUTORS = [
    {"sigla": "ENEL_SP", "nome": "Enel Distribuição São Paulo", "uf": "SP", "subsistema": "SE_CO", "clientes": 7800000, "porte": "Grande"},
    {"sigla": "CPFL_PAULISTA", "nome": "CPFL Paulista", "uf": "SP", "subsistema": "SE_CO", "clientes": 4900000, "porte": "Grande"},
    {"sigla": "CEMIG_D", "nome": "Cemig Distribuição", "uf": "MG", "subsistema": "SE_CO", "clientes": 8900000, "porte": "Grande"},
    {"sigla": "COPEL_DIS", "nome": "Copel Distribuição", "uf": "PR", "subsistema": "S", "clientes": 5100000, "porte": "Grande"},
    {"sigla": "CELESC", "nome": "Celesc Distribuição", "uf": "SC", "subsistema": "S", "clientes": 3400000, "porte": "Médio"},
    {"sigla": "RGE_SUL", "nome": "RGE Sul", "uf": "RS", "subsistema": "S", "clientes": 3100000, "porte": "Médio"},
    {"sigla": "NEOENERGIA_COELBA", "nome": "Neoenergia Coelba", "uf": "BA", "subsistema": "NE", "clientes": 6500000, "porte": "Grande"},
    {"sigla": "NEOENERGIA_PERNAMBUCO", "nome": "Neoenergia Pernambuco (Celpe)", "uf": "PE", "subsistema": "NE", "clientes": 3900000, "porte": "Médio"},
    {"sigla": "EQUATORIAL_MA", "nome": "Equatorial Maranhão", "uf": "MA", "subsistema": "NE", "clientes": 2700000, "porte": "Médio"},
    {"sigla": "EQUATORIAL_GO", "nome": "Equatorial Goiás", "uf": "GO", "subsistema": "SE_CO", "clientes": 3300000, "porte": "Médio"},
    {"sigla": "LIGHT", "nome": "Light Serviços de Eletricidade", "uf": "RJ", "subsistema": "SE_CO", "clientes": 4100000, "porte": "Grande"},
    {"sigla": "EQUATORIAL_PA", "nome": "Equatorial Pará", "uf": "PA", "subsistema": "N", "clientes": 2900000, "porte": "Médio"},
    {"sigla": "ENERGISA_MT", "nome": "Energisa Mato Grosso", "uf": "MT", "subsistema": "SE_CO", "clientes": 1600000, "porte": "Médio"},
]

TRANSMITTERS = [
    {"nome": "ISA CTEEP", "rap_base_mm": 5420.0, "extensao_km": 21500, "ativos": 128},
    {"nome": "TAESA", "rap_base_mm": 3890.0, "extensao_km": 14200, "ativos": 96},
    {"nome": "ELETROBRAS FURNAS", "rap_base_mm": 6120.0, "extensao_km": 30200, "ativos": 154},
    {"nome": "ALUPAR", "rap_base_mm": 2450.0, "extensao_km": 8200, "ativos": 48},
    {"nome": "EQUATORIAL TRANSMISSÃO", "rap_base_mm": 1380.0, "extensao_km": 4900, "ativos": 32},
    {"nome": "ENGIE TRANSMISSÃO", "rap_base_mm": 1920.0, "extensao_km": 6800, "ativos": 42}
]

# Curated Seed Data
SEED_DATA = {
    "operacao_sin": {
        "ear_subsistemas": [
            {"data_referencia": "2026-08-01", "subsistema": "SE_CO", "ear_percentual": 64.8, "ear_max_mwmes": 204500, "ear_atual_mwmes": 132516, "meta_seguranca_percentual": 45.0, "status_criticidade": "Favorável"},
            {"data_referencia": "2026-08-01", "subsistema": "S", "ear_percentual": 78.2, "ear_max_mwmes": 20200, "ear_atual_mwmes": 15796, "meta_seguranca_percentual": 50.0, "status_criticidade": "Favorável"},
            {"data_referencia": "2026-08-01", "subsistema": "NE", "ear_percentual": 56.4, "ear_max_mwmes": 51800, "ear_atual_mwmes": 29215, "meta_seguranca_percentual": 40.0, "status_criticidade": "Atenção Moderada"},
            {"data_referencia": "2026-08-01", "subsistema": "N", "ear_percentual": 82.5, "ear_max_mwmes": 15300, "ear_atual_mwmes": 12622, "meta_seguranca_percentual": 45.0, "status_criticidade": "Favorável"},
        ],
        "ear_historico_meses": [
            {"mes": "Jan/26", "SE_CO": 74.2, "S": 88.5, "NE": 68.1, "N": 91.0, "SIN_Total": 76.4},
            {"mes": "Fev/26", "SE_CO": 72.5, "S": 84.1, "NE": 65.4, "N": 89.2, "SIN_Total": 74.3},
            {"mes": "Mar/26", "SE_CO": 70.8, "S": 82.0, "NE": 63.0, "N": 87.5, "SIN_Total": 72.1},
            {"mes": "Abr/26", "SE_CO": 68.9, "S": 80.4, "NE": 61.2, "N": 86.0, "SIN_Total": 70.2},
            {"mes": "Mai/26", "SE_CO": 67.1, "S": 79.1, "NE": 59.5, "N": 84.8, "SIN_Total": 68.4},
            {"mes": "Jun/26", "SE_CO": 66.0, "S": 78.5, "NE": 58.0, "N": 83.9, "SIN_Total": 67.2},
            {"mes": "Jul/26", "SE_CO": 65.2, "S": 78.0, "NE": 57.1, "N": 83.1, "SIN_Total": 66.3},
            {"mes": "Ago/26", "SE_CO": 64.8, "S": 78.2, "NE": 56.4, "N": 82.5, "SIN_Total": 65.8}
        ],
        "ena_subsistemas": [
            {"subsistema": "SE_CO", "ena_mwmed": 28400, "ena_percentual_mlt": 88.5, "classificacao": "Próximo à Média"},
            {"subsistema": "S", "ena_mwmed": 9650, "ena_percentual_mlt": 112.4, "classificacao": "Acima da Média"},
            {"subsistema": "NE", "ena_mwmed": 4120, "ena_percentual_mlt": 72.8, "classificacao": "Abaixo da Média"},
            {"subsistema": "N", "ena_mwmed": 3890, "ena_percentual_mlt": 84.1, "classificacao": "Moderado"},
        ],
        "cmo_atual": [
            {"subsistema": "SE_CO", "cmo_rs_mwh": 68.42, "patamar_leve": 61.20, "patamar_medio": 68.42, "patamar_pesado": 79.50, "despacho_termico_mw": 3450},
            {"subsistema": "S", "cmo_rs_mwh": 65.10, "patamar_leve": 59.80, "patamar_medio": 65.10, "patamar_pesado": 74.20, "despacho_termico_mw": 820},
            {"subsistema": "NE", "cmo_rs_mwh": 74.90, "patamar_leve": 66.30, "patamar_medio": 74.90, "patamar_pesado": 86.10, "despacho_termico_mw": 2100},
            {"subsistema": "N", "cmo_rs_mwh": 63.80, "patamar_leve": 58.40, "patamar_medio": 63.80, "patamar_pesado": 71.30, "despacho_termico_mw": 680},
        ],
        "cmo_historico": [
            {"data": "01/08", "SE_CO": 64.2, "S": 61.0, "NE": 71.5, "N": 60.1},
            {"data": "05/08", "SE_CO": 66.8, "S": 63.4, "NE": 73.2, "N": 62.0},
            {"data": "10/08", "SE_CO": 69.1, "S": 66.0, "NE": 76.4, "N": 64.5},
            {"data": "15/08", "SE_CO": 67.5, "S": 64.8, "NE": 74.1, "N": 63.2},
            {"data": "19/08", "SE_CO": 68.4, "S": 65.1, "NE": 74.9, "N": 63.8},
        ]
    },
    "mercado_ccee": {
        "pld_atual": {
            "pld_medio_rs_mwh": 69.45,
            "pld_teto_rs_mwh": 678.85,
            "pld_piso_rs_mwh": 61.07,
            "subsistemas": [
                {"subsistema": "SE_CO", "pld_rs_mwh": 68.42, "status": "Dentro da Normalidade"},
                {"subsistema": "S", "pld_rs_mwh": 65.10, "status": "Dentro da Normalidade"},
                {"subsistema": "NE", "pld_rs_mwh": 74.90, "status": "Descolamento por Restrição"},
                {"subsistema": "N", "pld_rs_mwh": 63.80, "status": "Dentro da Normalidade"},
            ]
        },
        "gsf_historico": [
            {"mes": "Jan/26", "gsf": 0.89, "alerta": "Normal"},
            {"mes": "Fev/26", "gsf": 0.92, "alerta": "Normal"},
            {"mes": "Mar/26", "gsf": 0.88, "alerta": "Normal"},
            {"mes": "Abr/26", "gsf": 0.84, "alerta": "Atenção"},
            {"mes": "Mai/26", "gsf": 0.81, "alerta": "Atenção"},
            {"mes": "Jun/26", "gsf": 0.79, "alerta": "Crítico"},
            {"mes": "Jul/26", "gsf": 0.77, "alerta": "Crítico"},
            {"mes": "Ago/26", "gsf": 0.76, "alerta": "Crítico"},
        ],
        "ess_encargos": {
            "total_mes_rs_mm": 482.6,
            "categorias": [
                {"tipo": "Segurança Energética (Despacho Térmico)", "valor_rs_mm": 298.4, "pct": 61.8},
                {"tipo": "Restrição Elétrica de Transmissão", "valor_rs_mm": 134.2, "pct": 27.8},
                {"tipo": "Unit Commitment e Reserva de Capacidade", "valor_rs_mm": 50.0, "pct": 10.4},
            ]
        },
        "bandeira_vigente": {
            "bandeira": "Verde",
            "adicional_rs_kwh": 0.00,
            "previsao_proximo_mes": "Verde / Baixa probabilidade de Amarela",
            "justificativa": "Condições de armazenamento favoráveis nos reservatórios do Sudeste/Sul."
        },
        "curtailment": [
            {"subsistema": "NE", "fonte": "Eólica", "gerada_gwh": 7450, "cortada_gwh": 890, "taxa_curtailment_pct": 10.7, "motivo": "Gargalo de Transmissão NE->SE"},
            {"subsistema": "NE", "fonte": "Solar", "gerada_gwh": 2980, "cortada_gwh": 410, "taxa_curtailment_pct": 12.1, "motivo": "Restrição Operativa ONS"},
            {"subsistema": "N", "fonte": "Solar", "gerada_gwh": 650, "cortada_gwh": 35, "taxa_curtailment_pct": 5.1, "motivo": "Fluxo no tronco Norte-Sul"},
        ]
    },
    "transmissao": {
        "kpis_resumo": {
            "rap_total_nacional_rs_mm": 38400.0,
            "pvd_total_ano_rs_mm": 215.8,
            "disponibilidade_media_linhas_pct": 99.88,
            "disponibilidade_media_transformadores_pct": 99.72,
            "ens_total_mwh": 1420.5
        },
        "concessionarias": [
            {"nome": "ISA CTEEP", "rap_homologada_rs_mm": 5420.0, "pvd_rs_mm": 24.5, "disponibilidade_pct": 99.91, "ens_mwh": 180.2, "status": "Excelente"},
            {"nome": "TAESA", "rap_homologada_rs_mm": 3890.0, "pvd_rs_mm": 14.2, "disponibilidade_pct": 99.94, "ens_mwh": 95.0, "status": "Excelente"},
            {"nome": "ELETROBRAS FURNAS", "rap_homologada_rs_mm": 6120.0, "pvd_rs_mm": 48.6, "disponibilidade_pct": 99.81, "ens_mwh": 420.0, "status": "Atenção"},
            {"nome": "ALUPAR", "rap_homologada_rs_mm": 2450.0, "pvd_rs_mm": 8.9, "disponibilidade_pct": 99.95, "ens_mwh": 45.3, "status": "Excelente"},
            {"nome": "EQUATORIAL TRANSMISSÃO", "rap_homologada_rs_mm": 1380.0, "pvd_rs_mm": 11.2, "disponibilidade_pct": 99.85, "ens_mwh": 110.0, "status": "Conforme"},
            {"nome": "ENGIE TRANSMISSÃO", "rap_homologada_rs_mm": 1920.0, "pvd_rs_mm": 7.4, "disponibilidade_pct": 99.93, "ens_mwh": 62.1, "status": "Excelente"}
        ],
        "desligamentos_recentes": [
            {"data": "14/08/2026", "concessionaria": "ELETROBRAS FURNAS", "ativo": "LT 500kV Itumbiara-Campinas", "duracao_h": 2.4, "pvd_rs_mil": 420.0, "causa": "Descarga Atmosférica"},
            {"data": "08/08/2026", "concessionaria": "ISA CTEEP", "ativo": "SE 440kV Embu-Guaçu TR-02", "duracao_h": 1.1, "pvd_rs_mil": 185.0, "causa": "Falha em Bucha de Passagem"},
            {"data": "02/08/2026", "concessionaria": "EQUATORIAL TRANSMISSÃO", "ativo": "LT 230kV Miracema-Palmas", "duracao_h": 3.8, "pvd_rs_mil": 310.0, "causa": "Queimada sob a Faixa de Servidão"}
        ]
    },
    "distribuicao_qualidade": {
        "ranking_dec_fec": [
            {"distribuidora": "CPFL_PAULISTA", "nome": "CPFL Paulista", "uf": "SP", "dec": 6.82, "meta_dec": 8.10, "fec": 4.12, "meta_fec": 5.40, "status": "Conforme", "compensacao_rs_mm": 4.2},
            {"distribuidora": "COPEL_DIS", "nome": "Copel", "uf": "PR", "dec": 7.15, "meta_dec": 8.50, "fec": 4.60, "meta_fec": 5.80, "status": "Conforme", "compensacao_rs_mm": 5.1},
            {"distribuidora": "CELESC", "nome": "Celesc", "uf": "SC", "dec": 9.40, "meta_dec": 10.20, "fec": 6.30, "meta_fec": 7.10, "status": "Conforme", "compensacao_rs_mm": 7.8},
            {"distribuidora": "ENEL_SP", "nome": "Enel São Paulo", "uf": "SP", "dec": 11.45, "meta_dec": 9.20, "fec": 6.10, "meta_fec": 5.80, "status": "Não Conforme (DEC)", "compensacao_rs_mm": 38.5},
            {"distribuidora": "CEMIG_D", "nome": "Cemig Distribuição", "uf": "MG", "dec": 9.80, "meta_dec": 9.50, "fec": 5.90, "meta_fec": 6.00, "status": "Atenção Limite", "compensacao_rs_mm": 19.4},
            {"distribuidora": "RGE_SUL", "nome": "RGE Sul", "uf": "RS", "dec": 12.80, "meta_dec": 11.50, "fec": 6.90, "meta_fec": 6.80, "status": "Não Conforme (Eventos Climáticos)", "compensacao_rs_mm": 24.2},
            {"distribuidora": "LIGHT", "nome": "Light", "uf": "RJ", "dec": 10.90, "meta_dec": 9.80, "fec": 5.40, "meta_fec": 5.20, "status": "Não Conforme (DEC/FEC)", "compensacao_rs_mm": 29.8},
            {"distribuidora": "NEOENERGIA_COELBA", "nome": "Neoenergia Coelba", "uf": "BA", "dec": 11.20, "meta_dec": 12.00, "fec": 6.40, "meta_fec": 7.00, "status": "Conforme", "compensacao_rs_mm": 21.0},
            {"distribuidora": "EQUATORIAL_GO", "nome": "Equatorial Goiás", "uf": "GO", "dec": 14.10, "meta_dec": 12.50, "fec": 8.90, "meta_fec": 8.00, "status": "Crítico", "compensacao_rs_mm": 41.2},
            {"distribuidora": "EQUATORIAL_PA", "nome": "Equatorial Pará", "uf": "PA", "dec": 18.50, "meta_dec": 17.20, "fec": 11.20, "meta_fec": 10.80, "status": "Crítico", "compensacao_rs_mm": 35.6}
        ],
        "tensao_conformidade": {
            "drp_medio_nacional_pct": 1.45,
            "drc_medio_nacional_pct": 0.42,
            "penalidades_tensao_total_rs_mm": 18.4
        }
    },
    "perdas_mmgd": {
        "balanco_nacional": {
            "energia_injetada_total_twh": 512.4,
            "energia_faturada_total_twh": 435.8,
            "perdas_tecnicas_twh": 41.2, # ~8.04%
            "perdas_nao_tecnicas_twh": 35.4, # ~6.91%
            "perda_total_pct": 14.95,
            "meta_regulatoria_media_pct": 12.80
        },
        "perdas_por_distribuidora": [
            {"distribuidora": "LIGHT", "uf": "RJ", "perda_tecnica_pct": 7.8, "perda_nao_tecnica_pct": 16.4, "perda_total_pct": 24.2, "meta_aneel_pct": 18.5, "impacto_ebitda_rs_mm": -480.0},
            {"distribuidora": "EQUATORIAL_PA", "uf": "PA", "perda_tecnica_pct": 8.2, "perda_nao_tecnica_pct": 15.1, "perda_total_pct": 23.3, "meta_aneel_pct": 17.2, "impacto_ebitda_rs_mm": -320.0},
            {"distribuidora": "ENEL_SP", "uf": "SP", "perda_tecnica_pct": 5.9, "perda_nao_tecnica_pct": 4.3, "perda_total_pct": 10.2, "meta_aneel_pct": 9.8, "impacto_ebitda_rs_mm": -95.0},
            {"distribuidora": "CEMIG_D", "uf": "MG", "perda_tecnica_pct": 7.4, "perda_nao_tecnica_pct": 3.8, "perda_total_pct": 11.2, "meta_aneel_pct": 10.9, "impacto_ebitda_rs_mm": -60.0},
            {"distribuidora": "CPFL_PAULISTA", "uf": "SP", "perda_tecnica_pct": 6.1, "perda_nao_tecnica_pct": 2.4, "perda_total_pct": 8.5, "meta_aneel_pct": 8.7, "impacto_ebitda_rs_mm": 18.0},
            {"distribuidora": "COPEL_DIS", "uf": "PR", "perda_tecnica_pct": 6.3, "perda_nao_tecnica_pct": 1.9, "perda_total_pct": 8.2, "meta_aneel_pct": 8.4, "impacto_ebitda_rs_mm": 15.0},
        ],
        "mmgd_estatisticas": {
            "potencia_instalada_total_gw": 31.8,
            "qtd_unidades_consumidoras_gd": 2840000,
            "energia_autogerada_ano_twh": 48.5,
            "impacto_perda_mercado_cativo_pct": 9.8,
            "top_ufs_potencia_mw": [
                {"uf": "SP", "potencia_mw": 4650, "conexoes": 415000},
                {"uf": "MG", "potencia_mw": 4120, "conexoes": 348000},
                {"uf": "RS", "potencia_mw": 3280, "conexoes": 295000},
                {"uf": "PR", "potencia_mw": 2890, "conexoes": 260000},
                {"uf": "BA", "potencia_mw": 2150, "conexoes": 189000},
                {"uf": "GO", "potencia_mw": 1980, "conexoes": 172000},
            ]
        },
        "inadimplencia_pdd": [
            {"distribuidora": "CPFL_PAULISTA", "taxa_inadimplencia_pct": 1.15, "pdd_rs_mm": 98.4, "status": "Excelente"},
            {"distribuidora": "COPEL_DIS", "taxa_inadimplencia_pct": 1.28, "pdd_rs_mm": 84.2, "status": "Excelente"},
            {"distribuidora": "CEMIG_D", "taxa_inadimplencia_pct": 2.10, "pdd_rs_mm": 210.0, "status": "Adequado"},
            {"distribuidora": "ENEL_SP", "taxa_inadimplencia_pct": 3.45, "pdd_rs_mm": 490.0, "status": "Atenção"},
            {"distribuidora": "LIGHT", "taxa_inadimplencia_pct": 5.80, "pdd_rs_mm": 680.0, "status": "Crítico"},
            {"distribuidora": "EQUATORIAL_MA", "taxa_inadimplencia_pct": 4.90, "pdd_rs_mm": 240.0, "status": "Crítico"},
        ]
    },
    "atendimento_cliente": {
        "ranking_iasc": [
            {"posicao": 1, "distribuidora": "CPFL Santa Cruz", "score": 83.4, "porte": "Médio"},
            {"posicao": 2, "distribuidora": "Copel", "score": 79.8, "porte": "Grande"},
            {"posicao": 3, "distribuidora": "CPFL Paulista", "score": 78.5, "porte": "Grande"},
            {"posicao": 4, "distribuidora": "Celesc", "score": 74.2, "porte": "Médio"},
            {"posicao": 5, "distribuidora": "Cemig", "score": 71.0, "porte": "Grande"},
            {"posicao": 8, "distribuidora": "Enel SP", "score": 63.4, "porte": "Grande"},
            {"posicao": 11, "distribuidora": "Light", "score": 58.9, "porte": "Grande"},
        ],
        "canais_atendimento": {
            "ins_medio_nacional_pct": 87.4, # Meta: > 85%
            "iab_medio_nacional_pct": 3.2,  # Meta: < 5%
            "tma_medio_segundos": 142.0,
            "distribuidoras": [
                {"distribuidora": "CPFL_PAULISTA", "ins_pct": 92.4, "iab_pct": 1.8, "tma_s": 128, "status": "Conforme"},
                {"distribuidora": "COPEL_DIS", "ins_pct": 91.0, "iab_pct": 2.1, "tma_s": 134, "status": "Conforme"},
                {"distribuidora": "CEMIG_D", "ins_pct": 86.8, "iab_pct": 3.4, "tma_s": 148, "status": "Conforme"},
                {"distribuidora": "ENEL_SP", "ins_pct": 81.5, "iab_pct": 5.9, "tma_s": 185, "status": "Não Conforme (IAb > 5%)"},
                {"distribuidora": "EQUATORIAL_GO", "ins_pct": 82.0, "iab_pct": 5.4, "tma_s": 172, "status": "Atenção"},
            ]
        },
        "slas_comerciais": [
            {"servico": "Ligação Nova Urbana", "sla_aneel_dias": 2, "tempo_medio_dias": 1.6, "cumprimento_pct": 96.8},
            {"servico": "Ligação Nova Rural", "sla_aneel_dias": 5, "tempo_medio_dias": 3.9, "cumprimento_pct": 94.2},
            {"servico": "Religação Normal Urbana", "sla_aneel_horas": 24, "tempo_medio_horas": 14.5, "cumprimento_pct": 97.4},
            {"servico": "Religação de Urgência", "sla_aneel_horas": 4, "tempo_medio_horas": 2.8, "cumprimento_pct": 98.1},
            {"servico": "Ressarcimento Danos Elétricos", "sla_aneel_dias": 15, "tempo_medio_dias": 11.2, "cumprimento_pct": 91.5},
        ],
        "ouvidoria_aneel": [
            {"tipologia": "Faturamento / Cobrança Indevida", "reclamacoes_mes": 14500, "pct_total": 42.1, "tempo_resolucao_dias": 4.8},
            {"tipologia": "Interrupção de Fornecimento / Demora", "reclamacoes_mes": 11200, "pct_total": 32.5, "tempo_resolucao_dias": 3.2},
            {"tipologia": "Danos a Equipamentos Elétricos", "reclamacoes_mes": 4800, "pct_total": 13.9, "tempo_resolucao_dias": 8.4},
            {"tipologia": "Atendimento Comercial / Falha no Canal", "reclamacoes_mes": 3950, "pct_total": 11.5, "tempo_resolucao_dias": 5.1},
        ]
    },
    "financeiro_proret": {
        "indicadores_setoriais": {
            "ebitda_total_setor_rs_mm": 64800.0,
            "margem_ebitda_media_pct": 34.2,
            "capex_executado_ano_rs_mm": 42500.0,
            "alavancagem_media_dl_ebitda": 2.45,
            "dividend_yield_medio_pct": 7.8
        },
        "empresas_dre": [
            {"empresa": "CPFL Energia", "receita_liquida_rs_mm": 39800.0, "ebitda_rs_mm": 12450.0, "margem_ebitda_pct": 31.3, "lucro_liquido_rs_mm": 5120.0, "capex_rs_mm": 5200.0, "alavancagem": 2.1},
            {"empresa": "Cemig", "receita_liquida_rs_mm": 36500.0, "ebitda_rs_mm": 8900.0, "margem_ebitda_pct": 24.4, "lucro_liquido_rs_mm": 4850.0, "capex_rs_mm": 3800.0, "alavancagem": 1.8},
            {"empresa": "Copel", "receita_liquida_rs_mm": 23400.0, "ebitda_rs_mm": 5800.0, "margem_ebitda_pct": 24.8, "lucro_liquido_rs_mm": 2900.0, "capex_rs_mm": 2600.0, "alavancagem": 1.9},
            {"empresa": "ISA CTEEP (Transmissão)", "receita_liquida_rs_mm": 4350.0, "ebitda_rs_mm": 3480.0, "margem_ebitda_pct": 80.0, "lucro_liquido_rs_mm": 2150.0, "capex_rs_mm": 1950.0, "alavancagem": 2.6},
            {"empresa": "TAESA (Transmissão)", "receita_liquida_rs_mm": 3600.0, "ebitda_rs_mm": 3100.0, "margem_ebitda_pct": 86.1, "lucro_liquido_rs_mm": 1890.0, "capex_rs_mm": 1450.0, "alavancagem": 3.7},
            {"empresa": "Equatorial Energia", "receita_liquida_rs_mm": 38200.0, "ebitda_rs_mm": 9150.0, "margem_ebitda_pct": 24.0, "lucro_liquido_rs_mm": 2640.0, "capex_rs_mm": 4900.0, "alavancagem": 3.2},
            {"empresa": "Neoenergia", "receita_liquida_rs_mm": 44100.0, "ebitda_rs_mm": 11800.0, "margem_ebitda_pct": 26.8, "lucro_liquido_rs_mm": 4100.0, "capex_rs_mm": 8600.0, "alavancagem": 3.4}
        ],
        "parametros_proret_padrao": {
            "distribuidora_exemplo": "CPFL Paulista",
            "brr_liquida_rs_mm": 14200.0,
            "wacc_regulatorio_pct": 7.32,  # WACC Real após impostos da ANEEL
            "opex_eficiente_rs_mm": 2150.0,
            "fator_x_pct": 0.85,
            "componente_q_pct": -0.15,     # Bônus por melhora de DEC/FEC
            "mercado_faturado_gwh": 28500.0
        },
        "qualidade_dados_ativos": [
            {"distribuidora": "CPFL_PAULISTA", "acuracia_brr_pct": 99.4, "ativos_orfaos_pct": 0.35, "consistencia_uc_medidor_pct": 99.8, "lead_time_capitalizacao_dias": 34.0, "status": "Excelente"},
            {"distribuidora": "COPEL_DIS", "acuracia_brr_pct": 99.1, "ativos_orfaos_pct": 0.42, "consistencia_uc_medidor_pct": 99.7, "lead_time_capitalizacao_dias": 38.0, "status": "Excelente"},
            {"distribuidora": "CEMIG_D", "acuracia_brr_pct": 98.2, "ativos_orfaos_pct": 1.15, "consistencia_uc_medidor_pct": 98.9, "lead_time_capitalizacao_dias": 52.0, "status": "Adequado"},
            {"distribuidora": "ENEL_SP", "acuracia_brr_pct": 97.4, "ativos_orfaos_pct": 2.40, "consistencia_uc_medidor_pct": 97.8, "lead_time_capitalizacao_dias": 68.0, "status": "Atenção"},
            {"distribuidora": "LIGHT", "acuracia_brr_pct": 96.1, "ativos_orfaos_pct": 3.85, "consistencia_uc_medidor_pct": 96.2, "lead_time_capitalizacao_dias": 84.0, "status": "Crítico"},
            {"distribuidora": "EQUATORIAL_GO", "acuracia_brr_pct": 96.8, "ativos_orfaos_pct": 2.90, "consistencia_uc_medidor_pct": 97.1, "lead_time_capitalizacao_dias": 75.0, "status": "Atenção"},
        ]
    },
    "alertas_regulatorios": [
        {
            "id": "ALT-001",
            "nivel": "critico",
            "modulo": "Comercialização / CCEE",
            "titulo": "GSF abaixo de 0.80 (Risco Hidrológico Elevado)",
            "descricao": "GSF apurado em 0.76 no mês atual. Exposição financeira estimada de geradores no MCP de R$ 850 MM.",
            "data_evento": "2026-08-18"
        },
        {
            "id": "ALT-002",
            "nivel": "critico",
            "modulo": "Distribuição / Qualidade",
            "titulo": "DEC acima do Limite Regulatório ANEEL",
            "descricao": "Enel SP apurou DEC de 11.45h vs limite ANEEL de 9.20h (+24.4% de desvio). Risco de ressarcimento Módulo 9.",
            "data_evento": "2026-08-15"
        },
        {
            "id": "ALT-003",
            "nivel": "alerta",
            "modulo": "Comercialização / CCEE",
            "titulo": "Curtailment Solar/Eólico no Nordeste > 10%",
            "descricao": "Corte de geração eólica de 10.7% e solar de 12.1% no subsistema Nordeste por saturação do tronco de transmissão.",
            "data_evento": "2026-08-17"
        },
        {
            "id": "ALT-004",
            "nivel": "alerta",
            "modulo": "Perdas / MMGD",
            "titulo": "Perdas Não-Técnicas Severas (Light e Equatorial Pará)",
            "descricao": "Light com 16.4% e Equatorial PA com 15.1% de perdas por furto/fraude, superando as trajetórias regulatórias da ANEEL.",
            "data_evento": "2026-08-10"
        },
        {
            "id": "ALT-005",
            "nivel": "info",
            "modulo": "Operação SIN",
            "titulo": "EAR do SIN em nível seguro (65.8%)",
            "descricao": "Nível de armazenamento agregado mantém folga confortável em relação à curva guia de segurança energética do ONS.",
            "data_evento": "2026-08-19"
        }
    ]
}
