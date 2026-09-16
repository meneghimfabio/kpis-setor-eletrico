import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';
import { StatCard } from '../components/common/StatCard';
import { Badge } from '../components/common/Badge';
import { TrendingUp, AlertTriangle, Wind, Sun, ShieldAlert, DollarSign, RefreshCw, CheckCircle2 } from 'lucide-react';
import {
  ResponsiveContainer,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid
} from 'recharts';

import type { SubsystemId } from '../types';

interface CceeMarketProps {
  selectedSubsystem?: SubsystemId;
}

export const CceeMarket: React.FC<CceeMarketProps> = ({ selectedSubsystem = 'SIN' }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncFeedback, setSyncFeedback] = useState<string | null>(null);

  const loadData = () => {
    return apiService.getCceeOverview()
      .then(res => setData(res))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    loadData().finally(() => setLoading(false));
  }, []);

  const handleSyncCcee = async () => {
    try {
      setIsSyncing(true);
      setSyncFeedback(null);
      await apiService.triggerCceeIngestion();
      await loadData();
      setSyncFeedback('Dados do Mercado CCEE atualizados com sucesso!');
      setTimeout(() => setSyncFeedback(null), 4000);
    } catch (err) {
      console.error(err);
      setSyncFeedback('Erro ao atualizar dados da CCEE.');
      setTimeout(() => setSyncFeedback(null), 4000);
    } finally {
      setIsSyncing(false);
    }
  };

  if (loading || !data) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[400px]">
        <div className="text-sm font-semibold text-slate-500 animate-pulse">Carregando dados de Mercado CCEE...</div>
      </div>
    );
  }

  const { pld_atual, gsf_historico, ess_encargos, bandeira_vigente, curtailment: all_curtailment, ultima_atualizacao_ccee } = data;
  const curtailment = selectedSubsystem === 'SIN'
    ? all_curtailment
    : all_curtailment.filter((c: any) => c.subsistema === selectedSubsystem);

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="p-2 bg-indigo-50 text-indigo-700 rounded-lg">
              <TrendingUp className="w-5 h-5" />
            </span>
            <div>
              <h2 className="text-lg font-bold text-slate-900">Comercialização & Mercado (CCEE)</h2>
              <p className="text-xs text-slate-500">
                Preço de Liquidação das Diferenças (PLD), Fator de Risco Hidrológico (GSF), Encargos ESS e Curtailment
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-indigo-100 text-indigo-800 flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5" />
              {ultima_atualizacao_ccee || 'Fonte: CCEE / BigQuery'}
            </span>
            <button
              onClick={handleSyncCcee}
              disabled={isSyncing}
              className={`inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-900 text-white hover:bg-slate-800 transition shadow-sm ${
                isSyncing ? 'opacity-70 cursor-not-allowed' : ''
              }`}
              title="Sincronizar com dados oficiais de mercado da CCEE"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isSyncing ? 'animate-spin' : ''}`} />
              <span>{isSyncing ? 'Sincronizando CCEE...' : 'Atualizar Dados CCEE'}</span>
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
          title="PLD Médio Brasil"
          value={`R$ ${pld_atual.pld_medio_rs_mwh}`}
          unit="/ MWh"
          statusText="Piso Regulatório"
          statusVariant="info"
          subtitle={`Teto: R$ ${pld_atual.pld_teto_rs_mwh} | Piso: R$ ${pld_atual.pld_piso_rs_mwh}`}
          icon={<DollarSign className="w-4 h-4 text-indigo-600" />}
        />
        <StatCard
          title="GSF Atual (Risco Hidrológico)"
          value="0.76"
          statusText="Crítico (< 0.80)"
          statusVariant="critico"
          subtitle="Geração Física / Garantia Física"
          icon={<AlertTriangle className="w-4 h-4 text-rose-600" />}
        />
        <StatCard
          title="Encargos ESS do Mês"
          value={`R$ ${ess_encargos.total_mes_rs_mm} MM`}
          statusText="61.8% Térmicas"
          statusVariant="alerta"
          subtitle="Segurança Energética"
          icon={<ShieldAlert className="w-4 h-4 text-amber-600" />}
        />
        <StatCard
          title="Bandeira Tarifária"
          value={bandeira_vigente.bandeira}
          statusText="R$ 0,00 / kWh"
          statusVariant="sucesso"
          subtitle={bandeira_vigente.justificativa}
          icon={<Sun className="w-4 h-4 text-emerald-600" />}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-7 bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
          <div className="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
            <div>
              <h3 className="text-sm font-bold text-slate-900">Evolução do GSF (Generation Scaling Factor)</h3>
              <p className="text-xs text-slate-500">GSF &lt; 1 indica que usinas hidrelétricas geraram abaixo da sua garantia física.</p>
            </div>
            <Badge variant="critico">Risco Hidro MRE</Badge>
          </div>

          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={gsf_historico} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="mes" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} domain={[0.65, 1.0]} />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#fff', fontSize: '12px' }} />
                <Line type="monotone" dataKey="gsf" name="GSF Apurado" stroke="#E11D48" strokeWidth={3} dot={{ r: 4 }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="lg:col-span-5 bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2 mb-3 border-b border-slate-100 pb-2">
              <Wind className="w-4 h-4 text-blue-600" />
              <h3 className="text-sm font-bold text-slate-900">Curtailment de Renováveis (Corte pelo ONS)</h3>
            </div>
            <p className="text-xs text-slate-500 mb-3">
              Energia eólica e solar cortada (constrained-off) por limitações no escoamento de transmissão.
            </p>

            <div className="space-y-3 text-xs">
              {curtailment.map((c: any, idx: number) => (
                <div key={idx} className="p-3 rounded-lg border border-slate-200 bg-slate-50">
                  <div className="flex justify-between font-bold text-slate-900">
                    <span className="flex items-center">
                      {c.fonte === 'Eólica' ? <Wind className="w-3.5 h-3.5 mr-1 text-blue-600" /> : <Sun className="w-3.5 h-3.5 mr-1 text-amber-500" />}
                      {c.fonte} ({c.subsistema})
                    </span>
                    <Badge variant="critico">{c.taxa_curtailment_pct}% cortada</Badge>
                  </div>
                  <div className="flex justify-between text-[11px] text-slate-500 mt-2">
                    <span>Gerada: {c.gerada_gwh.toLocaleString()} GWh</span>
                    <span className="text-rose-600 font-semibold">Cortada: {c.cortada_gwh.toLocaleString()} GWh</span>
                  </div>
                  <div className="text-[10px] text-slate-400 mt-1 italic">
                    Motivo: {c.motivo}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <h3 className="text-sm font-bold text-slate-900 mb-1">Encargos de Serviço do Sistema (ESS) por Categoria</h3>
        <p className="text-xs text-slate-500 mb-4">Custo alocado aos agentes para manutenção da segurança operativa</p>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {ess_encargos.categorias.map((cat: any, idx: number) => (
            <div key={idx} className="p-4 rounded-xl border border-slate-200 bg-slate-50">
              <div className="text-xs font-semibold text-slate-600">{cat.tipo}</div>
              <div className="text-xl font-bold text-slate-900 mt-1">R$ {cat.valor_rs_mm} MM</div>
              <div className="text-xs text-blue-600 font-medium mt-1">{cat.pct}% do total de encargos</div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
