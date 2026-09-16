import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';
import { StatCard } from '../components/common/StatCard';
import { Badge } from '../components/common/Badge';
import { Percent, Sun, ShieldAlert, DollarSign, RefreshCw, CheckCircle2 } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from 'recharts';

import type { SubsystemId } from '../types';

const UF_TO_SUBSYSTEM: Record<string, SubsystemId> = {
  SP: 'SE_CO', RJ: 'SE_CO', MG: 'SE_CO', ES: 'SE_CO', GO: 'SE_CO', MT: 'SE_CO', MS: 'SE_CO', DF: 'SE_CO',
  RS: 'S', SC: 'S', PR: 'S',
  BA: 'NE', PE: 'NE', CE: 'NE', MA: 'NE', PB: 'NE', RN: 'NE', AL: 'NE', SE: 'NE', PI: 'NE',
  PA: 'N', AM: 'N', TO: 'N', RO: 'N', AP: 'N', AC: 'N', RR: 'N'
};

const DIST_TO_SUBSYSTEM: Record<string, SubsystemId> = {
  LIGHT: 'SE_CO', EQUATORIAL_PA: 'N', ENEL_SP: 'SE_CO', CEMIG_D: 'SE_CO', CPFL_PAULISTA: 'SE_CO', COPEL_DIS: 'S', EQUATORIAL_MA: 'NE', RGE_SUL: 'S', CELESC: 'S', NEOENERGIA_COELBA: 'NE', EQUATORIAL_GO: 'SE_CO'
};

interface LossesMmgdProps {
  selectedSubsystem?: SubsystemId;
}

