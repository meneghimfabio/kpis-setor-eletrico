import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';
import { StatCard } from '../components/common/StatCard';
import { Badge } from '../components/common/Badge';
import { Radio, AlertOctagon, ShieldCheck, Zap } from 'lucide-react';

export const Transmission: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiService.getTransmissaoOverview()
      .then(res => setData(res))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading || !data) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[400px]">
        <div className="text-sm font-semibold text-slate-500 animate-pulse">Carregando dados de Transmissão...</div>
      </div>
    );
  }

  const { kpis_resumo, concessionarias, desligamentos_recentes } = data;

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="p-2 bg-blue-50 text-blue-700 rounded-lg">
              <Radio className="w-5 h-5" />
            </span>
            <div>
              <h2 className="text-lg font-bold text-slate-900">Transmissão: Disponibilidade, RAP e Deduções de PVd</h2>
              <p className="text-xs text-slate-500">
                Receita Anual Permitida (RAP), Parcela Variável por Indisponibilidade (PVd) e Energia Não Suprida (ENS)
              </p>
            </div>
          </div>
          <span className="px-3 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-800">
            Fonte: ANEEL / ONS / BigQuery
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <StatCard
          title="RAP Total Nacional"
          value={`R$ ${(kpis_resumo.rap_total_nacional_rs_mm / 1000).toFixed(1)} B`}
          statusText="Contratada"
          statusVariant="sucesso"
          subtitle="Ciclo Tarifário 2026/2027"
          icon={<Radio className="w-4 h-4 text-blue-600" />}
        />
        <StatCard
          title="Deduções de PVd no Ano"
          value={`R$ ${kpis_resumo.pvd_total_ano_rs_mm} MM`}
          statusText="0.56% da RAP"
          statusVariant="sucesso"
          subtitle="Penalidades por Indisponibilidade"
          icon={<AlertOctagon className="w-4 h-4 text-amber-600" />}
        />
        <StatCard
          title="Disponibilidade de Linhas"
          value={`${kpis_resumo.disponibilidade_media_linhas_pct}%`}
          statusText="Alta Confiabilidade"
          statusVariant="sucesso"
          subtitle="Rede Básica do SIN"
          icon={<ShieldCheck className="w-4 h-4 text-emerald-600" />}
        />
        <StatCard
          title="Energia Não Suprida (ENS)"
          value={`${kpis_resumo.ens_total_mwh} MWh`}
          statusText="Dentro do Limite"
          statusVariant="sucesso"
          subtitle="Interrupções na Rede Básica"
          icon={<Zap className="w-4 h-4 text-indigo-600" />}
        />
      </div>

      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <h3 className="text-sm font-bold text-slate-900 mb-1">Desempenho das Principais Transmissoras</h3>
        <p className="text-xs text-slate-500 mb-4">Acompanhamento de RAP homologada vs Deduções de PVd e Confiabilidade</p>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500 uppercase font-bold text-[10px]">
                <th className="py-2.5 px-3">Transmissora</th>
                <th className="py-2.5 px-3">RAP Homologada</th>
                <th className="py-2.5 px-3">Dedução PVd</th>
                <th className="py-2.5 px-3">Disponibilidade</th>
                <th className="py-2.5 px-3">ENS (MWh)</th>
                <th className="py-2.5 px-3 text-right">Avaliação</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {concessionarias.map((c: any, idx: number) => (
                <tr key={idx} className="hover:bg-slate-50">
                  <td className="py-3 px-3 font-bold text-slate-800">{c.nome}</td>
                  <td className="py-3 px-3 font-semibold text-slate-900">R$ {c.rap_homologada_rs_mm.toLocaleString()} MM</td>
                  <td className="py-3 px-3 text-rose-600 font-semibold">R$ {c.pvd_rs_mm.toFixed(1)} MM</td>
                  <td className="py-3 px-3 font-semibold text-emerald-700">{c.disponibilidade_pct}%</td>
                  <td className="py-3 px-3 text-slate-600">{c.ens_mwh} MWh</td>
                  <td className="py-3 px-3 text-right">
                    <Badge variant={c.status === 'Excelente' ? 'sucesso' : c.status === 'Conforme' ? 'info' : 'alerta'}>
                      {c.status}
                    </Badge>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <h3 className="text-sm font-bold text-slate-900 mb-1">Registro Recente de Desligamentos Intempestivos e PVd</h3>
        <p className="text-xs text-slate-500 mb-4">Eventos que impactaram a remuneração das transmissoras</p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          {desligamentos_recentes.map((d: any, idx: number) => (
            <div key={idx} className="p-3.5 rounded-lg border border-slate-200 bg-slate-50">
              <div className="flex justify-between font-bold text-slate-800 mb-1">
                <span>{d.concessionaria}</span>
                <span className="text-[10px] text-slate-500">{d.data}</span>
              </div>
              <div className="font-semibold text-slate-900 mt-1">{d.ativo}</div>
              <div className="mt-2 pt-2 border-t border-slate-200 flex justify-between text-[11px]">
                <span className="text-slate-500">Duração: {d.duracao_h}h ({d.causa})</span>
                <span className="text-rose-600 font-bold">PVd: R$ {d.pvd_rs_mil}k</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
