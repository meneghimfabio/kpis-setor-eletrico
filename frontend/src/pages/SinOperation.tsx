import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';
import { Badge } from '../components/common/Badge';
import { Activity, Droplets, Flame, BarChart2, RefreshCw, CheckCircle2 } from 'lucide-react';
import {
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend
} from 'recharts';

import type { SubsystemId } from '../types';

interface SinOperationProps {
  selectedSubsystem?: SubsystemId;
}

export const SinOperation: React.FC<SinOperationProps> = ({ selectedSubsystem = 'SIN' }) => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [isSyncing, setIsSyncing] = useState(false);
  const [syncFeedback, setSyncFeedback] = useState<string | null>(null);

  const loadData = () => {
    return apiService.getSinOverview()
      .then(res => setData(res))
      .catch(err => console.error(err));
  };

  useEffect(() => {
    loadData().finally(() => setLoading(false));
  }, []);

  const handleSyncOns = async () => {
    try {
      setIsSyncing(true);
      setSyncFeedback(null);
      await apiService.triggerSinIngestion([2025, 2026]);
      await loadData();
      setSyncFeedback('Dados do ONS atualizados com sucesso!');
      setTimeout(() => setSyncFeedback(null), 4000);
    } catch (err) {
      console.error(err);
      setSyncFeedback('Erro ao atualizar dados do ONS.');
      setTimeout(() => setSyncFeedback(null), 4000);
    } finally {
      setIsSyncing(false);
    }
  };

  if (loading || !data) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[400px]">
        <div className="text-sm font-semibold text-slate-500 animate-pulse">Carregando dados da Operação do SIN...</div>
      </div>
    );
  }

  const { ear_atual, ear_historico, ena_subsistemas, cmo_atual, cmo_historico, ultima_atualizacao_ons } = data;

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="p-2 bg-emerald-50 text-emerald-700 rounded-lg">
              <Activity className="w-5 h-5" />
            </span>
            <div>
              <h2 className="text-lg font-bold text-slate-900">Operação do SIN: O Pulso da Geração e Hidrologia</h2>
              <p className="text-xs text-slate-500">
                Acompanhamento de Energia Armazenada (EAR%), Afluência (ENA% MLT) e Custo Marginal de Operação (CMO) por subsistema
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5" />
              {ultima_atualizacao_ons || 'Fonte: ONS / BigQuery'}
            </span>
            <button
              onClick={handleSyncOns}
              disabled={isSyncing}
              className={`inline-flex items-center space-x-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-slate-900 text-white hover:bg-slate-800 transition shadow-sm ${
                isSyncing ? 'opacity-70 cursor-not-allowed' : ''
              }`}
              title="Baixar dados diários mais recentes da API de Dados Abertos do ONS"
            >
              <RefreshCw className={`w-3.5 h-3.5 ${isSyncing ? 'animate-spin' : ''}`} />
              <span>{isSyncing ? 'Sincronizando ONS...' : 'Atualizar Dados ONS'}</span>
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
        {ear_atual.map((ear: any) => {
          const isSelected = selectedSubsystem !== 'SIN' && ear.subsistema === selectedSubsystem;
          return (
            <div
              key={ear.subsistema}
              className={`bg-white rounded-xl border p-4 shadow-sm transition-all ${
                isSelected
                  ? 'border-blue-500 ring-2 ring-blue-500/20 bg-blue-50/10'
                  : 'border-slate-200/80'
              }`}
            >
              <div className="flex justify-between items-center text-xs text-slate-500 mb-1">
                <div className="flex items-center gap-1.5">
                  <span className="font-bold uppercase tracking-wider">{ear.subsistema}</span>
                  {isSelected && (
                    <span className="px-1.5 py-0.2 text-[9px] font-bold rounded bg-blue-100 text-blue-800">
                      Selecionado
                    </span>
                  )}
                </div>
                <Badge variant={ear.status_criticidade === 'Favorável' || ear.status_criticidade === 'Favoravel' ? 'sucesso' : 'alerta'}>
                  {ear.status_criticidade}
                </Badge>
              </div>
              <div className="text-2xl font-bold text-slate-900">
                {ear.ear_percentual}%
              </div>
              <div className="w-full bg-slate-100 rounded-full h-2 mt-2">
                <div
                  className={`h-2 rounded-full ${ear.ear_percentual > 60 ? 'bg-emerald-500' : ear.ear_percentual > 40 ? 'bg-blue-500' : 'bg-amber-500'}`}
                  style={{ width: `${ear.ear_percentual}%` }}
                ></div>
              </div>
              <div className="flex justify-between text-[11px] text-slate-500 mt-2">
                <span>Atual: {ear.ear_atual_mwmes.toLocaleString()} MWmês</span>
                <span>Meta: {ear.meta_seguranca_percentual}%</span>
              </div>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-8 bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
          <h3 className="text-sm font-bold text-slate-900 mb-1">Evolução do Nível de Armazenamento (EAR % por Mês)</h3>
          <p className="text-xs text-slate-500 mb-4">Comportamento sazonal dos reservatórios nos subsistemas</p>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={ear_historico} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                <defs>
                  <linearGradient id="colorSE" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#2563EB" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#2563EB" stopOpacity={0}/>
                  </linearGradient>
                  <linearGradient id="colorS" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10B981" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#10B981" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="mes" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} domain={[40, 100]} />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#fff', fontSize: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Area type="monotone" dataKey="SE_CO" name="Sudeste/CO" stroke="#2563EB" strokeWidth={2} fillOpacity={1} fill="url(#colorSE)" />
                <Area type="monotone" dataKey="S" name="Sul" stroke="#10B981" strokeWidth={2} fillOpacity={1} fill="url(#colorS)" />
                <Line type="monotone" dataKey="NE" name="Nordeste" stroke="#F59E0B" strokeWidth={2} dot={false} />
                <Line type="monotone" dataKey="N" name="Norte" stroke="#8B5CF6" strokeWidth={2} dot={false} />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="lg:col-span-4 bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm flex flex-col justify-between">
          <div>
            <div className="flex items-center space-x-2 mb-3 border-b border-slate-100 pb-2">
              <Droplets className="w-4 h-4 text-blue-600" />
              <h3 className="text-sm font-bold text-slate-900">Afluência (ENA % MLT)</h3>
            </div>
            <p className="text-xs text-slate-500 mb-3">
              Volume de água que chega aos reservatórios em relação à Média de Longo Termo (MLT).
            </p>

            <div className="space-y-3 text-xs">
              {ena_subsistemas.map((ena: any) => (
                <div key={ena.subsistema} className="p-2.5 rounded-lg border border-slate-100 bg-slate-50">
                  <div className="flex justify-between font-bold text-slate-800">
                    <span>{ena.subsistema}</span>
                    <span className={ena.ena_percentual_mlt >= 100 ? 'text-emerald-700' : 'text-amber-700'}>
                      {ena.ena_percentual_mlt}% MLT
                    </span>
                  </div>
                  <div className="flex justify-between text-[11px] text-slate-500 mt-1">
                    <span>{ena.ena_mwmed.toLocaleString()} MWméd</span>
                    <span className="font-medium">{ena.classificacao}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="mt-3 text-[11px] text-slate-400 bg-slate-50 p-2 rounded">
            ENA abaixo de 80% MLT no Nordeste exige acionamento de usinas térmicas fora da ordem de mérito.
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-6 bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
          <div className="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
            <div className="flex items-center space-x-2">
              <Flame className="w-4 h-4 text-amber-600" />
              <h3 className="text-sm font-bold text-slate-900">CMO por Patamar de Carga (R$/MWh)</h3>
            </div>
            <span className="text-[11px] text-slate-500">Custo do próximo MWh</span>
          </div>

          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={cmo_atual} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="subsistema" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#fff', fontSize: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Bar dataKey="patamar_leve" name="Leve" fill="#93C5FD" radius={[4, 4, 0, 0]} />
                <Bar dataKey="patamar_medio" name="Média" fill="#3B82F6" radius={[4, 4, 0, 0]} />
                <Bar dataKey="patamar_pesado" name="Pesada" fill="#1E40AF" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="lg:col-span-6 bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
          <div className="flex items-center justify-between mb-3 border-b border-slate-100 pb-2">
            <div className="flex items-center space-x-2">
              <BarChart2 className="w-4 h-4 text-indigo-600" />
              <h3 className="text-sm font-bold text-slate-900">Tendência Semanal do CMO</h3>
            </div>
            <span className="text-[11px] text-slate-500">Agosto/2026</span>
          </div>

          <div className="h-56">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={cmo_historico} margin={{ top: 10, right: 10, left: -10, bottom: 0 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
                <XAxis dataKey="data" stroke="#64748b" fontSize={11} />
                <YAxis stroke="#64748b" fontSize={11} domain={[55, 85]} />
                <Tooltip contentStyle={{ backgroundColor: '#1e293b', border: 'none', borderRadius: '8px', color: '#fff', fontSize: '12px' }} />
                <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                <Line type="monotone" dataKey="SE_CO" name="SE/CO" stroke="#2563EB" strokeWidth={2} />
                <Line type="monotone" dataKey="S" name="Sul" stroke="#10B981" strokeWidth={2} />
                <Line type="monotone" dataKey="NE" name="Nordeste" stroke="#F59E0B" strokeWidth={2} />
                <Line type="monotone" dataKey="N" name="Norte" stroke="#8B5CF6" strokeWidth={2} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};
