import React, { useState, useEffect } from 'react';
import type { ProretInput, ProretResult } from '../../types';
import { apiService } from '../../services/api';
import { Calculator, Info } from 'lucide-react';

function computeProretLocal(p: ProretInput): ProretResult {
  const selic = 13.75;
  const ipca = 4.22;
  const wacc_nominal = Number(((1.0 + p.wacc_regulatorio_pct / 100.0) * (1.0 + ipca / 100.0) - 1.0) * 100.0).toFixed(2);
  const remuneracao_capital = p.brr_liquida_rs_mm * (p.wacc_regulatorio_pct / 100.0);
  const opex = p.opex_eficiente_rs_mm;
  const fator_x = (p.fator_x_pct / 100.0) * opex;
  const comp_q = (p.componente_q_pct / 100.0) * opex;
  const parcela_b = remuneracao_capital + opex - fator_x - comp_q;
  const receita_requerida = p.custos_parcela_a_rs_mm + parcela_b;
  const mercado_mwh = p.mercado_faturado_gwh * 1000.0;
  const receita_rs = receita_requerida * 1_000_000.0;
  const tarifa_mwh = mercado_mwh > 0 ? receita_rs / mercado_mwh : 0;
  const tarifa_kwh = tarifa_mwh / 1000.0;
  const impacto = ((tarifa_mwh - 315.0) / 315.0) * 100.0;

  let analise_q = "Neutro: Indicadores de continuidade aderentes aos limites regulatórios.";
  if (p.componente_q_pct < 0) {
    analise_q = `Bônus de Qualidade: A distribuidora superou as metas de DEC/FEC da ANEEL, gerando benefício de R$ ${Math.abs(comp_q).toFixed(2)} MM.`;
  } else if (p.componente_q_pct > 0) {
    analise_q = `Penalidade de Qualidade: Desvios nos limites de interrupção (DEC/FEC) geraram redutor tarifário de R$ ${comp_q.toFixed(2)} MM.`;
  }

  return {
    remuneracao_capital_rs_mm: Number(remuneracao_capital.toFixed(2)),
    opex_eficiente_rs_mm: Number(opex.toFixed(2)),
    deducao_fator_x_rs_mm: Number(fator_x.toFixed(2)),
    ajuste_componente_q_rs_mm: Number(comp_q.toFixed(2)),
    parcela_b_rs_mm: Number(parcela_b.toFixed(2)),
    parcela_a_rs_mm: Number(p.custos_parcela_a_rs_mm.toFixed(2)),
    receita_requerida_total_rs_mm: Number(receita_requerida.toFixed(2)),
    tarifa_media_rs_mwh: Number(tarifa_mwh.toFixed(2)),
    tarifa_media_rs_kwh: Number(tarifa_kwh.toFixed(4)),
    impacto_tarifa_percentual: Number(impacto.toFixed(2)),
    analise_qualidade_dec_fec: analise_q,
    detalhes_calculo: {
      formula: "Receita Requerida = Parcela A + [ (BRR * WACC_Real) + OPEX - Fator_X - Comp_Q ]",
      wacc_real_pct: p.wacc_regulatorio_pct,
      wacc_nominal_estimado_pct: Number(wacc_nominal),
      taxa_selic_pct: selic,
      inflacao_ipca_12m_pct: ipca,
      macro_fonte: "Banco Central do Brasil (BCB SGS)"
    }
  };
}

