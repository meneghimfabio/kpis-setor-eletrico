"""
Dicionário de Metadados e Governança Semântica - Setor Elétrico Brasileiro
Google Cloud Knowledge Catalog & BigQuery Dataplex Universal Catalog

Centraliza descrições de negócio C-Level, taxonomias regulatórias
(ANEEL, CCEE, ONS, CVM), esquemas de colunas detalhados, métricas atestadas e Golden Queries
para enriquecimento dos ativos no BigQuery e Knowledge Catalog.
"""

from typing import Dict, List, Any

# ==============================================================================
# 1. METADADOS DOS DATASETS
# ==============================================================================

DATASET_METADATA = {
    "aneel_silver": {
        "description": (
            "Camada Silver de dados regulatórios oficiais da ANEEL (Agência Nacional de Energia Elétrica) e CVM. "
            "Contém dados limpos, deduplicados e tipados de continuidade de fornecimento (DEC/FEC - PRODIST Módulo 8), "
            "expansão da micro e minigeração distribuída (SISGD - Lei 14.300/2022), tarifas homologadas de distribuição "
            "(PRORET - TUSD e TE), reclamações e ouvidoria setorial (IASC), concessões de transmissão (RAP e PVd) "
            "e demonstrações financeiras padronizadas (DFP/ITR CVM das empresas de energia)."
        ),
        "labels": {
            "dataplex-governed": "true",
            "environment": "production",
            "tier": "silver",
            "data-domain": "regulatorio-aneel",
            "data-owner": "regulacao-distribuicao"
        }
    },
    "mercado_ccee": {
        "description": (
            "Camada Silver de dados do Mercado Livre de Energia Elétrica (ACL) apurados pela CCEE "
            "(Câmara de Comercialização de Energia Elétrica). Inclui séries horárias do Preço de Liquidação "
            "das Diferenças (PLD), risco hidrológico do Mecanismo de Realocação de Energia (GSF), "
            "Encargos de Serviço do Sistema (ESS), acionamento de Bandeiras Tarifárias e histórico de Curtailment renovável."
        ),
        "labels": {
            "dataplex-governed": "true",
            "environment": "production",
            "tier": "silver",
            "data-domain": "mercado-ccee",
            "data-owner": "mesa-trading-energia"
        }
    },
    "operacao_sin": {
        "description": (
            "Camada Silver de dados eletroenergéticos operacionais do Sistema Interligado Nacional (SIN) gerados pelo ONS. "
            "Armazena curvas históricas e diárias de Energia Armazenada (EAR %), Energia Natural Afluente (ENA % MLT), "
            "Custo Marginal de Operação (CMO horário/semanal por patamar) e despachos térmicos de segurança energética."
        ),
        "labels": {
            "dataplex-governed": "true",
            "environment": "production",
            "tier": "silver",
            "data-domain": "operacao-ons",
            "data-owner": "operacao-sin"
        }
    },
    "gold_kpis": {
        "description": (
            "Camada Gold analítica executiva com KPIs do Setor Elétrico Brasileiro acelerados via BigQuery BI Engine. "
            "Armazena agregações de alta performance com conformidade regulatória de DEC/FEC vs metas contratuais, "
            "ranking de tarifas homologadas residenciais (B1) e industriais (A4), capacidade instalada de MMGD por UF, "
            "indicadores de ouvidoria/IASC, saúde financeira (EBITDA/alavancagem CVM), integridade do SIN e spreads de PLD."
        ),
        "labels": {
            "dataplex-governed": "true",
            "okf-enabled": "true",
            "environment": "production",
            "tier": "gold",
            "data-domain": "analytics-executivo",
            "data-owner": "diretoria-c-level"
        }
    }
}

# ==============================================================================
# 2. METADADOS DAS TABELAS E COLUNAS
# ==============================================================================

