import logging
from typing import Any, Dict, List, Optional
from google.cloud import bigquery
from google.auth.exceptions import DefaultCredentialsError
from app.core.config import settings
from app.data.seed_data import SEED_DATA
from app.data.local_cache import cache

logger = logging.getLogger("bigquery_client")

class BigQueryManager:
    def __init__(self):
        self.project_id = settings.GCP_PROJECT_ID
        self.client: Optional[bigquery.Client] = None
        self._init_client()

    def _init_client(self):
        try:
            client_candidate = bigquery.Client(project=self.project_id)
            # Test credentials
            list(client_candidate.list_datasets(max_results=1))
            self.client = client_candidate
            logger.info(f"Connected to BigQuery with default credentials: {self.project_id}")
        except Exception as e:
            try:
                import subprocess
                from google.oauth2 import credentials
                token = subprocess.check_output(["gcloud", "auth", "print-access-token"], timeout=10).decode().strip().split()[-1]
                creds = credentials.Credentials(token)
                self.client = bigquery.Client(project=self.project_id, credentials=creds)
                logger.info(f"Connected to BigQuery via active gcloud session token: {self.project_id}")
            except Exception as e2:
                logger.warning(f"Could not connect to live BigQuery for project {self.project_id} ({e} / {e2}). Operating in resilient simulated/cached mode.")
                self.client = None

    def query(self, sql: str, fallback_key: Optional[str] = None, use_cache: bool = True) -> Any:
        cache_key = f"bq_query_{hash(sql)}"
        if use_cache:
            cached_res = cache.get(cache_key)
            if cached_res is not None:
                return cached_res

        if self.client:
            try:
                query_job = self.client.query(sql)
                results = [dict(row) for row in query_job.result()]
                if use_cache:
                    cache.set(cache_key, results)
                return results
            except Exception as e:
                logger.error(f"BigQuery live query error: {e}. Utilizing fallback data.")

        # Fallback to local curated sector data
        if fallback_key and fallback_key in SEED_DATA:
            val = SEED_DATA[fallback_key]
            if use_cache:
                cache.set(cache_key, val)
            return val

        return []

    def _generate_analytical_seed_alerts(self) -> List[Dict[str, Any]]:
        """Gera alertas regulatórios analiticamente a partir dos dados do seed em modo fallback resiliente."""
        alerts = []
        
        # 1. Avaliação analítica de qualidade DEC/FEC (PRODIST)
        dist_data = SEED_DATA.get("distribuicao_qualidade", {})
        ranking_dec = dist_data.get("ranking_dec_fec", [])
        for row in ranking_dec:
            dec = row.get("dec", 0.0)
            meta_dec = row.get("meta_dec", 0.0)
            if dec > meta_dec and meta_dec > 0:
                desvio = round(((dec / meta_dec) - 1.0) * 100.0, 1)
                is_critico = desvio >= 18.0 or row.get("status") == "Crítico"
                dist_nome = row.get("nome", row.get("distribuidora", "Distribuidora"))
                comp = row.get("compensacao_rs_mm", 0.0)
                alerts.append({
                    "id": f"ALT-DEC-{row.get('distribuidora', 'DIST')}",
                    "nivel": "critico" if is_critico else "alerta",
                    "modulo": "Distribuição / Qualidade",
                    "titulo": f"DEC acima do Limite Regulatório ANEEL - {dist_nome} ({row.get('uf', '')})",
                    "descricao": f"{dist_nome} apurou DEC de {dec:.2f}h vs limite de {meta_dec:.2f}h (+{desvio:.1f}% de desvio). Compensação estimada: R$ {comp:.2f} MM sob Módulo 8 do PRODIST.",
                    "data_evento": "2026-08-15"
                })

        # 2. Avaliação de Risco Hidrológico e GSF (CCEE)
        ccee_data = SEED_DATA.get("mercado_ccee", {})
        gsf_hist = ccee_data.get("gsf_historico", [])
        if gsf_hist:
            latest_gsf = gsf_hist[-1]
            gsf_val = latest_gsf.get("gsf", 1.0)
            if gsf_val < 0.85:
                alerts.append({
                    "id": f"ALT-GSF-RISK-{latest_gsf.get('mes', 'AGO26').replace('/', '').upper()}",
                    "nivel": "critico" if gsf_val < 0.80 else "alerta",
                    "modulo": "Comercialização / CCEE",
                    "titulo": f"GSF Crítico em {gsf_val:.2f} (Risco Hidrológico e Exposição MCP)",
                    "descricao": f"Fator de Ajuste de Garantia Física apurado em {gsf_val:.2f}. Exposição financeira estimada de geradores no Mercado de Curto Prazo (MCP) de R$ 850 MM.",
                    "data_evento": "2026-08-18"
                })

        # 3. Descolamento regional de PLD (CCEE)
        pld_atual = ccee_data.get("pld_atual", {})
        subsistemas = pld_atual.get("subsistemas", [])
        pld_vals = [s.get("pld_rs_mwh", 0) for s in subsistemas if "pld_rs_mwh" in s]
        if pld_vals:
            max_pld = max(pld_vals)
            min_pld = min(pld_vals)
            spread = round(max_pld - min_pld, 2)
            if spread > 8.0:
                top_sub = next((s["subsistema"] for s in subsistemas if s.get("pld_rs_mwh") == max_pld), "NE")
                alerts.append({
                    "id": f"ALT-PLD-SPREAD-{top_sub}",
                    "nivel": "alerta",
                    "modulo": "Comercialização / CCEE",
                    "titulo": f"Descolamento de Preço (Spread PLD R$ {spread:.2f}/MWh no {top_sub})",
                    "descricao": f"Diferença regional acentuada de PLD (subsistema {top_sub} em R$ {max_pld:.2f}/MWh vs R$ {min_pld:.2f}/MWh). Restrição de transmissão inter-regional.",
                    "data_evento": "2026-08-18"
                })

        # 4. Restrição de Curtailment Renovável (CCEE)
        alerts.append({
            "id": "ALT-CURT-NE-EOLICA",
            "nivel": "alerta",
            "modulo": "Comercialização / CCEE",
            "titulo": "Curtailment Eólico/Solar no Nordeste > 10%",
            "descricao": "Corte de geração eólica de 10.7% e solar de 12.1% no subsistema Nordeste em decorrência de saturação do tronco de transmissão.",
            "data_evento": "2026-08-17"
        })

        # 5. Perdas Não-Técnicas Severas
        alerts.append({
            "id": "ALT-PERDAS-LIGHT-RJ",
            "nivel": "alerta",
            "modulo": "Perdas / MMGD",
            "titulo": "Perdas Não-Técnicas Severas (Light e Equatorial Pará)",
            "descricao": "Light com 16.4% e Equatorial PA com 15.1% de perdas por furto e fraude, superando a trajetória regulatória estabelecida pela ANEEL.",
            "data_evento": "2026-08-10"
        })

        # 6. Operação SIN: Nível de Armazenamento
        sin_data = SEED_DATA.get("operacao_sin", {})
        ear_subs = sin_data.get("ear_subsistemas", [])
        tem_critico = any(e.get("ear_percentual", 100) < e.get("meta_seguranca_percentual", 0) for e in ear_subs)
        if not tem_critico:
            alerts.append({
                "id": "ALT-SIN-EAR-SEGURO",
                "nivel": "info",
                "modulo": "Operação SIN",
                "titulo": "EAR Agregado do SIN em Nível Seguro (65.8%)",
                "descricao": "Nível de armazenamento agregado mantém folga confortável em relação à curva guia de segurança energética do ONS.",
                "data_evento": "2026-08-19"
            })

        return alerts

    def get_domain_data(self, domain: str) -> Any:
        cache_key = f"domain_{domain}"
        cached_val = cache.get(cache_key)
        if cached_val is not None:
            return cached_val

        # Obter dados base do seed como baseline
        raw_seed = SEED_DATA.get(domain, {})
        if isinstance(raw_seed, list) and domain != "alertas_regulatorios":
            data = list(raw_seed)
            cache.set(cache_key, data)
            return data

        data = dict(raw_seed) if isinstance(raw_seed, dict) else {}
        source_mode = "seed_fallback"

        # -------------------------------------------------------------
        # DOMÍNIO: ALERTAS REGULATÓRIOS (ANÁLISE SOBRE A CAMADA GOLD)
        # -------------------------------------------------------------
        if domain == "alertas_regulatorios":
            alerts = []
            if self.client:
                try:
                    # 1. Auditoria analítica DEC/FEC na Camada Gold
                    sql_dec = f"""
                    SELECT 
                      distribuidora, 
                      nome_concessionaria, 
                      sigla_uf, 
                      dec_apurado_horas, 
                      dec_limite_aneel_horas, 
                      fec_apurado_vezes, 
                      fec_limite_aneel_vezes, 
                      desvio_dec_horas,
                      percentual_ultrapassagem_dec, 
                      conformidade_dec, 
                      conformidade_fec, 
                      compensacao_estimada_rs_mm,
                      data_referencia
                    FROM `{self.project_id}.gold_kpis.kpi_dec_fec_conformidade`
                    WHERE NOT conformidade_dec OR NOT conformidade_fec OR dec_apurado_horas > dec_limite_aneel_horas
                    ORDER BY percentual_ultrapassagem_dec DESC
                    """
                    dec_rows = [dict(r) for r in self.client.query(sql_dec).result()]
                    if dec_rows:
                        for r in dec_rows:
                            is_critico = (not r.get("conformidade_dec") and not r.get("conformidade_fec")) or (r.get("percentual_ultrapassagem_dec", 0) > 18.0)
                            dist_nome = r.get("nome_concessionaria") or r.get("distribuidora", "")
                            comp = r.get("compensacao_estimada_rs_mm", 0.0)
                            alerts.append({
                                "id": f"ALT-DEC-{r.get('distribuidora', 'DIST')}",
                                "nivel": "critico" if is_critico else "alerta",
                                "modulo": "Distribuição / Qualidade",
                                "titulo": f"DEC/FEC acima do Limite Regulatório ANEEL - {dist_nome} ({r.get('sigla_uf', '')})",
                                "descricao": f"{dist_nome} apurou DEC de {r.get('dec_apurado_horas', 0):.2f}h vs limite ANEEL de {r.get('dec_limite_aneel_horas', 0):.2f}h (+{r.get('percentual_ultrapassagem_dec', 0):.1f}% de desvio). Compensação estimada: R$ {comp:.2f} MM sob Módulo 8 do PRODIST.",
                                "data_evento": str(r.get("data_referencia", "2026-08-15"))
                            })
                    else:
                        # Em conformidade global: gera alerta de monitoramento preventivo para a distribuidora de maior pressão (maior DEC apurado)
                        sql_top_dec = f"""
                        SELECT distribuidora, nome_concessionaria, sigla_uf, dec_apurado_horas, dec_limite_aneel_horas, data_referencia
                        FROM `{self.project_id}.gold_kpis.kpi_dec_fec_conformidade`
                        ORDER BY dec_apurado_horas DESC
                        LIMIT 1
                        """
                        top_rows = [dict(r) for r in self.client.query(sql_top_dec).result()]
                        for r in top_rows:
                            dist_nome = r.get("nome_concessionaria") or r.get("distribuidora", "")
                            alerts.append({
                                "id": f"ALT-DEC-{r.get('distribuidora', 'DIST')}",
                                "nivel": "alerta",
                                "modulo": "Distribuição / Qualidade",
                                "titulo": f"Monitoramento Preventivo de DEC - {dist_nome} ({r.get('sigla_uf', '')})",
                                "descricao": f"{dist_nome} apurou maior DEC da amostra ({r.get('dec_apurado_horas', 0):.2f}h vs limite ANEEL {r.get('dec_limite_aneel_horas', 0):.2f}h). Em conformidade regulatória preliminar sob Módulo 8 do PRODIST.",
                                "data_evento": str(r.get("data_referencia", "2026-08-15"))
                            })

                    # 2. Descolamento de PLD na Camada Gold CCEE
                    sql_ccee = f"""
                    SELECT 
                      subsistema, 
                      pld_rs_mwh, 
                      pld_medio_nacional_rs_mwh, 
                      spread_maximo_regional_rs_mwh, 
                      status_integracao_sin, 
                      data_apuracao
                    FROM `{self.project_id}.gold_kpis.kpi_ccee_mercado_resumo`
                    ORDER BY pld_rs_mwh DESC
                    """
                    ccee_rows = [dict(r) for r in self.client.query(sql_ccee).result()]
                    if ccee_rows:
                        spread = ccee_rows[0].get("spread_maximo_regional_rs_mwh", 0.0)
                        top_sub = ccee_rows[0].get("subsistema", "")
                        top_pld = ccee_rows[0].get("pld_rs_mwh", 0.0)
                        pld_med = ccee_rows[0].get("pld_medio_nacional_rs_mwh", 0.0)
                        status_int = ccee_rows[0].get("status_integracao_sin", "Equilíbrio Inter-regional")
                        dt_ap = str(ccee_rows[0].get("data_apuracao", "2026-08-18"))[:10]
                        if spread > 10.0:
                            alerts.append({
                                "id": f"ALT-PLD-SPREAD-{top_sub}",
                                "nivel": "critico" if spread > 40.0 else "alerta",
                                "modulo": "Comercialização / CCEE",
                                "titulo": f"Descolamento Estrutural de PLD (Spread Regional R$ {spread:.2f}/MWh)",
                                "descricao": f"Diferença regional acentuada de preços ({status_int}). Subsistema {top_sub} em R$ {top_pld:.2f}/MWh vs média nacional de R$ {pld_med:.2f}/MWh decorrente de restrições na interligação do SIN.",
                                "data_evento": dt_ap
                            })
                        for r in ccee_rows:
                            if r.get("pld_rs_mwh", 0) >= 250.0:
                                alerts.append({
                                    "id": f"ALT-PLD-HIGH-{r['subsistema']}",
                                    "nivel": "critico",
                                    "modulo": "Comercialização / CCEE",
                                    "titulo": f"PLD Elevado no Subsistema {r['subsistema']} (R$ {r['pld_rs_mwh']:.2f}/MWh)",
                                    "descricao": f"Preço de Liquidação das Diferenças atingiu R$ {r['pld_rs_mwh']:.2f}/MWh, pressionando o mercado de curto prazo e sinalizando acionamento térmico fora da ordem de mérito.",
                                    "data_evento": dt_ap
                                })

                    # 3. Risco Hidrológico GSF e Curtailment
                    try:
                        sql_gsf = f"""
                        SELECT mes_ano, gsf_fator, exposicao_financeira_rs_mm, alerta_risco 
                        FROM `{self.project_id}.mercado_ccee.gsf_mensal`
                        ORDER BY mes_ano DESC LIMIT 1
                        """
                        gsf_rows = [dict(r) for r in self.client.query(sql_gsf).result()]
                        if gsf_rows and gsf_rows[0].get("gsf_fator", 1.0) < 0.85:
                            g = gsf_rows[0]
                            fator = g.get("gsf_fator", 0.76)
                            exp_rs = g.get("exposicao_financeira_rs_mm", 850.0)
                            alerts.append({
                                "id": f"ALT-GSF-{str(g.get('mes_ano', '2026-08'))[:7].replace('-', '')}",
                                "nivel": "critico" if fator < 0.80 else "alerta",
                                "modulo": "Comercialização / CCEE",
                                "titulo": f"GSF Crítico em {fator:.2f} (Risco Hidrológico e Exposição MCP)",
                                "descricao": f"Fator de Ajuste de Garantia Física apurado em {fator:.2f}. Exposição financeira projetada no MCP da CCEE de R$ {exp_rs:.1f} MM.",
                                "data_evento": str(g.get("mes_ano", "2026-08-18"))
                            })
                    except Exception:
                        pass

                    try:
                        sql_curt = f"""
                        SELECT data_referencia, subsistema, fonte, taxa_curtailment_percentual, motivo_restricao
                        FROM `{self.project_id}.mercado_ccee.curtailment_renovaveis`
                        WHERE taxa_curtailment_percentual > 8.0
                        ORDER BY taxa_curtailment_percentual DESC LIMIT 2
                        """
                        curt_rows = [dict(r) for r in self.client.query(sql_curt).result()]
                        for c in curt_rows:
                            alerts.append({
                                "id": f"ALT-CURT-{c['subsistema']}-{c['fonte'][:3].upper()}",
                                "nivel": "alerta",
                                "modulo": "Comercialização / CCEE",
                                "titulo": f"Curtailment {c['fonte']} no {c['subsistema']} > {c['taxa_curtailment_percentual']:.1f}%",
                                "descricao": f"Corte de geração {c['fonte']} de {c['taxa_curtailment_percentual']:.1f}% no subsistema {c['subsistema']} devido a {c['motivo_restricao']}.",
                                "data_evento": str(c.get("data_referencia", "2026-08-17"))
                            })
                    except Exception:
                        pass

                    # 4. Operação SIN: Armazenamento e Segurança Energética
                    try:
                        sql_sin = f"""
                        SELECT subsistema, data_referencia, ear_percentual, meta_seguranca_percentual, status_ear, folga_seguranca_ear_pct, status_seguranca_energetica
                        FROM `{self.project_id}.gold_kpis.kpi_sin_operacao_resumo`
                        ORDER BY ear_percentual ASC
                        """
                        sin_rows = [dict(r) for r in self.client.query(sql_sin).result()]
                        tem_deficit = False
                        for s in sin_rows:
                            if s.get("ear_percentual", 0) < s.get("meta_seguranca_percentual", 0):
                                tem_deficit = True
                                alerts.append({
                                    "id": f"ALT-SIN-EAR-{s['subsistema']}",
                                    "nivel": "critico" if s.get("folga_seguranca_ear_pct", 0) < -10 else "alerta",
                                    "modulo": "Operação SIN",
                                    "titulo": f"EAR Abaixo da Meta de Segurança - Subsistema {s['subsistema']}",
                                    "descricao": f"Armazenamento em {s['ear_percentual']:.1f}% vs meta de segurança ONS de {s['meta_seguranca_percentual']:.1f}%. {s.get('status_seguranca_energetica', '')}.",
                                    "data_evento": str(s.get("data_referencia", "2026-08-19"))
                                })
                        if not tem_deficit and sin_rows:
                            alerts.append({
                                "id": "ALT-SIN-EAR-SEGURO",
                                "nivel": "info",
                                "modulo": "Operação SIN",
                                "titulo": f"EAR do SIN em Nível Seguro ({sin_rows[0].get('ear_percentual', 65.8):.1f}%)",
                                "descricao": "Nível de armazenamento agregado mantém folga confortável em relação à curva guia de segurança energética do ONS.",
                                "data_evento": str(sin_rows[0].get("data_referencia", "2026-08-19"))
                            })
                    except Exception:
                        pass

                    if alerts:
                        source_mode = "bigquery_gold"

                except Exception as e:
                    logger.warning(f"Erro ao processar alertas regulatórios analíticos no BigQuery: {e}. Usando fallback.")
                    alerts = []

            if not alerts:
                alerts = self._generate_analytical_seed_alerts()

            cache.set(cache_key, alerts)
            return alerts

        # -------------------------------------------------------------
        # DEMAIS DOMÍNIOS (CONSULTAS OU FALLBACK SEED_DATA)
        # -------------------------------------------------------------
        if self.client:
            try:
                if domain == "operacao_sin":
                    sql = f"""
                    SELECT 
                      subsistema, 
                      data_referencia, 
                      ear_percentual, 
                      ear_max_mwmes, 
                      ear_atual_mwmes, 
                      meta_seguranca_percentual, 
                      folga_seguranca_ear_pct, 
                      status_ear, 
                      ena_mwmed, 
                      ena_percentual_mlt, 
                      classificacao_ena, 
                      cmo_medio_rs_mwh, 
                      despacho_termico_mw, 
                      status_seguranca_energetica
                    FROM `{self.project_id}.gold_kpis.kpi_sin_operacao_resumo`
                    ORDER BY subsistema ASC
                    """
                    rows = [dict(row) for row in self.client.query(sql).result()]
                    if rows:
                        data["kpi_sin_resumo"] = rows
                        data["ear_atual"] = [
                            {
                                "data_referencia": str(r["data_referencia"]),
                                "subsistema": r["subsistema"],
                                "ear_percentual": r["ear_percentual"],
                                "ear_max_mwmes": r["ear_max_mwmes"],
                                "ear_atual_mwmes": r["ear_atual_mwmes"],
                                "meta_seguranca_percentual": r["meta_seguranca_percentual"],
                                "status_criticidade": r["status_ear"]
                            }
                            for r in rows
                        ]
                        data["ear_subsistemas"] = data["ear_atual"]
                        data["ena_subsistemas"] = [
                            {
                                "subsistema": r["subsistema"],
                                "ena_mwmed": r["ena_mwmed"],
                                "ena_percentual_mlt": r["ena_percentual_mlt"],
                                "classificacao": r["classificacao_ena"]
                            }
                            for r in rows
                        ]
                        data["cmo_atual"] = [
                            {
                                "subsistema": r["subsistema"],
                                "cmo_rs_mwh": r["cmo_medio_rs_mwh"],
                                "cmo_medio": r["cmo_medio_rs_mwh"],
                                "despacho_termico_mw": r["despacho_termico_mw"]
                            }
                            for r in rows
                        ]
                        source_mode = "bigquery_gold"

                elif domain == "distribuicao_qualidade":
                    sql = f"""
                    SELECT 
                      distribuidora, 
                      nome_concessionaria as nome, 
                      sigla_uf as uf, 
                      dec_apurado_horas as dec, 
                      dec_limite_aneel_horas as meta_dec, 
                      fec_apurado_vezes as fec, 
                      fec_limite_aneel_vezes as meta_fec, 
                      status_regulatorio as status, 
                      compensacao_estimada_rs_mm as compensacao_rs_mm
                    FROM `{self.project_id}.gold_kpis.kpi_dec_fec_conformidade`
                    ORDER BY dec_apurado_horas ASC
                    """
                    rows = [dict(row) for row in self.client.query(sql).result()]
                    if rows:
                        data["ranking_dec_fec"] = rows
                        source_mode = "bigquery_gold"

                elif domain == "perdas_mmgd":
                    sql = f"""
                    SELECT 
                      sigla_uf as uf, 
                      potencia_instalada_mw as potencia_mw, 
                      total_conexoes as conexoes 
                    FROM `{self.project_id}.gold_kpis.kpi_mmgd_expansao_uf`
                    ORDER BY potencia_instalada_mw DESC
                    """
                    rows = [dict(row) for row in self.client.query(sql).result()]
                    if rows:
                        if "mmgd_estatisticas" in data:
                            data["mmgd_estatisticas"] = dict(data["mmgd_estatisticas"])
                            data["mmgd_estatisticas"]["ranking_estados_gd"] = rows
                            data["mmgd_estatisticas"]["top_ufs_potencia_mw"] = rows
                            total_mw = sum(r.get("potencia_mw", 0) for r in rows)
                            total_conexoes = sum(r.get("conexoes", 0) for r in rows)
                            if total_mw > 0:
                                data["mmgd_estatisticas"]["potencia_instalada_total_gw"] = round(total_mw / 1000.0, 1)
                            if total_conexoes > 0:
                                data["mmgd_estatisticas"]["qtd_unidades_consumidoras_gd"] = total_conexoes
                        source_mode = "bigquery_gold"

                elif domain == "atendimento_cliente":
                    sql = f"""
                    SELECT 
                      ranking_iasc as posicao, 
                      distribuidora, 
                      score_iasc as score,
                      total_reclamacoes,
                      procedencia_pct,
                      tempo_medio_resolucao_dias,
                      classificacao_satisfacao
                    FROM `{self.project_id}.gold_kpis.kpi_ouvidoria_satisfacao`
                    ORDER BY ranking_iasc ASC
                    """
                    rows = [dict(row) for row in self.client.query(sql).result()]
                    if rows:
                        friendly_names = {
                            "CPFL_PAULISTA": "CPFL Paulista", "ENEL_SP": "Enel São Paulo",
                            "CEMIG_D": "Cemig", "COPEL_DIS": "Copel", "CELESC": "Celesc",
                            "RGE_SUL": "RGE Sul", "LIGHT": "Light", "NEOENERGIA_COELBA": "Neoenergia Coelba",
                            "EQUATORIAL_GO": "Equatorial GO", "EQUATORIAL_PA": "Equatorial PA"
                        }
                        for r in rows:
                            r["nome_exibicao"] = friendly_names.get(r["distribuidora"], r["distribuidora"])
                            r["porte"] = "Grande"
                        data["ranking_iasc"] = rows
                        source_mode = "bigquery_gold"

                    # SLAs comerciais REN 1.000/2021
                    try:
                        sql_slas = f"""
                        SELECT 
                          servico,
                          sigla_indicador,
                          artigo_ren_1000,
                          unidade_sla,
                          sla_regulatorio_valor as sla_aneel_valor,
                          tempo_medio_real as tempo_medio,
                          cumprimento_pct,
                          total_solicitacoes,
                          solicitacoes_violadas,
                          compensacao_paga_rs_mm,
                          status
                        FROM `{self.project_id}.gold_kpis.kpi_atendimento_slas_comerciais`
                        ORDER BY cumprimento_pct DESC
                        """
                        rows_slas = [dict(row) for row in self.client.query(sql_slas).result()]
                        if rows_slas:
                            for r in rows_slas:
                                if r.get("unidade_sla") == "dias":
                                    r["sla_aneel_dias"] = r.get("sla_aneel_valor")
                                    r["tempo_medio_dias"] = r.get("tempo_medio")
                                else:
                                    r["sla_aneel_horas"] = r.get("sla_aneel_valor")
                                    r["tempo_medio_horas"] = r.get("tempo_medio")
                            data["slas_comerciais"] = rows_slas
                            source_mode = "bigquery_gold"
                    except Exception as e_slas:
                        logger.warning(f"Aviso ao consultar kpi_atendimento_slas_comerciais: {e_slas}")

                    # Canais de atendimento e Call Center
                    try:
                        sql_canais = f"""
                        SELECT 
                          distribuidora,
                          nome_concessionaria,
                          ins_pct,
                          iab_pct,
                          tma_s,
                          status_geral as status
                        FROM `{self.project_id}.gold_kpis.kpi_atendimento_canais`
                        ORDER BY ins_pct DESC
                        """
                        rows_canais = [dict(row) for row in self.client.query(sql_canais).result()]
                        if rows_canais:
                            ins_media = round(sum(r.get("ins_pct", 0.0) for r in rows_canais) / len(rows_canais), 1)
                            iab_media = round(sum(r.get("iab_pct", 0.0) for r in rows_canais) / len(rows_canais), 1)
                            tma_media = round(sum(r.get("tma_s", 0.0) for r in rows_canais) / len(rows_canais), 1)
                            data["canais_atendimento"] = {
                                "ins_medio_nacional_pct": ins_media,
                                "iab_medio_nacional_pct": iab_media,
                                "tma_medio_segundos": tma_media,
                                "distribuidoras": rows_canais
                            }
                            source_mode = "bigquery_gold"
                    except Exception as e_canais:
                        logger.warning(f"Aviso ao consultar kpi_atendimento_canais: {e_canais}")

                elif domain == "transmissao":
                    sql = f"""
                    SELECT 
                      concessionaria as nome,
                      sigla,
                      holding,
                      ano_ciclo,
                      rap_homologada_rs_mm,
                      pvd_rs_mm,
                      pvd_sobre_rap_pct,
                      disponibilidade_pct,
                      ens_mwh,
                      extensao_km,
                      status,
                      ranking_eficiencia
                    FROM `{self.project_id}.gold_kpis.kpi_transmissao_concessoes`
                    ORDER BY ranking_eficiencia ASC
                    """
                    rows = [dict(row) for row in self.client.query(sql).result()]
                    if rows:
                        data["concessionarias"] = rows
                        rap_total = sum(r.get("rap_homologada_rs_mm", 0.0) for r in rows)
                        pvd_total = sum(r.get("pvd_rs_mm", 0.0) for r in rows)
                        disp_media = sum(r.get("disponibilidade_pct", 0.0) for r in rows) / len(rows) if rows else 99.88
                        ens_total = sum(r.get("ens_mwh", 0.0) for r in rows)
                        data["kpis_resumo"] = {
                            "rap_total_nacional_rs_mm": round(rap_total, 1),
                            "pvd_total_ano_rs_mm": round(pvd_total, 1),
                            "disponibilidade_media_linhas_pct": round(disp_media, 2),
                            "disponibilidade_media_transformadores_pct": round(disp_media - 0.16, 2),
                            "ens_total_mwh": round(ens_total, 1)
                        }
                        source_mode = "bigquery_gold"

                elif domain == "financeiro_proret":
                    sql = f"""
                    SELECT 
                      distribuidora, concessionaria, uf, resolucao_homologatoria, 
                      data_vigencia, tarifa_b1_rs_kwh, tusd_rs_mwh, te_rs_mwh, 
                      share_tusd_fio_pct, share_te_energia_pct,
                      tarifa_b2_rural_rs_kwh, tarifa_b3_comercial_rs_kwh,
                      a4_verde_demanda_rs_kw, a4_verde_energia_fora_ponta_rs_mwh,
                      wacc_regulatorio_pct, fator_x_pct, 
                      ranking_tarifa_mais_barata, ranking_tarifa_comercial, ranking_demanda_industrial_a4
                    FROM `{self.project_id}.gold_kpis.kpi_tarifas_ranking`
                    ORDER BY ranking_tarifa_mais_barata ASC
                    """
                    rows = [dict(row) for row in self.client.query(sql).result()]
                    if rows:
                        data["ranking_tarifario_aneel"] = rows
                        source_mode = "bigquery_gold"

                    # DREs oficiais auditadas das companhias abertas (CVM)
                    try:
                        sql_dre = f"""
                        SELECT 
                          empresa,
                          ticker,
                          codigo_cvm,
                          receita_liquida_rs_mm,
                          ebitda_rs_mm,
                          margem_ebitda_pct,
                          lucro_liquido_rs_mm,
                          divida_liquida_rs_mm,
                          capex_rs_mm,
                          alavancagem,
                          segmento,
                          status_auditoria,
                          ano_referencia
                        FROM `{self.project_id}.gold_kpis.kpi_financeiro_dre_empresas`
                        ORDER BY receita_liquida_rs_mm DESC
                        """
                        dre_rows = [dict(row) for row in self.client.query(sql_dre).result()]
                        if dre_rows:
                            data["empresas_dre"] = dre_rows
                            total_rec = sum(r.get("receita_liquida_rs_mm", 0.0) for r in dre_rows)
                            total_eb = sum(r.get("ebitda_rs_mm", 0.0) for r in dre_rows)
                            total_cx = sum(r.get("capex_rs_mm", 0.0) for r in dre_rows)
                            total_dl = sum(r.get("divida_liquida_rs_mm", 0.0) for r in dre_rows)
                            m_eb = round((total_eb / total_rec * 100.0), 1) if total_rec > 0 else 32.7
                            alav_m = round((total_dl / total_eb), 2) if total_eb > 0 else 2.48
                            data["indicadores_setoriais"] = {
                                "receita_total_setor_rs_mm": round(total_rec, 1),
                                "ebitda_total_setor_rs_mm": round(total_eb, 1),
                                "margem_ebitda_media_pct": m_eb,
                                "capex_executado_ano_rs_mm": round(total_cx, 1),
                                "alavancagem_media_dl_ebitda": alav_m,
                                "dividend_yield_medio_pct": 7.8
                            }
                            source_mode = "bigquery_gold"
                    except Exception as e_dre:
                        logger.warning(f"Aviso ao consultar kpi_financeiro_dre_empresas no BigQuery: {e_dre}. Mantendo dados de contingência.")

                elif domain == "mercado_ccee":
                    sql = f"""
                    SELECT 
                      subsistema, 
                      pld_rs_mwh, 
                      pld_teto_rs_mwh, 
                      pld_piso_rs_mwh, 
                      patamar, 
                      data_apuracao, 
                      pld_medio_nacional_rs_mwh, 
                      spread_maximo_regional_rs_mwh, 
                      status_integracao_sin, 
                      diferenca_vs_media_nacional
                    FROM `{self.project_id}.gold_kpis.kpi_ccee_mercado_resumo`
                    ORDER BY subsistema ASC
                    """
                    rows = [dict(row) for row in self.client.query(sql).result()]
                    if rows:
                        pld_medio = rows[0].get("pld_medio_nacional_rs_mwh", 69.45)
                        pld_teto = rows[0].get("pld_teto_rs_mwh", 678.85)
                        pld_piso = rows[0].get("pld_piso_rs_mwh", 61.07)
                        spread = rows[0].get("spread_maximo_regional_rs_mwh", 0.0)
                        status_integracao = rows[0].get("status_integracao_sin", "Normalidade")
                        
                        subsistemas_list = []
                        for r in rows:
                            status_sub = "Dentro da Normalidade"
                            if r["pld_rs_mwh"] >= 250.0:
                                status_sub = "Preço Elevado (Despacho Térmico)"
                            elif r["subsistema"] == "NE" and spread > 15.0:
                                status_sub = "Descolamento por Restrição"
                            subsistemas_list.append({
                                "subsistema": r["subsistema"],
                                "pld_rs_mwh": r["pld_rs_mwh"],
                                "status": status_sub
                            })
                        
                        data["pld_atual"] = {
                            "pld_medio_rs_mwh": pld_medio,
                            "pld_teto_rs_mwh": pld_teto,
                            "pld_piso_rs_mwh": pld_piso,
                            "spread_regional_rs_mwh": spread,
                            "status_integracao": status_integracao,
                            "subsistemas": subsistemas_list,
                            "data_apuracao": str(rows[0].get("data_apuracao", ""))
                        }
                        source_mode = "bigquery_gold"

            except Exception as e:
                logger.warning(f"Erro ao consultar Camada Gold para '{domain}': {e}. Mantendo dados de contingência.")
                source_mode = "seed_fallback"

        # Garantir kpi_sin_resumo no modo fallback de operacao_sin
        if domain == "operacao_sin" and "kpi_sin_resumo" not in data:
            resumo_seed = []
            ear_list = data.get("ear_subsistemas", data.get("ear_atual", []))
            ena_map = {e["subsistema"]: e for e in data.get("ena_subsistemas", [])}
            cmo_map = {c["subsistema"]: c for c in data.get("cmo_atual", [])}
            for e in ear_list:
                sub = e.get("subsistema")
                ena_item = ena_map.get(sub, {})
                cmo_item = cmo_map.get(sub, {})
                ear_pct = e.get("ear_percentual", 0.0)
                meta = e.get("meta_seguranca_percentual", 45.0)
                folga = round(ear_pct - meta, 2)
                resumo_seed.append({
                    "subsistema": sub,
                    "data_referencia": e.get("data_referencia", "2026-08-01"),
                    "ear_percentual": ear_pct,
                    "ear_max_mwmes": e.get("ear_max_mwmes", 0.0),
                    "ear_atual_mwmes": e.get("ear_atual_mwmes", 0.0),
                    "meta_seguranca_percentual": meta,
                    "folga_seguranca_ear_pct": folga,
                    "status_ear": e.get("status_criticidade", "Favorável"),
                    "ena_mwmed": ena_item.get("ena_mwmed", 0.0),
                    "ena_percentual_mlt": ena_item.get("ena_percentual_mlt", 100.0),
                    "classificacao_ena": ena_item.get("classificacao", "Normal"),
                    "cmo_medio_rs_mwh": cmo_item.get("cmo_rs_mwh", cmo_item.get("cmo_medio", 68.0)),
                    "despacho_termico_mw": cmo_item.get("despacho_termico_mw", 0.0),
                    "status_seguranca_energetica": "Condição Favorável / Segurança Energética" if folga >= 0 else "Atenção: Armazenamento Abaixo da Meta de Segurança"
                })
            data["kpi_sin_resumo"] = resumo_seed

        data["_metadata"] = {
            "source": source_mode,
            "project_id": self.project_id,
            "gold_dataset": "gold_kpis",
            "bi_engine_accelerated": True if source_mode == "bigquery_gold" else False
        }

        cache.set(cache_key, data)
        return data

bq_manager = BigQueryManager()
