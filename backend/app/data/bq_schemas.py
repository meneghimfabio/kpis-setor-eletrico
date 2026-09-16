from google.cloud import bigquery

SCHEMAS = {
    "operacao_sin": {
        "ear_subsistemas": [
            bigquery.SchemaField("data_referencia", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("subsistema", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("ear_percentual", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("ear_max_mwmes", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("ear_atual_mwmes", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("meta_seguranca_percentual", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("status_criticidade", "STRING", mode="REQUIRED"),
        ],
        "ena_historico": [
            bigquery.SchemaField("data_referencia", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("subsistema", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("ena_mwmed", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("ena_percentual_mlt", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("classificacao_hidrologica", "STRING", mode="REQUIRED"),
        ],
        "cmo_horario_semanal": [
            bigquery.SchemaField("data_referencia", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("patamar_carga", "STRING", mode="REQUIRED"), # Leve, Media, Pesada
            bigquery.SchemaField("subsistema", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("cmo_rs_mwh", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("despacho_termico_mw", "FLOAT", mode="REQUIRED"),
        ]
    },
    "mercado_ccee": {
        "pld_horario": [
            bigquery.SchemaField("data_hora", "TIMESTAMP", mode="REQUIRED"),
            bigquery.SchemaField("subsistema", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("pld_rs_mwh", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("pld_teto_rs_mwh", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("pld_piso_rs_mwh", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("patamar", "STRING", mode="REQUIRED"),
        ],
        "gsf_mensal": [
            bigquery.SchemaField("mes_ano", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("gsf_fator", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("exposicao_financeira_rs_mm", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("alerta_risco", "STRING", mode="REQUIRED"),
        ],
        "ess_encargos": [
            bigquery.SchemaField("mes_ano", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("tipo_encargo", "STRING", mode="REQUIRED"), # Seguranca Energetica, Restricao Eletrica, Unit Commitment
            bigquery.SchemaField("valor_rs_milhoes", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("impacto_tarifa_rs_mwh", "FLOAT", mode="REQUIRED"),
        ],
        "bandeiras_tarifarias": [
            bigquery.SchemaField("mes_ano", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("bandeira_acionada", "STRING", mode="REQUIRED"), # Verde, Amarela, Vermelha P1, Vermelha P2
            bigquery.SchemaField("adicional_rs_kwh", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("justificativa_ons_ccee", "STRING", mode="NULLABLE"),
        ],
        "curtailment_renovaveis": [
            bigquery.SchemaField("data_referencia", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("subsistema", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("fonte", "STRING", mode="REQUIRED"), # Eolica, Solar
            bigquery.SchemaField("energia_gerada_mwh", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("energia_cortada_mwh", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("taxa_curtailment_percentual", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("motivo_restricao", "STRING", mode="REQUIRED"),
        ]
    },
    "transmissao": {
        "concessoes_rap": [
            bigquery.SchemaField("ano_ciclo", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("concessionaria", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("rap_homologada_rs_mm", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("rap_recebida_rs_mm", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("extensao_km", "FLOAT", mode="REQUIRED"),
        ],
        "pvd_deducoes": [
            bigquery.SchemaField("mes_ano", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("concessionaria", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("equipamento_afetado", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("pvd_aplicada_rs_mil", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("duracao_desligamento_horas", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("motivo_intempestivo", "STRING", mode="REQUIRED"),
        ],
        "disponibilidade_linhas_se": [
            bigquery.SchemaField("mes_ano", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("tipo_ativo", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("taxa_disponibilidade_percentual", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("meta_regulatoria_percentual", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("ens_mwh", "FLOAT", mode="REQUIRED"),
        ]
    },
    "distribuicao_qualidade": {
        "dec_fec_distribuidoras": [
            bigquery.SchemaField("ano_mes", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("distribuidora", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("sigla_uf", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("dec_apurado_horas", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("dec_limite_aneel_horas", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("fec_apurado_vezes", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("fec_limite_aneel_vezes", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("conformidade_dec", "BOOLEAN", mode="REQUIRED"),
            bigquery.SchemaField("conformidade_fec", "BOOLEAN", mode="REQUIRED"),
        ],
        "indicadores_individuais_dic_fic": [
            bigquery.SchemaField("ano_mes", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("distribuidora", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("dic_horas", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("fic_vezes", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("dmic_horas", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("dicri_horas", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("compensacao_estimada_rs_mil", "FLOAT", mode="REQUIRED"),
        ],
        "conformidade_tensao_drp_drc": [
            bigquery.SchemaField("ano_mes", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("distribuidora", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("drp_percentual", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("drc_percentual", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("penalidades_tensao_rs_mil", "FLOAT", mode="REQUIRED"),
        ]
    },
    "perdas_mmgd": {
        "balanco_energetico_perdas": [
            bigquery.SchemaField("ano_mes", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("distribuidora", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("energia_injetada_gwh", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("energia_faturada_gwh", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("perdas_tecnicas_gwh", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("perdas_nao_tecnicas_gwh", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("perdas_totais_percentual", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("meta_regulatoria_perdas_pct", "FLOAT", mode="REQUIRED"),
        ],
        "mmgd_potencia_instalada": [
            bigquery.SchemaField("ano_mes", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("uf", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("qtd_conexoes_gd", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("potencia_instalada_kw", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("energia_autogerada_estimada_gwh", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("impacto_mercado_cativo_rs_mm", "FLOAT", mode="REQUIRED"),
        ],
        "inadimplencia_distribuicao": [
            bigquery.SchemaField("ano_mes", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("distribuidora", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("faturamento_bruto_rs_mm", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("arrecadado_rs_mm", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("taxa_inadimplencia_percentual", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("pdd_contabil_rs_mm", "FLOAT", mode="REQUIRED"),
        ]
    },
    "atendimento_cliente": {
        "iasc_satisfacao": [
            bigquery.SchemaField("ano", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("distribuidora", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("score_iasc", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("ranking_nacional", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("categoria_porte", "STRING", mode="REQUIRED"),
        ],
        "niveis_servico_callcenter": [
            bigquery.SchemaField("ano_mes", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("distribuidora", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("ins_percentual", "FLOAT", mode="REQUIRED"), # Nivel de Servico
            bigquery.SchemaField("iab_percentual", "FLOAT", mode="REQUIRED"), # Abandono
            bigquery.SchemaField("tma_segundos", "FLOAT", mode="REQUIRED"), # Tempo Medio Atendimento
            bigquery.SchemaField("total_chamadas_recebidas", "INTEGER", mode="REQUIRED"),
        ],
        "prazos_comerciais_sla": [
            bigquery.SchemaField("ano_mes", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("distribuidora", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("tipo_solicitacao", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("tempo_medio_execucao_horas", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("sla_regulatorio_horas", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("cumprimento_sla_percentual", "FLOAT", mode="REQUIRED"),
        ],
        "ouvidoria_reclamacoes": [
            bigquery.SchemaField("ano_mes", "DATE", mode="REQUIRED"),
            bigquery.SchemaField("distribuidora", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("tipologia_reclamacao", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("quantidade_escalacoes", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("procedencia_percentual", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("tempo_resolucao_dias", "FLOAT", mode="REQUIRED"),
        ]
    },
    "financeiro_ativos": {
        "dre_ebitda_trimestral": [
            bigquery.SchemaField("trimestre", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("empresa", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("segmento", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("receita_liquida_rs_mm", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("ebitda_rs_mm", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("margem_ebitda_percentual", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("lucro_liquido_rs_mm", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("divida_liquida_rs_mm", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("alavancagem_dl_ebitda", "FLOAT", mode="REQUIRED"),
        ],
        "capex_pmso_pdd": [
            bigquery.SchemaField("ano_trimestre", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("empresa", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("capex_executado_rs_mm", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("capex_regulatorio_rs_mm", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("pmso_realizado_rs_mm", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("pmso_regulatorio_rs_mm", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("eficiencia_opex_percentual", "FLOAT", mode="REQUIRED"),
        ],
        "base_remuneracao_brr": [
            bigquery.SchemaField("ciclo_revisao", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("distribuidora", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("brr_bruta_rs_mm", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("brr_liquida_rs_mm", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("wacc_regulatorio_percentual", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("fator_x_percentual", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("componente_q_percentual", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("acuracia_brr_percentual", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("taxa_ativos_orfaos_percentual", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("lead_time_capitalizacao_dias", "FLOAT", mode="REQUIRED"),
        ]
    }
}