TABLE_METADATA: Dict[str, Dict[str, Any]] = {
    # --------------------------------------------------------------------------
    # GOLD_KPIS
    # --------------------------------------------------------------------------
    "gold_kpis.kpi_dec_fec_conformidade": {
        "description": (
            "Visão executiva da conformidade de qualidade de fornecimento das distribuidoras de energia elétrica. "
            "Compara a Duração Equivalente de Interrupção por Unidade Consumidora (DEC em horas) e a Frequência Equivalente "
            "(FEC em vezes) contra os limites anuais regulatórios fixados pela ANEEL no PRODIST Módulo 8. "
            "Calcula o desvio em horas/vezes, percentual de extrapolação, ranking de qualidade e estimativa de penalidades financeiras."
        ),
        "columns": {
            "data_referencia": "Mês e ano de referência da apuração contábil e regulatória (formato DATE/TIMESTAMP).",
            "distribuidora": "Sigla de identificação regulatória da distribuidora perante a ANEEL (ex: CPFL_PAULISTA, ENEL_SP, CEMIG_D).",
            "nome_concessionaria": "Razão social completa da concessionária ou permissionária de distribuição de energia elétrica.",
            "sigla_uf": "Unidade Federativa (UF) principal de atuação da área de concessão.",
            "dec_apurado_horas": "Duração Equivalente de Interrupção por Unidade Consumidora apurada no período, medida em horas contínuas.",
            "dec_limite_aneel_horas": "Meta regulatória máxima de DEC fixada em contrato de concessão pela Resolução Homologatória da ANEEL.",
            "desvio_dec_horas": "Diferença aritmética absoluta entre DEC apurado e o limite regulatório (horas). Valores positivos denotam infração.",
            "percentual_ultrapassagem_dec": "Percentual de violação do limite regulatório de DEC: ((dec_apurado / dec_limite) - 1) * 100.",
            "conformidade_dec": "Booleano indicando se a distribuidora cumpriu a meta de continuidade (TRUE = Conforme / DEC <= Limite).",
            "fec_apurado_vezes": "Frequência Equivalente de Interrupção apurada no período, medida em quantidade de interrupções.",
            "fec_limite_aneel_vezes": "Limite regulatório máximo de frequência (FEC) homologado pela ANEEL.",
            "desvio_fec_vezes": "Diferença aritmética absoluta entre FEC apurado e limite regulatório (vezes).",
            "percentual_ultrapassagem_fec": "Percentual de violação do limite de frequência de interrupção (FEC).",
            "conformidade_fec": "Booleano indicando conformidade do FEC (TRUE = Conforme / FEC <= Limite).",
            "status_regulatorio": "Classificação executiva: 'Conforme', 'Crítico (DEC e FEC)', 'Atenção (DEC Ultrapassado)' ou 'Atenção (FEC Ultrapassado)'.",
            "compensacao_estimada_rs_mm": "Estimativa paramétrica da compensação financeira obrigatória a ser creditada na fatura dos consumidores (R$ Milhões).",
            "ranking_qualidade_dec": "Posição no ranking nacional de qualidade de fornecimento (1º lugar = menor DEC / maior continuidade)."
        },
        "golden_queries": [
            {
                "title": "Top 10 Distribuidoras com Maior Extrapolação de DEC",
                "sql": (
                    "SELECT distribuidora, sigla_uf, dec_apurado_horas, dec_limite_aneel_horas, "
                    "desvio_dec_horas, percentual_ultrapassagem_dec, compensacao_estimada_rs_mm "
                    "FROM `kpisetoreletrico.gold_kpis.kpi_dec_fec_conformidade` "
                    "WHERE NOT conformidade_dec "
                    "ORDER BY desvio_dec_horas DESC LIMIT 10;"
                )
            }
        ]
    },

    "gold_kpis.kpi_mmgd_expansao_uf": {
        "description": (
            "Indicadores executivos agregados de Micro e Minigeração Distribuída (MMGD) por Estado brasileiro. "
            "Consolida o total de conexões ativas na rede, potência instalada acumulada (MW), projeção de geração de energia mensal (GWh), "
            "market share estadual sobre o parque nacional e subsistema elétrico associado (SIN)."
        ),
        "columns": {
            "sigla_uf": "Unidade Federativa de localização dos empreendimentos de MMGD (27 estados e DF).",
            "subsistema": "Subsistema do Sistema Interligado Nacional (SE_CO, SUL, NORDESTE, NORTE).",
            "ultima_data_referencia": "Data mais recente de atualização da base de dados do SISGD/ANEEL.",
            "total_conexoes": "Quantidade acumulada de unidades geradoras conectadas à rede de distribuição de baixa e média tensão.",
            "potencia_instalada_mw": "Potência operacional instalada de geração distribuída no estado, convertida para Megawatts (MW).",
            "energia_autogerada_gwh_mes": "Estimativa paramétrica de geração de energia elétrica mensal (GWh) baseada em fator de capacidade fotovoltaico médio (~19%).",
            "market_share_nacional_pct": "Participação percentual da potência instalada do estado em relação ao total nacional de MMGD.",
            "ranking_nacional_potencia": "Posição ordinal no ranking brasileiro de capacidade instalada de geração distribuída (1º = maior capacidade instalada)."
        },
        "golden_queries": [
            {
                "title": "Top 5 Estados em Capacidade Instalada de MMGD (MW)",
                "sql": (
                    "SELECT sigla_uf, subsistema, total_conexoes, potencia_instalada_mw, market_share_nacional_pct "
                    "FROM `kpisetoreletrico.gold_kpis.kpi_mmgd_expansao_uf` "
                    "ORDER BY potencia_instalada_mw DESC LIMIT 5;"
                )
            }
        ]
    },

    "gold_kpis.kpi_tarifas_ranking": {
        "description": (
            "Ranking e decomposição das tarifas homologadas de energia elétrica (PRORET) para classe B1 Residencial. "
            "Apresenta a tarifa final de aplicação (R$/kWh) e sua segregação estrutural entre a parcela do fio "
            "(TUSD - Tarifa de Uso do Sistema de Distribuição) e a parcela de suprimento de energia (TE - Tarifa de Energia), "
            "além de parâmetros regulatórios como WACC e Fator X."
        ),
        "columns": {
            "distribuidora": "Sigla da concessionária regulada perante a ANEEL.",
            "concessionaria": "Nome empresarial da empresa distribuidora.",
            "uf": "Unidade Federativa de concessão.",
            "resolucao_homologatoria": "Número oficial da Resolução Homologatória da ANEEL que fixou as tarifas vigentes.",
            "data_vigencia": "Data formal de início de vigência do ciclo tarifário homologado.",
            "tarifa_b1_rs_kwh": "Tarifa homologada de aplicação para consumidores da classe B1 Residencial em Reais por quilowatt-hora (R$/kWh), sem impostos.",
            "tusd_rs_mwh": "Parcela TUSD em R$/MWh referente à remuneração do sistema de distribuição (fio e encargos setoriais).",
            "te_rs_mwh": "Parcela TE em R$/MWh referente à compra de energia e comercialização.",
            "share_tusd_fio_pct": "Participação percentual da parcela TUSD no custo total da tarifa: (TUSD / (TUSD + TE)) * 100.",
            "share_te_energia_pct": "Participação percentual da parcela TE de suprimento de energia no custo total: (TE / (TUSD + TE)) * 100.",
            "wacc_regulatorio_pct": "Taxa de Custo Médio Ponderado de Capital regulatório após impostos definido pela ANEEL.",
            "fator_x_pct": "Fator X de ganhos de produtividade e eficiência repassado às tarifas no reajuste/revisão periódica.",
            "ranking_tarifa_mais_barata": "Posição ordinal no ranking tarifário nacional (1º = tarifa mais barata do Brasil)."
        },
        "golden_queries": [
            {
                "title": "Top 5 Tarifas Mais Caras do Brasil",
                "sql": (
                    "SELECT distribuidora, concessionaria, uf, tarifa_b1_rs_kwh, share_tusd_fio_pct, share_te_energia_pct "
                    "FROM `kpisetoreletrico.gold_kpis.kpi_tarifas_ranking` "
                    "ORDER BY tarifa_b1_rs_kwh DESC LIMIT 5;"
                )
            }
        ]
    },

    "gold_kpis.kpi_ccee_mercado_resumo": {
        "description": (
            "Visão executiva e analítica do Mercado de Curto Prazo (MCP) operado pela CCEE. "
            "Acompanha o Preço de Liquidação das Diferenças (PLD) horário mais recente por submercado (SE/CO, SUL, NE, NORTE), "
            "comparações contra piso e teto regulatórios, spread regional máximo e diagnóstico de desacoplamento do SIN."
        ),
        "columns": {
            "subsistema": "Submercado de comercialização do SIN (SE/CO, SUL, NORDESTE, NORTE).",
            "pld_rs_mwh": "Preço de Liquidação das Diferenças apurado para o submercado em Reais por Megawatt-hora (R$/MWh).",
            "pld_teto_rs_mwh": "Teto estrutural do PLD fixado anualmente pela ANEEL.",
            "pld_piso_rs_mwh": "Piso estrutural mínimo do PLD regulatório.",
            "patamar": "Patamar de carga horária (Carga Pesada, Média ou Leve).",
            "data_apuracao": "Timestamp da hora de apuração do PLD horário.",
            "pld_medio_nacional_rs_mwh": "Média aritmética do PLD entre os quatro submercados interligados no SIN.",
            "spread_maximo_regional_rs_mwh": "Maior descolamento de preço verificado entre dois submercados (Max(PLD) - Min(PLD)).",
            "status_integracao_sin": "Indicador de transmissão: 'Equilíbrio Inter-regional' ou 'Alerta: Descolamento Estrutural entre Submercados'.",
            "diferenca_vs_media_nacional": "Desvio do PLD do submercado em relação à média nacional (R$/MWh)."
        },
        "golden_queries": [
            {
                "title": "Último PLD por Submercado e Spread Máximo Regional",
                "sql": (
                    "SELECT subsistema, pld_rs_mwh, pld_teto_rs_mwh, spread_maximo_regional_rs_mwh, status_integracao_sin "
                    "FROM `kpisetoreletrico.gold_kpis.kpi_ccee_mercado_resumo` "
                    "ORDER BY pld_rs_mwh DESC;"
                )
            }
        ]
    },

    "gold_kpis.kpi_ouvidoria_satisfacao": {
        "description": (
            "Consolidação de Ouvidoria, Reclamações de Nível 2 escaladas à ANEEL e Índice IASC de Satisfação do Consumidor. "
            "Mede o tempo médio de resolução de conflitos, índice de procedência das reclamações e conformidade de SLAs comerciais."
        ),
        "columns": {
            "distribuidora": "Sigla da concessionária avaliada.",
            "data_referencia": "Mês/ano de apuração dos indicadores de ouvidoria.",
            "score_iasc": "Pontuação oficial no Índice ANEEL de Satisfação do Consumidor (escala de 0 a 100 pontos).",
            "ranking_iasc": "Posição no ranking nacional de satisfação IASC.",
            "total_reclamacoes": "Volume total de reclamações protocoladas na Ouvidoria Setorial da ANEEL.",
            "procedencia_pct": "Percentual de reclamações julgadas procedentes a favor do consumidor.",
            "tempo_medio_resolucao_dias": "Prazo médio em dias corridos para resolução definitiva do chamado.",
            "cumprimento_sla_pct": "Percentual de reclamações resolvidas dentro do prazo regulatório estipulado.",
            "classificacao_satisfacao": "Classificação da distribuidora: Alta Satisfação (Excelente), Satisfação Moderada ou Baixa Satisfação."
        },
        "golden_queries": [
            {
                "title": "Top 5 Melhores Concessionárias no Índice IASC",
                "sql": (
                    "SELECT distribuidora, score_iasc, ranking_iasc, tempo_medio_resolucao_dias, classificacao_satisfacao "
                    "FROM `kpisetoreletrico.gold_kpis.kpi_ouvidoria_satisfacao` "
                    "WHERE score_iasc IS NOT NULL "
                    "ORDER BY score_iasc DESC LIMIT 5;"
                )
            }
        ]
    },

    "gold_kpis.kpi_transmissao_concessoes": {
        "description": (
            "Desempenho operacional e regulatório das concessões de transmissão de energia elétrica. "
            "Acompanha a Receita Anual Permitida (RAP homologada), a Parcela Variável por Indisponibilidade (PVd aplicada), "
            "o percentual de desconto sobre a receita (PVd/RAP) e o índice de disponibilidade da malha em quilômetros."
        ),
        "columns": {
            "concessionaria": "Nome empresarial da concessionária de transmissão (ex: TAESA, ISA_CTEEP, ELETROBRAS).",
            "sigla": "Sigla de mercado do transmissor.",
            "holding": "Grupo econômico controlador da concessionária.",
            "ano_ciclo": "Ano do ciclo tarifário regulatório da transmissão (ex: 2024/2025).",
            "rap_homologada_rs_mm": "Receita Anual Permitida homologada pela Resolução da ANEEL (R$ Milhões).",
            "pvd_rs_mm": "Parcela Variável por Indisponibilidade deduzida da receita devido a desligamentos de linhas e transformadores (R$ Milhões).",
            "pvd_sobre_rap_pct": "Percentual de perda de receita por indisponibilidade: (PVd / RAP) * 100.",
            "disponibilidade_pct": "Índice de disponibilidade física das Funções Transmissão (%) monitorado pelo ONS.",
            "ens_mwh": "Energia Não Suprida decorrente de perturbações na rede básica da transmissora (MWh).",
            "extensao_km": "Extensão total das linhas de transmissão sob concessão em quilômetros.",
            "status": "Classificação de eficiência da concessão.",
            "ranking_eficiencia": "Posição no ranking de menor penalidade PVd (1º = menor desconto proporcional de receita).",
            "data_referencia": "Mês de apuração dos indicadores da transmissão.",
            "data_processamento": "Timestamp de execução da carga na camada Gold."
        },
        "golden_queries": [
            {
                "title": "Transmissoras com Menor Taxa de Desconto de PVd sobre RAP",
                "sql": (
                    "SELECT sigla, holding, rap_homologada_rs_mm, pvd_rs_mm, pvd_sobre_rap_pct, disponibilidade_pct "
                    "FROM `kpisetoreletrico.gold_kpis.kpi_transmissao_concessoes` "
                    "ORDER BY pvd_sobre_rap_pct ASC LIMIT 5;"
                )
            }
        ]
    },

    "gold_kpis.kpi_atendimento_canais": {
        "description": (
            "Indicadores de atendimento telefônico e call center das distribuidoras conforme exigências da REN ANEEL 1.000/2021. "
            "Monitora o Índice de Nível de Serviço (INS - chamadas atendidas em até 30s), Índice de Abandono (IAb) e Tempo Médio de Atendimento (TMA)."
        ),
        "columns": {
            "distribuidora": "Código regulatório da distribuidora perante a ANEEL.",
            "nome_concessionaria": "Nome oficial da concessionária.",
            "ins_pct": "Índice de Nível de Serviço: percentual de chamadas telefônicas atendidas pelo operador humano em até 30 segundos (meta >= 85%).",
            "iab_pct": "Índice de Abandono: percentual de chamadas em espera que foram abandonadas pelo consumidor antes do atendimento (tolerância <= 2%).",
            "tma_s": "Tempo Médio de Atendimento em segundos durante o diálogo com o operador.",
            "chamadas_totais": "Volume consolidado de ligações recebidas no canal de call center no mês.",
            "status_ins": "Conformidade regulatória do INS ('Conforme' vs 'Não Conforme').",
            "status_iab": "Conformidade regulatória do índice de abandono.",
            "status_geral": "Status consolidado de excelência operacional nos canais de atendimento.",
            "data_referencia": "Mês de referência dos registros de teleatendimento.",
            "data_processamento": "Data de consolidação dos dados no BigQuery."
        }
    },

    "gold_kpis.kpi_atendimento_slas_comerciais": {
        "description": (
            "Cumprimento de prazos regulatórios e SLAs de serviços comerciais da Resolução Normativa ANEEL nº 1.000/2021. "
            "Acompanha solicitações de ligação nova, religação de emergência, vistorias e compensações financeiras pagas por atraso."
        ),
        "columns": {
            "servico": "Descrição do serviço comercial regulado (ex: Religação de Urgência, Ligação Nova Urbana, Troca de Titularidade).",
            "sigla_indicador": "Sigla padronizada pela ANEEL para o indicador comercial (ex: PRAZ_RELIG, PRAZ_LIG).",
            "artigo_ren_1000": "Artigo de fundamentação legal na Resolução Normativa ANEEL nº 1.000/2021.",
            "unidade_sla": "Unidade de contagem do prazo regulatório (Horas ou Dias Úteis).",
            "sla_regulatorio_valor": "Prazo máximo tolerado pela norma regulatória.",
            "tempo_medio_real": "Prazo médio efetivamente praticado pelas concessionárias para execução do serviço.",
            "cumprimento_pct": "Taxa percentual de solicitações atendidas estritamente dentro do prazo legal.",
            "total_solicitacoes": "Volume total de protocolos comerciais abertos pelos consumidores.",
            "solicitacoes_violadas": "Quantidade absoluta de pedidos executados com atraso ou ainda pendentes fora do prazo.",
            "compensacao_paga_rs_mm": "Montante total de crédito e indenizações financeiras creditadas aos clientes por violação de prazos regulatórios (R$ MM).",
            "status": "Conformidade do SLA: Conforme, Atenção ou Crítico.",
            "data_referencia": "Mês de apuração contábil dos serviços comerciais.",
            "data_processamento": "Timestamp de atualização do modelo Gold."
        }
    },

    "gold_kpis.kpi_sin_operacao_resumo": {
        "description": (
            "Visão consolidada da Operação do Sistema Interligado Nacional (SIN) com dados oficiais do ONS. "
            "Integra a Energia Armazenada (EAR %), Energia Natural Afluente (ENA % MLT), Custo Marginal de Operação (CMO) "
            "e despacho de usinas termelétricas fora da ordem de mérito por subsistema eletroenergético."
        ),
        "columns": {
            "subsistema": "Subsistema eletroenergético do SIN (SE_CO, SUL, NORDESTE, NORTE).",
            "data_referencia": "Data de apuração dos balanços e programações diárias/semanais de operação.",
            "ear_percentual": "Nível percentual de Energia Armazenada nos reservatórios hidrelétricos em relação à capacidade máxima do subsistema.",
            "ear_max_mwmes": "Capacidade máxima de armazenamento energético do subsistema expressa em Megawatts-mês (MWmês).",
            "ear_atual_mwmes": "Volume energético atualmente estocado nos reservatórios hidrelétricos (MWmês).",
            "meta_seguranca_percentual": "Meta de curva de segurança hídrica e armazenamento mínimo recomendada pelo ONS e CMSE.",
            "folga_seguranca_ear_pct": "Margem de segurança hídrica: (ear_percentual - meta_seguranca_percentual). Valores negativos indicam estresse hídrico.",
            "status_ear": "Classificação do reservatório: Confortável, Atenção ou Crítico.",
            "ena_mwmed": "Energia Natural Afluente prevista que flui para as calhas dos rios hidrelétricos, medida em MWmédios.",
            "ena_percentual_mlt": "Afluência hídrica expressa em percentual da Média de Longo Termo histórica (ENA % MLT).",
            "classificacao_ena": "Classificação hidrológica do período (Seca Severa, Seca Moderada, Normal, Úmido).",
            "cmo_medio_rs_mwh": "Custo Marginal de Operação calculado pelo modelo DECOMP/DESSEM do ONS em Reais por MWh.",
            "despacho_termico_mw": "Montante de geração termelétrica a gás/óleo/carvão acionada por garantia de suprimento energético.",
            "status_seguranca_energetica": "Diagnóstico do subsistema: 'Condição Favorável / Segurança Energética', 'Alerta Crítico' ou 'Atenção'."
        }
    },

    "gold_kpis.kpi_financeiro_dre_empresas": {
        "description": (
            "Visão financeira executiva consolidada das empresas de capital aberto do setor elétrico brasileiro (CVM). "
            "Monitora Receita Líquida, EBITDA ajustado, Margem EBITDA, Lucro Líquido, Dívida Líquida, CAPEX e alavancagem financeira (Dívida Líquida / EBITDA)."
        ),
        "columns": {
            "empresa": "Razão social ou denominação comercial da holding ou transmissora/distribuidora.",
            "ticker": "Código de negociação das ações na B3 (ex: CPFE3, EGIE3, CMIG4, TAEE11).",
            "codigo_cvm": "Código oficial de registro da companhia aberta na CVM.",
            "cnpj": "CNPJ da empresa.",
            "segmento": "Segmento de atuação: Geração, Transmissão, Distribuição ou Integrada.",
            "ano_referencia": "Ano do exercício fiscal apurado.",
            "tipo_demonstrativo": "Tipo da demonstração: DFP Consolidado ou ITR.",
            "status_auditoria": "Parecer dos auditores independentes (Sem Ressalva, etc.).",
            "receita_liquida_rs_mm": "Receita operacional líquida anual ou trimestral (R$ Milhões).",
            "ebitda_rs_mm": "Lucro antes de Juros, Impostos, Depreciação e Amortização (R$ Milhões).",
            "margem_ebitda_pct": "Margem de rentabilidade operacional: (EBITDA / Receita Líquida) * 100.",
            "lucro_liquido_rs_mm": "Resultado líquido final do exercício (R$ Milhões).",
            "divida_liquida_rs_mm": "Endividamento financeiro bruto menos caixa e equivalentes (R$ Milhões).",
            "capex_rs_mm": "Investimentos de capital realizados em expansão e modernização da rede (R$ Milhões).",
            "alavancagem": "Múltiplo de endividamento financeiro: Dívida Líquida / EBITDA.",
            "data_processamento": "Timestamp de consolidação dos dados no BigQuery."
        },
        "golden_queries": [
            {
                "title": "Ranking de Rentabilidade Operacional (Margem EBITDA) no Setor Elétrico",
                "sql": (
                    "SELECT empresa, ticker, segmento, receita_liquida_rs_mm, ebitda_rs_mm, margem_ebitda_pct, alavancagem "
                    "FROM `kpisetoreletrico.gold_kpis.kpi_financeiro_dre_empresas` "
                    "WHERE ebitda_rs_mm > 0 "
                    "ORDER BY margem_ebitda_pct DESC;"
                )
            }
        ]
    },

    # --------------------------------------------------------------------------
    # ANEEL_SILVER
    # --------------------------------------------------------------------------
    "aneel_silver.dec_fec_distribuidoras": {
        "description": "Base tratada e padronizada de indicadores de continuidade coletiva (DEC e FEC) das distribuidoras da ANEEL (PRODIST Módulo 8).",
        "columns": {
            "data_referencia": "Mês de apuração do indicador de continuidade (DATE).",
            "distribuidora": "Código identificador da concessionária regulada pela ANEEL.",
            "nome_concessionaria": "Razão social da concessionária de energia.",
            "sigla_uf": "Estado principal da área de concessão.",
            "dec_apurado_horas": "Horas totais de interrupção por consumidor apuradas no período.",
            "dec_limite_aneel_horas": "Limite contratual regulatório de DEC.",
            "conformidade_dec": "Status booleano de conformidade do DEC.",
            "fec_apurado_vezes": "Quantidade de interrupções sofridas pelo consumidor no período.",
            "fec_limite_aneel_vezes": "Limite regulatório máximo de frequência de interrupção (FEC).",
            "conformidade_fec": "Status booleano de conformidade do FEC."
        }
    },

    "aneel_silver.mmgd_instalacoes": {
        "description": "Empreendimentos de micro e minigeração distribuída registrados no SISGD/ANEEL sob o marco legal da Lei 14.300/2022.",
        "columns": {
            "codigo_gd": "Código único de identificação do empreendimento de geração distribuída no SISGD.",
            "sigla_uf": "Unidade Federativa de conexão do sistema.",
            "municipio": "Município de instalação do gerador solar ou biomassa.",
            "subsistema": "Subsistema elétrico de atendimento.",
            "data_conexao": "Data formal de conexão do sistema à rede da distribuidora.",
            "potencia_instalada_kw": "Potência nominal do inversor/gerador em quilowatts (kW).",
            "modalidade": "Modalidade jurídica da GD: Autoconsumo Local, Remoto, Geração Compartilhada ou EMUC.",
            "fonte_energia": "Tecnologia de geração: Solar Fotovoltaica, Hidroelétrica (CGH), Biomassa ou Eólica.",
            "qtd_conexoes": "Quantidade de unidades consumidoras beneficiárias dos créditos de energia."
        }
    },

    "aneel_silver.tarifas_homologadas": {
        "description": "Série histórica de resoluções homologatórias de tarifas de distribuição de energia elétrica (PRORET).",
        "columns": {
            "distribuidora": "Sigla da distribuidora regulada.",
            "concessionaria": "Nome empresarial da concessionária.",
            "uf": "Estado da concessão.",
            "resolucao_homologatoria": "Número da resolução normativa ou homologatória ANEEL.",
            "data_vigencia": "Data de vigência do novo ciclo tarifário.",
            "tarifa_b1_rs_kwh": "Tarifa de energia para residencial (B1) em R$/kWh.",
            "tusd_rs_mwh": "Componente tarifária de remuneração da rede de distribuição (R$/MWh).",
            "te_rs_mwh": "Componente tarifária de compra de energia gerada (R$/MWh).",
            "wacc_regulatorio_pct": "Taxa de retorno do capital aprovada no ciclo de revisão.",
            "fator_x_pct": "Ganhos de eficiência capturados no processo tarifário."
        }
    },

    "aneel_silver.ouvidoria_reclamacoes": {
        "description": "Registros de ouvidoria setorial da ANEEL e pesquisas de satisfação residencial do IASC.",
        "columns": {
            "distribuidora": "Sigla da concessionária.",
            "data_referencia": "Mês de referência das reclamações.",
            "score_iasc": "Nota obtida no Índice ANEEL de Satisfação do Consumidor (0-100).",
            "ranking_iasc": "Posição no ranking nacional de satisfação.",
            "total_reclamacoes": "Total de reclamações recebidas no período.",
            "procedencia_pct": "Percentual de procedência em favor do consumidor.",
            "tempo_medio_resolucao_dias": "Média de dias para resposta e saneamento.",
            "cumprimento_sla_pct": "Taxa de cumprimento do prazo regulatório de resposta."
        }
    },

    "aneel_silver.desempenho_transmissao": {
        "description": "Indicadores regulatórios de desempenho das concessionárias de transmissão de energia (CKAN ANEEL).",
        "columns": {
            "concessionaria": "Razão social da transmissora.",
            "sigla": "Identificador de mercado da empresa transmissora.",
            "holding": "Grupo empresarial controlador.",
            "ano_ciclo": "Ciclo anual da receita da transmissão.",
            "rap_homologada_rs_mm": "Receita Anual Permitida em R$ Milhões.",
            "pvd_rs_mm": "Parcela Variável por Indisponibilidade descontada (R$ Milhões).",
            "pvd_sobre_rap_pct": "Relação percentual PVd/RAP.",
            "disponibilidade_pct": "Percentual de disponibilidade das instalações.",
            "ens_mwh": "Energia Não Suprida decorrente de eventos operacionais.",
            "extensao_km": "Malha total de linhas sob concessão (km).",
            "status": "Classificação de conformidade operacional.",
            "data_referencia": "Mês da apuração regulatória."
        }
    },

    "aneel_silver.qualidade_atendimento_comercial": {
        "description": "Indicadores de qualidade de atendimento telefônico e cumprimento dos prazos comerciais da REN ANEEL 1.000/2021.",
        "columns": {
            "distribuidora": "Código da distribuidora perante a ANEEL.",
            "nome_concessionaria": "Razão social da empresa de distribuição.",
            "ins_pct": "Índice de Nível de Serviço do atendimento telefônico (meta >= 85%).",
            "iab_pct": "Índice de abandono de chamadas no call center (tolerância <= 2%).",
            "tma_s": "Tempo Médio de Atendimento em segundos.",
            "chamadas_totais": "Total de chamadas registradas.",
            "servico": "Nome do serviço comercial avaliado.",
            "sigla_indicador": "Sigla técnica do indicador comercial.",
            "artigo_ren_1000": "Artigo da REN 1.000/2021 que estipula o padrão.",
            "unidade_sla": "Unidade do prazo legal (Horas ou Dias Úteis).",
            "sla_regulatorio_valor": "Valor nominal do limite legal de prazo.",
            "tempo_medio_real": "Tempo médio real medido para atendimento.",
            "cumprimento_pct": "Percentual de pedidos concluídos no prazo regulamentar.",
            "total_solicitacoes": "Volume de requisições de serviço.",
            "solicitacoes_violadas": "Volume de requisições atendidas com descumprimento de prazo.",
            "compensacao_paga_rs_mm": "Valor financeiro pago em compensações aos clientes (R$ Milhões).",
            "status": "Classificação do serviço.",
            "status_geral": "Diagnóstico geral de conformidade.",
            "data_referencia": "Mês da apuração."
        }
    },

    "aneel_silver.cvm_dre_empresas": {
        "description": "Demonstrações financeiras padronizadas (DFP e ITR) das empresas do setor elétrico arquivadas na CVM.",
        "columns": {
            "empresa": "Razão social da companhia aberta.",
            "ticker": "Código na B3.",
            "codigo_cvm": "Número do registro CVM.",
            "cnpj": "CNPJ cadastral.",
            "segmento": "Segmento setorial.",
            "receita_liquida_rs_mm": "Receita Líquida em R$ Milhões.",
            "ebitda_rs_mm": "EBITDA contábil em R$ Milhões.",
            "margem_ebitda_pct": "Margem EBITDA percentual.",
            "lucro_liquido_rs_mm": "Lucro Líquido em R$ Milhões.",
            "divida_liquida_rs_mm": "Dívida Líquida em R$ Milhões.",
            "capex_rs_mm": "Investimentos em R$ Milhões.",
            "alavancagem": "Índice Dívida Líquida / EBITDA.",
            "ano_referencia": "Ano do exercício social.",
            "tipo_demonstrativo": "Tipo contábil do demonstrativo.",
            "status_auditoria": "Auditoria externa.",
            "auditor": "Firma de auditoria independente."
        }
    },

    # --------------------------------------------------------------------------
    # MERCADO_CCEE
    # --------------------------------------------------------------------------
    "mercado_ccee.pld_horario": {
        "description": "Preço de Liquidação das Diferenças (PLD) divulgado oficialmente em granularidade horária pela CCEE.",
        "columns": {
            "data_hora": "Timestamp da hora de apuração do preço de liquidação das diferenças.",
            "subsistema": "Submercado de comercialização (SE_CO, SUL, NE, NORTE).",
            "pld_rs_mwh": "Valor oficial do PLD para o submercado em R$/MWh.",
            "pld_teto_rs_mwh": "Teto máximo regulatório do PLD no período.",
            "pld_piso_rs_mwh": "Piso mínimo regulatório do PLD.",
            "patamar": "Patamar de consumo (Pesada, Média, Leve)."
        }
    },

    "mercado_ccee.gsf_mensal": {
        "description": "Fator de Escala de Geração (GSF - Generation Scaling Factor) do Mecanismo de Realocação de Energia (MRE).",
        "columns": {
            "ano_mes": "Mês de apuração contábil da liquidação financeira do MRE.",
            "gsf_apurado": "Razão entre a geração hidrelétrica total do MRE e a Garantia Física consolidada.",
            "deficit_geracao_pct": "Déficit percentual de geração hídrica em relação à garantia física.",
            "status_risco_hidrologico": "Classificação do risco hidrológico para geradores hidrelétricos."
        }
    },

    "mercado_ccee.ess_encargos": {
        "description": "Encargos de Serviço do Sistema (ESS) decorrentes de segurança energética e restrições de transmissão.",
        "columns": {
            "ano_mes": "Mês de apuração da liquidação financeira da CCEE.",
            "motivo_encargo": "Razão do acionamento térmico: Restrição de Transmissão, Reserva de Potência ou Segurança Energética.",
            "valor_encargo_rs_mm": "Montante total faturado no mercado em R$ Milhões.",
            "impacto_unitario_rs_mwh": "Impacto médio rateado por Megawatt-hora de carga."
        }
    },

    "mercado_ccee.curtailment_renovaveis": {
        "description": "Histórico de cortes e restrições de despacho de usinas eólicas e solares fotovoltaicas pelo ONS.",
        "columns": {
            "data_referencia": "Data e turno da ocorrência do corte operativo de geração.",
            "subsistema": "Subsistema onde ocorreu o corte (comum no Nordeste e Norte).",
            "fonte": "Fonte afetada: Eólica ou Solar Fotovoltaica.",
            "energia_cortada_mwh": "Montante de energia elétrica limpa rejeitada na rede por restrição de transmissão (MWh).",
            "perda_financeira_estimada_rs_mm": "Estimativa de perda financeira associada ao corte de geração."
        }
    },

    "mercado_ccee.bandeiras_tarifarias": {
        "description": "Histórico de acionamento do Sistema de Bandeiras Tarifárias homologado pela ANEEL e CCEE.",
        "columns": {
            "mes_ano": "Mês/ano de referência de aplicação da bandeira tarifária.",
            "bandeira_acionada": "Bandeira vigente: Verde, Amarela, Vermelha Patamar 1, Vermelha Patamar 2 ou Escassez Hídrica.",
            "adicional_rs_kwh": "Custo adicional repassado à tarifa de consumo (R$/kWh).",
            "justificativa_ons_ccee": "Motivação técnico-energética para acionamento (CMO e GSF)."
        }
    },

    # --------------------------------------------------------------------------
    # OPERACAO_SIN
    # --------------------------------------------------------------------------
    "operacao_sin.ear_subsistemas": {
        "description": "Histórico diário e semanal de Energia Armazenada (EAR) nos reservatórios hidrelétricos do SIN (ONS).",
        "columns": {
            "data_referencia": "Data da apuração diária da EAR.",
            "subsistema": "Subsistema eletroenergético (SE_CO, SUL, NORDESTE, NORTE).",
            "ear_percentual": "Percentual de água estocada nos reservatórios sobre a capacidade máxima.",
            "ear_max_mwmes": "Energia máxima armazenável em MWmês.",
            "ear_atual_mwmes": "Energia atual armazenada em MWmês.",
            "meta_seguranca_percentual": "Curva guia mínima de segurança energética.",
            "status_criticidade": "Avaliação de criticidade hídrica."
        }
    },

    "operacao_sin.ena_historico": {
        "description": "Série histórica de Energia Natural Afluente (ENA) e afluências hídricas por subsistema (ONS).",
        "columns": {
            "data_referencia": "Data de consolidação das afluências.",
            "subsistema": "Subsistema eletroenergético.",
            "ena_mwmed": "Volume afluente em Megawatts médios.",
            "ena_percentual_mlt": "Afluência em relação à Média de Longo Termo histórica (% MLT).",
            "classificacao_hidrologica": "Classificação: Seca Severa, Moderada, Normal ou Úmido."
        }
    },

    "operacao_sin.cmo_horario_semanal": {
        "description": "Custo Marginal de Operação (CMO) calculado pelos modelos computacionais do ONS.",
        "columns": {
            "data_referencia": "Semana operativa ou hora de apuração do CMO.",
            "patamar_carga": "Patamar de carga: Leve, Média ou Pesada.",
            "subsistema": "Subsistema do SIN.",
            "cmo_rs_mwh": "Custo marginal de suprimento em R$/MWh.",
            "despacho_termico_mw": "Potência térmica acionada por restrição de rede ou segurança energética (MW)."
        }
    }
}

