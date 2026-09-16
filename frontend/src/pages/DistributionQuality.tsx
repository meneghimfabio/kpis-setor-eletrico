import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';
import { StatCard } from '../components/common/StatCard';
import { Badge } from '../components/common/Badge';
import { Zap, AlertTriangle, ShieldCheck, RefreshCw, CheckCircle2 } from 'lucide-react';
import { ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip, CartesianGrid, Legend } from 'recharts';

import type { SubsystemId } from '../types';

const UF_TO_SUBSYSTEM: Record<string, SubsystemId> = {
  SP: 'SE_CO', RJ: 'SE_CO', MG: 'SE_CO', ES: 'SE_CO', GO: 'SE_CO', MT: 'SE_CO', MS: 'SE_CO', DF: 'SE_CO',
  RS: 'S', SC: 'S', PR: 'S',
  BA: 'NE', PE: 'NE', CE: 'NE', MA: 'NE', PB: 'NE', RN: 'NE', AL: 'NE', SE: 'NE', PI: 'NE',
  PA: 'N', AM: 'N', TO: 'N', RO: 'N', AP: 'N', AC: 'N', RR: 'N'
};

interface DistributionQualityProps {
  selectedSubsystem?: SubsystemId;
}

export const DistributionQuality: React.FC<DistributionQualityProps> = ({ selectedSubsystem = 'SIN' }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncFeedback, setSyncFeedback] = useState<string | null>(null);

  const loadData = () => {
    return apiService.getDistribuicaoOverview()
      .then(res => setData(res))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    loadData().finally(() => setLoading(false));
  }, []);

  const handleSyncAneel = async () => {
    try {
      setIsSyncing(true);
      setSyncFeedback(null);
      await apiService.triggerDistribuicaoIngestion();
      await loadData();
      setSyncFeedback('Dados do PRODIST ANEEL (DEC/FEC) atualizados com sucesso!');
      setTimeout(() => setSyncFeedback(null), 4000);
    } catch (err) {
      console.error(err);
      setSyncFeedback('Erro ao atualizar dados da ANEEL.');
      setTimeout(() => setSyncFeedback(null), 4000);
    } finally {
      setIsSyncing(false);
    }
  };

  if (loading || !data) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[400px]">
        <div className="text-sm font-semibold text-slate-500 animate-pulse">Carregando indicadores de Distribuição (PRODIST)...</div>
      </div>
    );
  }

  const { ranking_dec_fec: all_ranking, ultima_atualizacao_aneel } = data;
  const ranking_dec_fec = selectedSubsystem === 'SIN' 
    ? all_ranking 
    : all_ranking.filter((item: any) => UF_TO_SUBSYSTEM[item.uf] === selectedSubsystem);

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="p-2 bg-amber-50 text-amber-700 rounded-lg">
              <Zap className="w-5 h-5" />
            </span>
            <div>
              <h2 className="text-lg font-bold text-slate-900">Qualidade do Fornecimento (Módulo 8 do PRODIST)</h2>
              <p className="text-xs text-slate-500">
                Indicadores Coletivos (DEC/FEC), Individuais (DIC/FIC/DMIC/DICRI) e Nível de Tensão (DRP/DRC)
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-amber-100 text-amber-800 flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5" />
              {ultima_atualizacao_aneel || 'Fonte: ANEEL / BigQuery'}
            </span>
            <button
              onClick={handleSyncAneel}
              disabled={isSyncing}
              className={`inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-900 text-white hover:bg-slate-800 transition shadow-sm ${
                isSyncing ? 'opacity-70 cursor-not-allowed' : ''
              }`}
              title="Sincronizar indicadores DEC/FEC com Dados Abertos da ANEEL"
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

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <StatCard
          title="DEC Médio das Grandes Concessionárias"
          value="9.85 h"
          statusText="Atenção Limites ANEEL"
          statusVariant="alerta"
          subtitle="Duração Equivalente de Interrupção"
          icon={<Zap className="w-4 h-4 text-amber-600" />}
        />
        <StatCard
          title="FEC Médio das Grandes Concessionárias"
          value="5.62 vezes"
          statusText="Maioria Conforme"
          statusVariant="sucesso"
          subtitle="Frequência Equivalente de Interrupção"
          icon={<ShieldCheck className="w-4 h-4 text-blue-600" />}
        />
        <StatCard
          title="Compensações Estimadas (Módulo 9)"
          value="R$ 212.8 MM"
          statusText="Ressarcimento em Fatura"
          statusVariant="critico"
          subtitle="Penalidades por violação de limites individuais"
          icon={<AlertTriangle className="w-4 h-4 text-rose-600" />}
        />
      </div>

      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <h3 className="text-sm font-bold text-slate-900 mb-1">Benchmarking: DEC Apurado vs Limite Regulatório ANEEL (Horas/UC)</h3>
        <p className="text-xs text-slate-500 mb-4">Barras que ultrapassam a meta representam não-conformidade regulatória e risco de multa/ressarcimento</p>

        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={ranking_dec_fec} margin={{ top: 10, right: 10, left: -10, bottom: 20 }}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="nome" stroke="#64748b" fontSize={10} angle={-25} textAnchor="end" />
              <YAxis stroke="#64748b" fontSize={11} />
              <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#fff', fontSize: '12px' }} />
              <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
              <Bar dataKey="dec" name="DEC Apurado (Horas)" fill="#EF4444" radius={[4, 4, 0, 0]} />
              <Bar dataKey="meta_dec" name="Meta Limite ANEEL (Horas)" fill="#94A3B8" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <h3 className="text-sm font-bold text-slate-900 mb-3">Tabela Detalhada de Indicadores Coletivos por Concessionária</h3>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500 uppercase font-bold text-[10px]">
                <th className="py-2.5 px-3">Distribuidora</th>
                <th className="py-2.5 px-3">UF</th>
                <th className="py-2.5 px-3">DEC Apurado</th>
                <th className="py-2.5 px-3">Meta DEC</th>
                <th className="py-2.5 px-3">FEC Apurado</th>
                <th className="py-2.5 px-3">Meta FEC</th>
                <th className="py-2.5 px-3">Compensação Est.</th>
                <th className="py-2.5 px-3 text-right">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {ranking_dec_fec.map((row: any, idx: number) => {
                const isDecBad = row.dec > row.meta_dec;
                const isFecBad = row.fec > row.meta_fec;
                return (
                  <tr key={idx} className="hover:bg-slate-50">
                    <td className="py-3 px-3 font-bold text-slate-800">{row.nome}</td>
                    <td className="py-3 px-3 text-slate-500">{row.uf}</td>
                    <td className={`py-3 px-3 font-semibold ${isDecBad ? 'text-rose-600 font-bold' : 'text-emerald-700'}`}>
                      {row.dec} h
                    </td>
                    <td className="py-3 px-3 text-slate-500">{row.meta_dec} h</td>
                    <td className={`py-3 px-3 font-semibold ${isFecBad ? 'text-rose-600 font-bold' : 'text-emerald-700'}`}>
                      {row.fec}x
                    </td>
                    <td className="py-3 px-3 text-slate-500">{row.meta_fec}x</td>
                    <td className="py-3 px-3 text-slate-700 font-medium">R$ {row.compensacao_rs_mm} MM</td>
                    <td className="py-3 px-3 text-right">
                      <Badge variant={row.status === 'Conforme' ? 'sucesso' : row.status.includes('Crítico') ? 'critico' : 'alerta'}>
                        {row.status}
                      </Badge>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