export const LossesMmgd: React.FC<LossesMmgdProps> = ({ selectedSubsystem = 'SIN' }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncFeedback, setSyncFeedback] = useState<string | null>(null);

  const loadData = () => {
    return apiService.getPerdasMmgdOverview()
      .then(res => setData(res))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    loadData().finally(() => setLoading(false));
  }, []);

  const handleSyncMmgd = async () => {
    try {
      setIsSyncing(true);
      setSyncFeedback(null);
      await apiService.triggerPerdasMmgdIngestion();
      await loadData();
      setSyncFeedback('Dados de Perdas e MMGD da ANEEL atualizados com sucesso!');
      setTimeout(() => setSyncFeedback(null), 4000);
    } catch (err) {
      console.error(err);
      setSyncFeedback('Erro ao atualizar dados de Perdas e MMGD.');
      setTimeout(() => setSyncFeedback(null), 4000);
    } finally {
      setIsSyncing(false);
    }
  };

  if (loading || !data) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[400px]">
        <div className="text-sm font-semibold text-slate-500 animate-pulse">Carregando dados de Perdas e MMGD...</div>
      </div>
    );
  }

  const { perdas_distribuidoras: all_perdas, mmgd_estatisticas: all_mmgd, inadimplencia_pdd: all_pdd, ultima_atualizacao_aneel } = data;
  
  const perdas_distribuidoras = selectedSubsystem === 'SIN'
    ? all_perdas
    : all_perdas.filter((d: any) => (d.uf && UF_TO_SUBSYSTEM[d.uf] === selectedSubsystem) || DIST_TO_SUBSYSTEM[d.distribuidora] === selectedSubsystem);

  const top_ufs_potencia_mw = selectedSubsystem === 'SIN'
    ? all_mmgd.top_ufs_potencia_mw
    : all_mmgd.top_ufs_potencia_mw.filter((u: any) => UF_TO_SUBSYSTEM[u.uf] === selectedSubsystem);

  const inadimplencia_pdd = selectedSubsystem === 'SIN'
    ? all_pdd
    : all_pdd.filter((p: any) => DIST_TO_SUBSYSTEM[p.distribuidora] === selectedSubsystem);

  const mmgd_estatisticas = {
    ...all_mmgd,
    top_ufs_potencia_mw
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="p-2 bg-rose-50 text-rose-700 rounded-lg">
              <Percent className="w-5 h-5" />
            </span>
            <div>
              <h2 className="text-lg font-bold text-slate-900">Perdas de Energia & Impacto da Micro e Minigeração (MMGD)</h2>
              <p className="text-xs text-slate-500">
                Perdas Técnicas (Módulo 7 PRODIST), Perdas Não-Técnicas (Furtos/Fraudes), Lei 14.300 e Inadimplência/PDD
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-rose-100 text-rose-800 flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5" />
              {ultima_atualizacao_aneel || 'Fonte: ANEEL / BigQuery'}
            </span>
            <button
              onClick={handleSyncMmgd}
              disabled={isSyncing}
              className={`inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-900 text-white hover:bg-slate-800 transition shadow-sm ${
                isSyncing ? 'opacity-70 cursor-not-allowed' : ''
              }`}
              title="Sincronizar dados de perdas e MMGD com a ANEEL"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isSyncing ? 'animate-spin' : ''}`} />
              <span>{isSyncing ? 'Sincronizando ANEEL...' : 'Atualizar Dados ANEEL'}</span>
            </button>
          </div>
        </div>
        {syncFeedback && (
          <div className="mt-3 p-2 text-xs bg-emerald-50 text-emerald-700 rounded border border-emerald-200 animate-fadeIn">
            {syncFeedback}
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="Perdas Não-Técnicas (Furtos)"
          value="35.4 TWh"
          statusText="Grande Ofensor da Margem"
          statusVariant="critico"
          subtitle="6.91% da Energia Injetada"
          icon={<ShieldAlert className="w-4 h-4 text-rose-600" />}
        />
        <StatCard
          title="Perdas Técnicas (Rede/Joule)"
          value="41.2 TWh"
          statusText="Conforme Física de Rede"
          statusVariant="sucesso"
          subtitle="8.04% da Energia Injetada"
          icon={<Percent className="w-4 h-4 text-blue-600" />}
        />
        <StatCard
          title="Potência MMGD Instalada"
          value={`${mmgd_estatisticas.potencia_instalada_total_gw} GW`}
          statusText="Lei 14.300"
          statusVariant="info"
          subtitle={`${mmgd_estatisticas.qtd_unidades_consumidoras_gd.toLocaleString()} Unidades Geradoras`}
          icon={<Sun className="w-4 h-4 text-amber-500" />}
        />
        <StatCard
          title="Impacto no Mercado Faturado"
          value={`- ${mmgd_estatisticas.impacto_perda_mercado_cativo_pct}%`}
          statusText="Erosão de Parcela B"
          statusVariant="alerta"
          subtitle="Autogeração Solar no Cativo"
          icon={<DollarSign className="w-4 h-4 text-amber-600" />}
        />
      </div>

      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <h3 className="text-sm font-bold text-slate-900 mb-1">Perdas Técnicas vs Não-Técnicas por Distribuidora (% da Energia Injetada)</h3>
        <p className="text-xs text-slate-500 mb-4">Distribuidoras com perdas comerciais elevadas sofrem descompasso com a cobertura tarifária da ANEEL</p>

        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={perdas_distribuidoras} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="distribuidora" stroke="#64748b" fontSize={11} />
              <YAxis stroke="#64748b" fontSize={11} />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#fff', fontSize: '12px' }} />
              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
              <Bar dataKey="perda_tecnica_pct" name="Perdas Técnicas (%)" fill="#60A5FA" stackId="a" />
              <Bar dataKey="perda_nao_tecnica_pct" name="Perdas Comerciais / Furtos (%)" fill="#F43F5E" stackId="a" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-6 bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
          <div className="flex items-center space-x-2 mb-3 border-b border-slate-100 pb-2">
            <Sun className="w-4 h-4 text-amber-500" />
            <h3 className="text-sm font-bold text-slate-900">Penetração de MMGD Solar por Estado</h3>
          </div>
          <div className="space-y-2.5 text-xs">
            {mmgd_estatisticas.top_ufs_potencia_mw.map((item: any, idx: number) => (
              <div key={idx} className="flex justify-between items-center p-2 rounded bg-slate-50 border border-slate-200">
                <span className="font-bold text-slate-800">Estado: {item.uf}</span>
                <div className="text-right">
                  <span className="font-bold text-blue-700">{item.potencia_mw.toLocaleString()} MW</span>
                  <span className="text-[10px] text-slate-500 ml-2">({item.conexoes.toLocaleString()} UCs)</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="lg:col-span-6 bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
          <div className="flex items-center space-x-2 mb-3 border-b border-slate-100 pb-2">
            <DollarSign className="w-4 h-4 text-emerald-600" />
            <h3 className="text-sm font-bold text-slate-900">Inadimplência & Provisão (PDD)</h3>
          </div>
          <div className="space-y-2.5 text-xs">
            {inadimplencia_pdd.map((item: any, idx: number) => (
              <div key={idx} className="flex justify-between items-center p-2 rounded bg-slate-50 border border-slate-200">
                <div>
                  <span className="font-bold text-slate-800">{item.distribuidora}</span>
                  <span className="text-[10px] text-slate-500 ml-2">Taxa: {item.taxa_inadimplencia_pct}%</span>
                </div>
                <div className="flex items-center space-x-2">
                  <span className="font-semibold text-slate-900">PDD: R$ {item.pdd_rs_mm} MM</span>
                  <Badge variant={item.status === 'Excelente' ? 'sucesso' : item.status === 'Crítico' ? 'critico' : 'alerta'}>
                    {item.status}
                  </Badge>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