export const ProretSimulator: React.FC = () => {
  const [params, setParams] = useState<ProretInput>({
    distribuidora: 'CPFL Paulista',
    brr_liquida_rs_mm: 14200.0,
    wacc_regulatorio_pct: 7.32,
    opex_eficiente_rs_mm: 2150.0,
    fator_x_pct: 0.85,
    componente_q_pct: -0.15,
    mercado_faturado_gwh: 28500.0,
    custos_parcela_a_rs_mm: 5800.0,
  });

  const [result, setResult] = useState<ProretResult>(() => computeProretLocal({
    distribuidora: 'CPFL Paulista',
    brr_liquida_rs_mm: 14200.0,
    wacc_regulatorio_pct: 7.32,
    opex_eficiente_rs_mm: 2150.0,
    fator_x_pct: 0.85,
    componente_q_pct: -0.15,
    mercado_faturado_gwh: 28500.0,
    custos_parcela_a_rs_mm: 5800.0,
  }));

  const calculate = async () => {
    try {
      const res = await apiService.simulateProret(params);
      if (res && res.receita_requerida_total_rs_mm) {
        setResult(res);
      } else {
        setResult(computeProretLocal(params));
      }
    } catch {
      // Fallback seguro imediato para manter simulador 100% responsivo
      setResult(computeProretLocal(params));
    }
  };

  useEffect(() => {
    calculate();
  }, [params]);

  const handleChange = (field: keyof ProretInput, val: number | string) => {
    setParams(prev => ({
      ...prev,
      [field]: typeof val === 'number' ? Number(val) : val
    }));
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200/80 p-6 shadow-sm">
      <div className="flex items-center justify-between mb-4 border-b border-slate-100 pb-3">
        <div className="flex items-center space-x-2">
          <div className="p-2 bg-blue-50 text-blue-700 rounded-lg">
            <Calculator className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-base font-bold text-slate-900">Simulador do Motor Regulatório (PRORET)</h3>
            <p className="text-xs text-slate-500">
              Equação da Revisão Tarifária: <code className="bg-slate-100 px-1 py-0.5 rounded font-semibold text-blue-700">[BRR × WACC] + [OPEX] - [Fator X] = Receita Requerida</code>
            </p>
          </div>
        </div>
        <button
          onClick={() => {
            setParams({
              distribuidora: 'CPFL Paulista',
              brr_liquida_rs_mm: 14200.0,
              wacc_regulatorio_pct: 7.32,
              opex_eficiente_rs_mm: 2150.0,
              fator_x_pct: 0.85,
              componente_q_pct: -0.15,
              mercado_faturado_gwh: 28500.0,
              custos_parcela_a_rs_mm: 5800.0,
            });
          }}
          className="text-xs font-semibold text-slate-500 hover:text-blue-600 underline"
        >
          Resetar Parâmetros
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        <div className="lg:col-span-7 space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Base de Remuneração (BRR)</span>
                <span className="text-blue-700">R$ {params.brr_liquida_rs_mm.toLocaleString()} MM</span>
              </div>
              <input
                type="range"
                min="5000"
                max="30000"
                step="250"
                value={params.brr_liquida_rs_mm}
                onChange={e => handleChange('brr_liquida_rs_mm', parseFloat(e.target.value))}
                className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <span className="text-[10px] text-slate-400">Ativos regulatórios líquidos (Submódulo 2.3)</span>
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>WACC Regulatório ANEEL</span>
                <span className="text-blue-700">{params.wacc_regulatorio_pct}%</span>
              </div>
              <input
                type="range"
                min="5.0"
                max="12.0"
                step="0.05"
                value={params.wacc_regulatorio_pct}
                onChange={e => handleChange('wacc_regulatorio_pct', parseFloat(e.target.value))}
                className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <span className="text-[10px] text-slate-400">Custo de capital real após impostos</span>
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>OPEX Eficiente (PMSO)</span>
                <span className="text-blue-700">R$ {params.opex_eficiente_rs_mm.toLocaleString()} MM</span>
              </div>
              <input
                type="range"
                min="500"
                max="6000"
                step="50"
                value={params.opex_eficiente_rs_mm}
                onChange={e => handleChange('opex_eficiente_rs_mm', parseFloat(e.target.value))}
                className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <span className="text-[10px] text-slate-400">Custos operacionais eficientes (Submódulo 2.2)</span>
            </div>

            <div>
              <div className="flex justify-between text-xs font-semibold text-slate-700 mb-1">
                <span>Fator X (Produtividade)</span>
                <span className="text-blue-700">{params.fator_x_pct}%</span>
              </div>
              <input
                type="range"
                min="0.0"
                max="3.0"
                step="0.05"
                value={params.fator_x_pct}
                onChange={e => handleChange('fator_x_pct', parseFloat(e.target.value))}
                className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <span className="text-[10px] text-slate-400">Redutor de ganhos de produtividade repassados</span>
            </div>

            <div className="md:col-span-2 bg-slate-50 p-3 rounded-lg border border-slate-200">
              <div className="flex justify-between text-xs font-semibold text-slate-800 mb-1">
                <span className="flex items-center">
                  Componente Q (Incentivo à Qualidade DEC/FEC)
                  <Info className="w-3.5 h-3.5 ml-1 text-slate-400 inline" />
                </span>
                <span className={`font-bold ${params.componente_q_pct < 0 ? 'text-emerald-700' : params.componente_q_pct > 0 ? 'text-rose-700' : 'text-slate-700'}`}>
                  {params.componente_q_pct > 0 ? `+${params.componente_q_pct}% (Penalidade)` : `${params.componente_q_pct}% (Bônus)`}
                </span>
              </div>
              <input
                type="range"
                min="-1.0"
                max="1.0"
                step="0.05"
                value={params.componente_q_pct}
                onChange={e => handleChange('componente_q_pct', parseFloat(e.target.value))}
                className="w-full h-1.5 bg-slate-200 rounded-lg appearance-none cursor-pointer accent-blue-600"
              />
              <p className="text-[11px] text-slate-500 mt-1">
                Se a qualidade do fornecimento piorar (DEC/FEC acima do limite), o Componente Q reduz a Parcela B da distribuidora.
              </p>
            </div>
          </div>
        </div>

        <div className="lg:col-span-5 bg-gradient-to-br from-slate-900 to-slate-850 text-white rounded-xl p-5 flex flex-col justify-between shadow-lg">
          <div>
            <div className="flex items-center justify-between mb-4 border-b border-slate-700/60 pb-3">
              <span className="text-xs font-bold uppercase text-slate-400 tracking-wider">Resultado da Revisão Tarifária</span>
              <span className="px-2 py-0.5 text-[10px] font-bold rounded bg-blue-500/20 text-blue-300 border border-blue-400/30">
                PRORET Submódulo 2.1
              </span>
            </div>

            {result && (
              <div className="space-y-3">
                <div className="flex justify-between items-center text-xs">
                  <span className="text-slate-300">Remuneração do Capital (BRR × WACC):</span>
                  <span className="font-semibold text-emerald-400">R$ {result.remuneracao_capital_rs_mm.toLocaleString()} MM</span>
                </div>
                <div className="flex justify-between items-center text-xs">
                  <span className="text-slate-300">OPEX Eficiente:</span>
                  <span className="font-semibold">R$ {result.opex_eficiente_rs_mm.toLocaleString()} MM</span>
                </div>
                <div className="flex justify-between items-center text-xs">
                  <span className="text-slate-300">Dedução Fator X + Comp. Q:</span>
                  <span className="font-semibold text-amber-400">- R$ {(result.deducao_fator_x_rs_mm + result.ajuste_componente_q_rs_mm).toFixed(2)} MM</span>
                </div>

                <div className="pt-2 border-t border-slate-700 flex justify-between items-center">
                  <span className="text-xs font-medium text-slate-300">Parcela B (Custos Gerenciáveis):</span>
                  <span className="text-sm font-bold text-white">R$ {result.parcela_b_rs_mm.toLocaleString()} MM</span>
                </div>

                <div className="pt-2 border-t border-slate-700 flex justify-between items-center">
                  <span className="text-xs font-bold text-blue-300 uppercase">Receita Requerida Total:</span>
                  <span className="text-base font-extrabold text-blue-300">R$ {result.receita_requerida_total_rs_mm.toLocaleString()} MM</span>
                </div>

                <div className="mt-4 bg-slate-800/80 border border-slate-700 rounded-lg p-3 text-center">
                  <span className="text-[11px] uppercase tracking-wider text-slate-400 font-semibold">Tarifa Média Homologada</span>
                  <div className="text-2xl font-black text-white mt-1">
                    R$ {result.tarifa_media_rs_mwh.toFixed(2)} <span className="text-xs font-normal text-slate-400">/ MWh</span>
                  </div>
                  <div className="text-xs text-slate-300 mt-1">
                    (Equivalente a <strong className="text-emerald-400">R$ {result.tarifa_media_rs_kwh.toFixed(4)} / kWh</strong>)
                  </div>
                </div>

                <div className="text-[11px] text-slate-300 bg-blue-950/40 border border-blue-800/40 rounded p-2.5 mt-3">
                  <strong>Impacto Regulatório:</strong> {result.analise_qualidade_dec_fec}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