# ==============================================================================
# 3. CONCEITOS FORMAIS DE MÉTRICAS (METRICS CATALOG)
# ==============================================================================

METRICS_CATALOG = {
    "dec_qualidade_fornecimento": {
        "name": "Duração Equivalente de Interrupção por Unidade Consumidora (DEC)",
        "formula": "SUM(duracao_interrupcao_horas * consumidores_afetados) / total_consumidores_distribuidora",
        "unit": "Horas",
        "regulator": "ANEEL (PRODIST Módulo 8)",
        "description": "Mede o intervalo médio de tempo que, no período considerado, cada unidade consumidora atendida pela distribuidora ficou desprovida de fornecimento de energia elétrica."
    },
    "fec_frequencia_interrupcoes": {
        "name": "Frequência Equivalente de Interrupção por Unidade Consumidora (FEC)",
        "formula": "SUM(interrupcoes * consumidores_afetados) / total_consumidores_distribuidora",
        "unit": "Vezes",
        "regulator": "ANEEL (PRODIST Módulo 8)",
        "description": "Mede o número médio de vezes que, no período considerado, cada unidade consumidora atendida pela distribuidora sofreu descontinuidade no suprimento de energia."
    },
    "potencia_instalada_mmgd": {
        "name": "Capacidade Instalada de Micro e Minigeração Distribuída (MMGD)",
        "formula": "SUM(potencia_nominal_inversor_kw) / 1000.0",
        "unit": "Megawatts (MW)",
        "regulator": "ANEEL (Lei 14.300/2022 e REN 1.000/2021)",
        "description": "Soma da potência instalada dos sistemas de microgeração (<= 75 kW) e minigeração (> 75 kW até 5 MW) conectados à rede de distribuição."
    },
    "pld_preco_liquidacao_diferencas": {
        "name": "Preço de Liquidação das Diferenças (PLD)",
        "formula": "Valor horário calculado pelo modelo DESSEM para valoração das diferenças de energia no MCP",
        "unit": "R$/MWh",
        "regulator": "CCEE e ANEEL",
        "description": "Preço horário utilizado para liquidar financeiramente a energia elétrica negociada no mercado de curto prazo da CCEE que diverge dos contratos bilaterais."
    },
    "iasc_satisfacao_consumidor": {
        "name": "Índice ANEEL de Satisfação do Consumidor (IASC)",
        "formula": "Índice ponderado das dimensões: Qualidade Percebida, Valor Percebido, Confiança, Fidelidade e Satisfação Global",
        "unit": "Pontos (0 a 100)",
        "regulator": "ANEEL",
        "description": "Indicador oficial da ANEEL obtido por pesquisa de opinião pública anual com consumidores residenciais para aferição da qualidade percebida dos serviços da distribuidora."
    },
    "pvd_parcela_variavel_transmissao": {
        "name": "Parcela Variável por Indisponibilidade (PVd)",
        "formula": "Dedução monetária calculada sobre a RAP contratada por eventos de indisponibilidade de equipamentos de transmissão",
        "unit": "R$ Milhões",
        "regulator": "ANEEL (Resoluções de Homologação da RAP)",
        "description": "Penalidade regulatória que reduz a remuneração mensal das transmissoras em função de desligamentos intempestivos ou programados na rede básica."
    },
    "alavancagem_financeira": {
        "name": "Alavancagem Financeira Setorial (Dívida Líquida / EBITDA)",
        "formula": "divida_liquida_rs_mm / NULLIF(ebitda_rs_mm, 0)",
        "unit": "Múltiplo (x)",
        "regulator": "CVM",
        "description": "Indicador de solvência que mensura em quantos anos de geração de caixa operacional a empresa liquidaria sua dívida líquida total."
    },
    "cmo_custo_marginal_operacao": {
        "name": "Custo Marginal de Operação (CMO)",
        "formula": "Custo derivado da função de valor da água pelos modelos computacionais do ONS (NEWAVE/DECOMP)",
        "unit": "R$/MWh",
        "regulator": "ONS",
        "description": "Custo por unidade de energia para atender um acréscimo de demanda no sistema elétrico mantendo os níveis de confiabilidade."
    }
}
