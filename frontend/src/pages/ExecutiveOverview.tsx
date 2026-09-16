import React, { useEffect, useState } from 'react';
import { StatCard } from '../components/common/StatCard';
import { Badge } from '../components/common/Badge';
import { BrazilSubsystemsMap } from '../components/map/BrazilSubsystemsMap';
import { apiService } from '../services/api';
import type { ExecutiveSummary, SubsystemId } from '../types';
import {
  Activity,
  Zap,
  TrendingUp,
  Radio,
  Percent,
  DollarSign,
  AlertTriangle,
  Layers,
  ArrowUpRight
} from 'lucide-react';

interface Props {
  selectedSubsystem: SubsystemId;
  onSelectSubsystem: (sub: SubsystemId) => void;
  onNavigateTab: (tab: any) => void;
}

export const ExecutiveOverview: React.FC<Props> = ({
  selectedSubsystem,
  onSelectSubsystem,
  onNavigateTab
}) => {
  const [data, setData] = useState<ExecutiveSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    apiService.getExecutiveSummary(selectedSubsystem)
      .then(res => setData(res))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, [selectedSubsystem]);

  if (loading || !data) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[400px]">
        <div className="text-sm font-semibold text-slate-500 animate-pulse">Carregando indicadores executivos ({selectedSubsystem})...</div>
      </div>
    );
  }

  const { kpis_destaque, matriz_sintese, alertas_recentes } = data;
  const regionLabel = selectedSubsystem === 'SIN' ? 'Brasil (Nacional - SIN)' : 
    selectedSubsystem === 'SE_CO' ? 'Sudeste / Centro-Oeste' :
    selectedSubsystem === 'S' ? 'Sul' :
    selectedSubsystem === 'NE' ? 'Nordeste' : 'Norte';

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-blue-900 to-indigo-950 text-white rounded-2xl p-6 shadow-md border border-blue-800/50">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-blue-500/30 text-blue-200 border border-blue-400/30">
                Painel de Controle Executivo (C-Level)
              </span>
              {selectedSubsystem !== 'SIN' && (
                <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-amber-400/30 text-amber-200 border border-amber-300/30">
                  Filtro: {regionLabel}
                </span>
              )}
            </div>
            <h2 className="text-xl font-bold mt-2 tracking-tight">
              Síntese Estratégica: {selectedSubsystem === 'SIN' ? 'Setor Elétrico Nacional' : `Subsistema ${regionLabel}`}
            </h2>
            <p className="text-xs text-blue-200/80 mt-1 max-w-2xl">
              Monitoramento integrado da cadeia de valor do Setor Elétrico Brasileiro. Dados consolidados de ONS, CCEE e ANEEL armazenados no BigQuery (projeto <code className="text-white font-mono">kpisetoreletrico</code>).
            </p>
          </div>
          <div className="bg-white/10 backdrop-blur-md rounded-xl p-4 border border-white/15 shrink-0 flex items-center space-x-4">
            <div className="text-right">
              <span className="text-[10px] uppercase font-bold text-blue-200">Bandeira Tarifária</span>
              <div className="text-lg font-black text-emerald-400">{kpis_destaque.bandeira_tarifaria.valor}</div>
              <span className="text-[10px] text-blue-200">Sem acréscimo tarifário</span>
            </div>
            <div className="w-10 h-10 rounded-full bg-emerald-500/20 border border-emerald-400 flex items-center justify-center text-xl">
              🌱
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="EAR% (Energia Armazenada)"
          value={`${kpis_destaque.ear_sin_pct.valor}%`}
          statusText="Favorável (Meta > 45%)"
          statusVariant="sucesso"
          subtitle="Segurança Hidrológica SIN"
          icon={<Activity className="w-4 h-4 text-blue-600" />}
        />
        <StatCard
          title="CMO Médio (Custo Marginal)"
          value={`R$ ${kpis_destaque.cmo_medio_sin.valor}`}
          unit="/ MWh"
          statusText="Estável"
          statusVariant="sucesso"
          subtitle="Despacho Térmico Moderado"
          icon={<Zap className="w-4 h-4 text-amber-600" />}
        />
        <StatCard
          title="PLD Médio (CCEE)"
          value={`R$ ${kpis_destaque.pld_medio.valor}`}
          unit="/ MWh"
          statusText="Próximo ao Piso"
          statusVariant="info"
          subtitle="Preço Spot Semanal"
          icon={<TrendingUp className="w-4 h-4 text-indigo-600" />}
        />
        <StatCard
          title="GSF (Risco Hidrológico)"
          value={kpis_destaque.gsf_risco_hidro.valor}
          statusText="Crítico (< 0.80)"
          statusVariant="critico"
          subtitle="Exposição Financeira MRE"
          icon={<AlertTriangle className="w-4 h-4 text-rose-600" />}
        />
        <StatCard
          title="RAP Transmissão"
          value={`R$ ${(kpis_destaque.rap_nacional.valor / 1000).toFixed(1)}B`}
          statusText="Contratada"
          statusVariant="sucesso"
          subtitle="Receita Anual Permitida"
          icon={<Radio className="w-4 h-4 text-blue-600" />}
        />
        <StatCard
          title="Perdas Globais (T+NT)"
          value={`${kpis_destaque.perdas_totais.valor}%`}
          statusText="Acima da Meta (12.8%)"
          statusVariant="alerta"
          subtitle="Impacto de Furtos / Fraudes"
          icon={<Percent className="w-4 h-4 text-amber-600" />}
        />
        <StatCard
          title="EBITDA Setorial Consolidado"
          value={`R$ ${(kpis_destaque.ebitda_setorial.valor / 1000).toFixed(1)}B`}
          statusText="Margem Média 34.2%"
          statusVariant="sucesso"
          subtitle="Geração, Transm. e Distr."
          icon={<DollarSign className="w-4 h-4 text-emerald-600" />}
        />
        <StatCard
          title="MMGD Conectada (Lei 14.300)"
          value="31.8 GW"
          statusText="+18% YoY"
          statusVariant="info"
          subtitle="Micro/Minigeração Solar"
          icon={<Zap className="w-4 h-4 text-amber-500" />}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-6">
          <BrazilSubsystemsMap
            selectedSubsystem={selectedSubsystem === 'SIN' ? undefined : selectedSubsystem}
            onSelectSubsystem={(sub) => onSelectSubsystem(sub)}
          />
        </div>

        <div className="lg:col-span-6 bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-3 border-b border-slate-100 pb-3">
              <div className="flex items-center space-x-2">
                <Layers className="w-4 h-4 text-blue-700" />
                <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
                  Matriz de Síntese: Cadeia de Valor & C-Level
                </h3>
              </div>
              <span className="text-[11px] text-slate-500">Governança Integrada</span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-200 text-slate-500 uppercase font-bold text-[10px]">
                    <th className="py-2 px-2">Categoria</th>
                    <th className="py-2 px-2">Owner</th>
                    <th className="py-2 px-2">Principais KPIs</th>
                    <th className="py-2 px-2 text-right">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {matriz_sintese.map((item, idx) => (
                    <tr key={idx} className="hover:bg-slate-50 transition-colors">
                      <td className="py-2.5 px-2 font-semibold text-slate-800">
                        {item.categoria}
                      </td>
                      <td className="py-2.5 px-2">
                        <span className="px-2 py-0.5 rounded bg-slate-100 text-slate-700 font-medium text-[10px]">
                          {item.owner}
                        </span>
                      </td>
                      <td className="py-2.5 px-2 text-slate-600 font-mono text-[11px]">
                        {item.kpis}
                      </td>
                      <td className="py-2.5 px-2 text-right">
                        <Badge variant={item.nivel}>
                          {item.status}
                        </Badge>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs text-slate-500">
            <span>A excelência no setor elétrico exige orquestração integrada entre física, regulação e finanças.</span>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <div className="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
          <div className="flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 text-amber-600" />
            <h3 className="text-sm font-bold text-slate-900 uppercase tracking-wider">
              Alertas Regulatórios & Semáforo de Criticidade
            </h3>
          </div>
          <button
            onClick={() => onNavigateTab('alerts')}
            className="text-xs font-semibold text-blue-700 hover:text-blue-900 flex items-center"
          >
            Ver todos ({alertas_recentes.length}) <ArrowUpRight className="w-3.5 h-3.5 ml-0.5" />
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
          {alertas_recentes.map((alt) => (
            <div
              key={alt.id}
              className={`p-3.5 rounded-lg border text-xs ${
                alt.nivel === 'critico'
                  ? 'bg-rose-50/70 border-rose-200 text-rose-900'
                  : alt.nivel === 'alerta'
                  ? 'bg-amber-50/70 border-amber-200 text-amber-900'
                  : 'bg-blue-50/70 border-blue-200 text-blue-900'
              }`}
            >
              <div className="flex items-center justify-between font-bold mb-1">
                <span>{alt.modulo}</span>
                <span className="text-[10px] opacity-75">{alt.data_evento}</span>
              </div>
              <div className="font-semibold text-slate-900">{alt.titulo}</div>
              <p className="text-slate-600 text-[11px] mt-1 line-clamp-2">{alt.descricao}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
