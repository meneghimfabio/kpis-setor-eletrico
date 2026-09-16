import React, { useEffect, useState, useMemo } from 'react';
import { apiService } from '../services/api';
import { StatCard } from '../components/common/StatCard';
import { Badge } from '../components/common/Badge';
import { ProretSimulator } from '../components/simulator/ProretSimulator';
import { DollarSign, TrendingUp, Landmark, ShieldCheck, Database, CheckCircle2, Search, Zap, Layers } from 'lucide-react';

export const FinancialProret: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [tariffSearch, setTariffSearch] = useState('');
  const [activeTariffTab, setActiveTariffTab] = useState<'b1' | 'b3' | 'a4'>('b1');

  useEffect(() => {
    apiService.getFinanceiroOverview()
      .then(res => setData(res))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading || !data) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[400px]">
        <div className="text-sm font-semibold text-slate-500 animate-pulse">Carregando dados Econômico-Financeiros e PRORET...</div>
      </div>
    );
  }

  const {
    indicadores_setoriais,
    empresas_dre,
    qualidade_dados_ativos,
    ranking_tarifario_aneel = [],
    ultima_atualizacao_aneel,
    _metadata
  } = data;

  const filteredTariffs = useMemo(() => {
    let list = [...ranking_tarifario_aneel];
    if (tariffSearch.trim()) {
      const q = tariffSearch.toLowerCase();
      list = list.filter((item: any) =>
        (item.distribuidora && item.distribuidora.toLowerCase().includes(q)) ||
        (item.concessionaria && item.concessionaria.toLowerCase().includes(q)) ||
        (item.uf && item.uf.toLowerCase().includes(q))
      );
    }
    if (activeTariffTab === 'b1') {
      list.sort((a, b) => (a.tarifa_b1_rs_kwh || 0) - (b.tarifa_b1_rs_kwh || 0));
    } else if (activeTariffTab === 'b3') {
      list.sort((a, b) => (a.tarifa_b3_comercial_rs_kwh || 0) - (b.tarifa_b3_comercial_rs_kwh || 0));
    } else if (activeTariffTab === 'a4') {
      list.sort((a, b) => (a.a4_verde_demanda_rs_kw || 0) - (b.a4_verde_demanda_rs_kw || 0));
    }
    return list;
  }, [ranking_tarifario_aneel, tariffSearch, activeTariffTab]);

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="p-2 bg-emerald-50 text-emerald-700 rounded-lg">
              <DollarSign className="w-5 h-5" />
            </span>
            <div>
              <h2 className="text-lg font-bold text-slate-900">Econômico-Financeiro & Motor Regulatório PRORET</h2>
              <p className="text-xs text-slate-500">
                Tarifas Oficiais Homologadas ANEEL (103 Concessionárias), DRE Corporativa, CAPEX e Simulador de Revisão Tarifária
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5" />
              {ultima_atualizacao_aneel || 'Fonte: ANEEL / BigQuery Gold'}
            </span>
            {_metadata?.bi_engine_accelerated && (
              <span className="px-2.5 py-0.5 rounded-full text-[11px] font-semibold bg-blue-50 text-blue-700 border border-blue-200">
                BI Engine Ativo
              </span>
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="EBITDA Total Setorial"
          value={`R$ ${(indicadores_setoriais.ebitda_total_setor_rs_mm / 1000).toFixed(1)} B`}
          statusText="Sólida Geração de Caixa"
          statusVariant="sucesso"
          subtitle="Margem Média: 34.2%"
          icon={<DollarSign className="w-4 h-4 text-emerald-600" />}
        />
        <StatCard
          title="CAPEX Executado no Ano"
          value={`R$ ${(indicadores_setoriais.capex_executado_ano_rs_mm / 1000).toFixed(1)} B`}
          statusText="Expansão & Modernização"
          statusVariant="info"
          subtitle="Adição de Ativos na BRR"
          icon={<TrendingUp className="w-4 h-4 text-blue-600" />}
        />
        <StatCard
          title="Alavancagem Média (DL / EBITDA)"
          value={`${indicadores_setoriais.alavancagem_media_dl_ebitda}x`}
          statusText="Faixa Segura (< 3.5x)"
          statusVariant="sucesso"
          subtitle="Capacidade de Pagamento"
          icon={<Landmark className="w-4 h-4 text-amber-600" />}
        />
        <StatCard
          title="Dividend Yield Médio"
          value={`${indicadores_setoriais.dividend_yield_medio_pct}%`}
          statusText="Retorno ao Acionista"
          statusVariant="sucesso"
          subtitle="Após obrigações setoriais"
          icon={<ShieldCheck className="w-4 h-4 text-emerald-600" />}
        />
      </div>

      {/* ANEEL REAL TARIFF RANKING - BIGQUERY GOLD (103 CONCESSIONÁRIAS) */}
      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-3 border-b border-slate-100 pb-4 mb-4">
          <div className="flex items-center space-x-2">
            <span className="p-1.5 bg-blue-50 text-blue-700 rounded-lg">
              <Zap className="w-4 h-4" />
            </span>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-bold text-slate-900">
                  Ranking Tarifário Homologado ANEEL (PRORET - {ranking_tarifario_aneel.length} Concessionárias)
                </h3>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-blue-100 text-blue-800">
                  Dados Reais BigQuery Gold
                </span>
              </div>
              <p className="text-xs text-slate-500">
                Tarifas de aplicação homologadas pela ANEEL para consumo residencial (B1), comercial (B3) e demanda industrial (A4 Verde)
              </p>
            </div>
          </div>

          {/* Controls: Search and Tabs */}
          <div className="flex flex-col sm:flex-row items-center gap-2">
            <div className="relative w-full sm:w-64">
              <Search className="w-3.5 h-3.5 absolute left-2.5 top-2.5 text-slate-400" />
              <input
                type="text"
                value={tariffSearch}
                onChange={(e) => setTariffSearch(e.target.value)}
                placeholder="Buscar concessionária ou UF..."
                className="w-full pl-8 pr-3 py-1.5 text-xs bg-slate-50 border border-slate-200 rounded-lg focus:outline-none focus:ring-1 focus:ring-blue-500"
              />
            </div>

            <div className="flex items-center bg-slate-100 p-0.5 rounded-lg text-xs font-semibold">
              <button
                onClick={() => setActiveTariffTab('b1')}
                className={`px-2.5 py-1 rounded-md transition ${
                  activeTariffTab === 'b1' ? 'bg-white text-blue-700 shadow-xs' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                B1 Residencial
              </button>
              <button
                onClick={() => setActiveTariffTab('b3')}
                className={`px-2.5 py-1 rounded-md transition ${
                  activeTariffTab === 'b3' ? 'bg-white text-blue-700 shadow-xs' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                B3 Comercial
              </button>
              <button
                onClick={() => setActiveTariffTab('a4')}
                className={`px-2.5 py-1 rounded-md transition ${
                  activeTariffTab === 'a4' ? 'bg-white text-blue-700 shadow-xs' : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                A4 Industrial
              </button>
            </div>
          </div>
        </div>

        {/* Table of 103 Distributors */}
        <div className="overflow-x-auto max-h-[440px] overflow-y-auto">
          <table className="w-full text-left text-xs">
            <thead className="sticky top-0 bg-white shadow-xs z-10">
              <tr className="border-b border-slate-200 text-slate-500 uppercase font-bold text-[10px]">
                <th className="py-2.5 px-3"># Pos</th>
                <th className="py-2.5 px-3">Distribuidora / Concessionária</th>
                <th className="py-2.5 px-3">UF</th>
                <th className="py-2.5 px-3 text-right">
                  {activeTariffTab === 'b1' ? 'Tarifa B1 (R$/kWh)' : activeTariffTab === 'b3' ? 'Tarifa B3 (R$/kWh)' : 'Demanda A4 (R$/kW)'}
                </th>
                <th className="py-2.5 px-3 text-center">TUSD vs TE (Fio vs Energia)</th>
                <th className="py-2.5 px-3 text-right">A4 Fora Ponta (R$/MWh)</th>
                <th className="py-2.5 px-3">Resolução ANEEL</th>
                <th className="py-2.5 px-3 text-right">Vigência</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filteredTariffs.map((t: any, idx: number) => {
                const pos = idx + 1;
                const valorPrincipal = activeTariffTab === 'b1' 
                  ? t.tarifa_b1_rs_kwh 
                  : activeTariffTab === 'b3' 
                  ? t.tarifa_b3_comercial_rs_kwh 
                  : t.a4_verde_demanda_rs_kw;
                const unit = activeTariffTab === 'a4' ? 'R$/kW' : 'R$/kWh';

                return (
                  <tr key={idx} className="hover:bg-slate-50/80 transition">
                    <td className="py-2.5 px-3 font-bold text-slate-600">
                      {pos === 1 ? (
                        <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-amber-100 text-amber-800 text-[10px] font-extrabold">1º</span>
                      ) : pos === 2 ? (
                        <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-slate-200 text-slate-700 text-[10px] font-extrabold">2º</span>
                      ) : pos === 3 ? (
                        <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-amber-50 text-amber-700 text-[10px] font-extrabold border border-amber-200">3º</span>
                      ) : (
                        <span className="text-slate-400 font-medium">{pos}º</span>
                      )}
                    </td>
                    <td className="py-2.5 px-3">
                      <div className="font-bold text-slate-800">{t.concessionaria || t.distribuidora}</div>
                      <div className="text-[10px] text-slate-400">{t.distribuidora}</div>
                    </td>
                    <td className="py-2.5 px-3">
                      <span className="px-1.5 py-0.5 rounded text-[10px] font-semibold bg-slate-100 text-slate-700 border border-slate-200">
                        {t.uf}
                      </span>
                    </td>
                    <td className="py-2.5 px-3 text-right">
                      <span className="font-bold text-slate-900 text-sm">
                        {typeof valorPrincipal === 'number' ? valorPrincipal.toFixed(4) : valorPrincipal}
                      </span>
                      <span className="text-[10px] text-slate-400 ml-1">{unit}</span>
                    </td>
                    <td className="py-2.5 px-3">
                      <div className="flex flex-col items-center">
                        <div className="flex justify-between w-32 text-[10px] text-slate-500 mb-0.5">
                          <span className="text-blue-600 font-semibold">{t.share_tusd_fio_pct}% TUSD</span>
                          <span className="text-emerald-600 font-semibold">{t.share_te_energia_pct}% TE</span>
                        </div>
                        <div className="w-32 h-1.5 bg-slate-100 rounded-full overflow-hidden flex">
                          <div style={{ width: `${t.share_tusd_fio_pct}%` }} className="bg-blue-500 h-full"></div>
                          <div style={{ width: `${t.share_te_energia_pct}%` }} className="bg-emerald-500 h-full"></div>
                        </div>
                      </div>
                    </td>
                    <td className="py-2.5 px-3 text-right font-medium text-slate-700">
                      R$ {typeof t.a4_verde_energia_fora_ponta_rs_mwh === 'number' ? t.a4_verde_energia_fora_ponta_rs_mwh.toFixed(2) : t.a4_verde_energia_fora_ponta_rs_mwh}
                    </td>
                    <td className="py-2.5 px-3 text-slate-600 text-[11px] max-w-[200px] truncate" title={t.resolucao_homologatoria}>
                      {t.resolucao_homologatoria ? t.resolucao_homologatoria.split(',')[0] : 'Homologação ANEEL'}
                    </td>
                    <td className="py-2.5 px-3 text-right text-slate-500 text-[11px]">
                      {t.data_vigencia || '-'}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
        <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400 border-t border-slate-100 pt-2">
          <span>Mostrando {filteredTariffs.length} de {ranking_tarifario_aneel.length} distribuidoras homologadas</span>
          <span className="flex items-center gap-1 text-blue-600 font-medium">
            <Layers className="w-3.5 h-3.5" /> Pipeline Medallion: GCS Bronze ➔ BigQuery Silver ➔ BigQuery Gold
          </span>
        </div>
      </div>

      <ProretSimulator />

      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <h3 className="text-sm font-bold text-slate-900 mb-1">Painel Corporativo: DRE e Métricas das Principais Empresas</h3>
        <p className="text-xs text-slate-500 mb-4">Demonstrativo comparativo de Receita Líquida, EBITDA, Margem, Lucro e Alavancagem</p>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500 uppercase font-bold text-[10px]">
                <th className="py-2.5 px-3">Empresa</th>
                <th className="py-2.5 px-3">Receita Líquida</th>
                <th className="py-2.5 px-3">EBITDA</th>
                <th className="py-2.5 px-3">Margem EBITDA</th>
                <th className="py-2.5 px-3">Lucro Líquido</th>
                <th className="py-2.5 px-3">CAPEX</th>
                <th className="py-2.5 px-3 text-right">Alavancagem</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {empresas_dre.map((emp: any, idx: number) => (
                <tr key={idx} className="hover:bg-slate-50">
                  <td className="py-3 px-3 font-bold text-slate-800">{emp.empresa}</td>
                  <td className="py-3 px-3 text-slate-700">R$ {emp.receita_liquida_rs_mm.toLocaleString()} MM</td>
                  <td className="py-3 px-3 font-bold text-slate-900">R$ {emp.ebitda_rs_mm.toLocaleString()} MM</td>
                  <td className="py-3 px-3 font-semibold text-emerald-700">{emp.margem_ebitda_pct}%</td>
                  <td className="py-3 px-3 text-slate-700">R$ {emp.lucro_liquido_rs_mm.toLocaleString()} MM</td>
                  <td className="py-3 px-3 text-blue-700 font-medium">R$ {emp.capex_rs_mm.toLocaleString()} MM</td>
                  <td className="py-3 px-3 text-right font-semibold">
                    <span className={`px-2 py-0.5 rounded text-[11px] ${emp.alavancagem > 3.0 ? 'bg-amber-100 text-amber-800' : 'bg-emerald-100 text-emerald-800'}`}>
                      {emp.alavancagem}x
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <div className="flex items-center space-x-2 mb-2">
          <Database className="w-4 h-4 text-blue-600" />
          <h3 className="text-sm font-bold text-slate-900">Qualidade de Dados & Gestão de Ativos Regulatórios (MCPSE / PRORET)</h3>
        </div>
        <p className="text-xs text-slate-500 mb-4">
          O motor invisível que sustenta a regulação: Acuracidade da BRR (ERP vs Homologada ANEEL), Ativos Órfãos e Lead Time de Capitalização
        </p>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500 uppercase font-bold text-[10px]">
                <th className="py-2.5 px-3">Distribuidora</th>
                <th className="py-2.5 px-3">Acurácia BRR (Meta &gt; 99%)</th>
                <th className="py-2.5 px-3">Ativos Órfãos (Meta &lt; 1%)</th>
                <th className="py-2.5 px-3">Consistência Cliente-UC-Medidor</th>
                <th className="py-2.5 px-3">Lead Time Capitalização</th>
                <th className="py-2.5 px-3 text-right">Avaliação</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {qualidade_dados_ativos.map((qa: any, idx: number) => (
                <tr key={idx} className="hover:bg-slate-50">
                  <td className="py-3 px-3 font-bold text-slate-800">{qa.distribuidora}</td>
                  <td className={`py-3 px-3 font-semibold ${qa.acuracia_brr_pct >= 99.0 ? 'text-emerald-700' : 'text-amber-700'}`}>
                    {qa.acuracia_brr_pct}%
                  </td>
                  <td className={`py-3 px-3 font-semibold ${qa.ativos_orfaos_pct <= 1.0 ? 'text-emerald-700' : 'text-rose-600'}`}>
                    {qa.ativos_orfaos_pct}%
                  </td>
                  <td className="py-3 px-3 text-slate-700">{qa.consistencia_uc_medidor_pct}%</td>
                  <td className="py-3 px-3 text-slate-700">{qa.lead_time_capitalizacao_dias} dias</td>
                  <td className="py-3 px-3 text-right">
                    <Badge variant={qa.status === 'Excelente' ? 'sucesso' : qa.status === 'Crítico' ? 'critico' : 'alerta'}>
                      {qa.status}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
