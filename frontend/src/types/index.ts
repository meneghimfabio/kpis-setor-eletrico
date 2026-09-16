export type SubsystemId = 'SE_CO' | 'S' | 'NE' | 'N' | 'SIN';

export interface SubsystemInfo {
  id: SubsystemId;
  name: string;
  uf_list: string[];
  peso_carga: number;
}

export interface ExecutiveSummary {
  kpis_destaque: {
    ear_sin_pct: { valor: number; meta: number; unidade: string; status: string; tendencia: string };
    cmo_medio_sin: { valor: number; unidade: string; status: string; tendencia: string };
    pld_medio: { valor: number; teto: number; piso: number; unidade: string; status: string };
    gsf_risco_hidro: { valor: number; alerta: string; unidade: string; status: string };
    rap_nacional: { valor: number; unidade: string; status: string };
    perdas_totais: { valor: number; meta: number; unidade: string; status: string };
    ebitda_setorial: { valor: number; unidade: string; status: string };
    bandeira_tarifaria: { valor: string; adicional: string; status: string };
  };
  matriz_sintese: Array<{
    categoria: string;
    cadeia: string[];
    owner: string;
    kpis: string;
    status: string;
    nivel: 'sucesso' | 'alerta' | 'critico';
  }>;
  subsistemas_resumo: SubsystemInfo[];
  alertas_recentes: AlertItem[];
}

export interface AlertItem {
  id: string;
  nivel: 'critico' | 'alerta' | 'info';
  modulo: string;
  titulo: string;
  descricao: string;
  data_evento: string;
}

export interface ProretInput {
  distribuidora: string;
  brr_liquida_rs_mm: number;
  wacc_regulatorio_pct: number;
  opex_eficiente_rs_mm: number;
  fator_x_pct: number;
  componente_q_pct: number;
  mercado_faturado_gwh: number;
  custos_parcela_a_rs_mm: number;
}

export interface ProretResult {
  remuneracao_capital_rs_mm: number;
  opex_eficiente_rs_mm: number;
  deducao_fator_x_rs_mm: number;
  ajuste_componente_q_rs_mm: number;
  parcela_b_rs_mm: number;
  parcela_a_rs_mm: number;
  receita_requerida_total_rs_mm: number;
  tarifa_media_rs_mwh: number;
  tarifa_media_rs_kwh: number;
  impacto_tarifa_percentual: number;
  analise_qualidade_dec_fec: string;
  detalhes_calculo: Record<string, any>;
}
