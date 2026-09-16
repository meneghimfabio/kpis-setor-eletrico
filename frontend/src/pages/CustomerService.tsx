import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';
import { StatCard } from '../components/common/StatCard';
import { Badge } from '../components/common/Badge';
import { Headphones, Award, PhoneCall, Clock, AlertCircle, CheckCircle2, Layers } from 'lucide-react';

export const CustomerService: React.FC = () => {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    apiService.getAtendimentoOverview()
      .then(res => setData(res))
      .catch(err => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  if (loading || !data) {
    return (
      <div className="p-8 flex items-center justify-center min-h-[400px]">
        <div className="text-sm font-semibold text-slate-500 animate-pulse">Carregando dados de Atendimento Comercial...</div>
      </div>
    );
  }

  const {
    canais_atendimento,
    slas_comerciais,
    ouvidoria_aneel,
    ranking_iasc = [],
    ultima_atualizacao_aneel,
    _metadata
  } = data;

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="p-2 bg-emerald-50 text-emerald-700 rounded-lg">
              <Headphones className="w-5 h-5" />
            </span>
            <div>
              <h2 className="text-lg font-bold text-slate-900">Atendimento Comercial & Satisfação do Consumidor</h2>
              <p className="text-xs text-slate-500">
                Índice ANEEL de Satisfação (IASC), Níveis de Serviço em Call Center (INS/IAb), SLAs Comerciais e Ouvidoria Nível 2
              </p>
            </div>
          </div>
          <div className="flex items-center space-x-3">
            <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 flex items-center gap-1.5">
              <CheckCircle2 className="w-3.5 h-3.5" />
              {ultima_atualizacao_aneel || 'Fonte: ANEEL Ouvidoria / BigQuery Gold'}
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
          title="Nível de Serviço Call Center (INS)"
          value={`${canais_atendimento.ins_medio_nacional_pct}%`}
          statusText="Meta > 85%"
          statusVariant="sucesso"
          subtitle="Chamadas atendidas no prazo"
          icon={<PhoneCall className="w-4 h-4 text-blue-600" />}
        />
        <StatCard
          title="Índice de Abandono (IAb)"
          value={`${canais_atendimento.iab_medio_nacional_pct}%`}
          statusText="Meta < 5%"
          statusVariant="sucesso"
          subtitle="Desistências na fila telefônica"
          icon={<AlertCircle className="w-4 h-4 text-amber-600" />}
        />
        <StatCard
          title="Tempo Médio de Atendimento (TMA)"
          value={`${canais_atendimento.tma_medio_segundos} s`}
          statusText="Eficiência Operacional"
          statusVariant="info"
          subtitle="Duração média das chamadas"
          icon={<Clock className="w-4 h-4 text-indigo-600" />}
        />
        <StatCard
          title="Prêmio IASC Destaque"
          value="CPFL Santa Cruz"
          statusText="Score: 83.4"
          statusVariant="sucesso"
          subtitle="Pesquisa anual de satisfação"
          icon={<Award className="w-4 h-4 text-amber-500" />}
        />
      </div>

      {/* ANEEL REAL IASC & OUVIDORIA NÍVEL 2 RANKING - BIGQUERY GOLD */}
      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3 mb-4">
          <div className="flex items-center space-x-2">
            <span className="p-1.5 bg-amber-50 text-amber-700 rounded-lg">
              <Award className="w-4 h-4" />
            </span>
            <div>
              <div className="flex items-center gap-2">
                <h3 className="text-sm font-bold text-slate-900">
                  Ranking Oficial de Satisfação (IASC) & Ouvidoria ANEEL Nível 2
                </h3>
                <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-100 text-amber-800">
                  Dados Reais BigQuery Gold
                </span>
              </div>
              <p className="text-xs text-slate-500">
                Índice ANEEL de Satisfação do Consumidor e volume de reclamações escaladas para a Ouvidoria Setorial Regulamentar
              </p>
            </div>
          </div>
          <span className="text-[11px] font-medium text-slate-500">
            {ranking_iasc.length} Concessionárias Ranqueadas
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs">
            <thead>
              <tr className="border-b border-slate-200 text-slate-500 uppercase font-bold text-[10px]">
                <th className="py-2.5 px-3"># Posição</th>
                <th className="py-2.5 px-3">Distribuidora</th>
                <th className="py-2.5 px-3">Porte</th>
                <th className="py-2.5 px-3">Score IASC (/100)</th>
                <th className="py-2.5 px-3 text-right">Reclamações Ouvidoria Nível 2</th>
                <th className="py-2.5 px-3 text-right">Procedência ANEEL</th>
                <th className="py-2.5 px-3 text-right">Tempo Resolução</th>
                <th className="py-2.5 px-3 text-right">Avaliação ANEEL</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {ranking_iasc.map((item: any, idx: number) => {
                const pos = item.posicao || (idx + 1);
                const score = item.score || 0;
                return (
                  <tr key={idx} className="hover:bg-slate-50/80 transition">
                    <td className="py-3 px-3 font-bold text-slate-700">
                      {pos <= 3 ? (
                        <span className="inline-flex items-center justify-center w-5 h-5 rounded-full bg-amber-100 text-amber-800 text-[10px] font-extrabold">
                          {pos}º
                        </span>
                      ) : (
                        <span className="text-slate-400">{pos}º</span>
                      )}
                    </td>
                    <td className="py-3 px-3 font-bold text-slate-800">
                      <div>{item.nome_exibicao || item.distribuidora}</div>
                      <div className="text-[10px] text-slate-400">{item.distribuidora}</div>
                    </td>
                    <td className="py-3 px-3 text-slate-600">
                      <span className="px-2 py-0.5 rounded text-[10px] font-medium bg-slate-100 text-slate-700">
                        {item.porte || 'Grande'}
                      </span>
                    </td>
                    <td className="py-3 px-3">
                      <div className="flex items-center space-x-2">
                        <span className="font-bold text-slate-900 w-8">{score}</span>
                        <div className="w-24 h-2 bg-slate-100 rounded-full overflow-hidden">
                          <div
                            style={{ width: `${Math.min(100, score)}%` }}
                            className={`h-full ${
                              score >= 80 ? 'bg-emerald-500' : score >= 70 ? 'bg-blue-500' : 'bg-amber-500'
                            }`}
                          ></div>
                        </div>
                      </div>
                    </td>
                    <td className="py-3 px-3 text-right font-medium text-slate-800">
                      {item.total_reclamacoes ? item.total_reclamacoes.toLocaleString() : '-'}
                    </td>
                    <td className="py-3 px-3 text-right font-semibold">
                      <span className={item.procedencia_pct > 20 ? 'text-rose-600' : 'text-slate-700'}>
                        {item.procedencia_pct ? `${item.procedencia_pct}%` : '-'}
                      </span>
                    </td>
                    <td className="py-3 px-3 text-right text-slate-600">
                      {item.tempo_medio_resolucao_dias ? `${item.tempo_medio_resolucao_dias} dias` : '-'}
                    </td>
                    <td className="py-3 px-3 text-right">
                      <Badge
                        variant={
                          item.classificacao_satisfacao?.includes('Excelente') || score >= 80
                            ? 'sucesso'
                            : item.classificacao_satisfacao?.includes('Crítico')
                            ? 'critico'
                            : 'alerta'
                        }
                      >
                        {item.classificacao_satisfacao || 'Conforme'}
                      </Badge>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>

        <div className="mt-3 flex items-center justify-between text-[11px] text-slate-400 border-t border-slate-100 pt-2">
          <span>Fonte: Pesquisa Anual IASC e Ouvidoria Setorial ANEEL</span>
          <span className="flex items-center gap-1 text-blue-600 font-medium">
            <Layers className="w-3.5 h-3.5" /> Pipeline Medallion: GCS Bronze ➔ BigQuery Silver ➔ BigQuery Gold
          </span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        <div className="lg:col-span-6 bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
          <div className="flex items-center space-x-2 mb-3 border-b border-slate-100 pb-2">
            <Clock className="w-4 h-4 text-blue-600" />
            <h3 className="text-sm font-bold text-slate-900">Cumprimento de Prazos Comerciais (SLAs ANEEL)</h3>
          </div>

          <div className="space-y-3 text-xs">
            {slas_comerciais.map((sla: any, idx: number) => (
              <div key={idx} className="p-3 rounded-lg border border-slate-200 bg-slate-50">
                <div className="flex justify-between font-bold text-slate-800">
                  <span>{sla.servico}</span>
                  <Badge variant="sucesso">{sla.cumprimento_pct}% no prazo</Badge>
                </div>
                <div className="flex justify-between text-[11px] text-slate-500 mt-2">
                  <span>SLA Regulatório: {sla.sla_aneel_dias ? `${sla.sla_aneel_dias} dias` : `${sla.sla_aneel_horas} horas`}</span>
                  <span>Tempo Médio Real: {sla.tempo_medio_dias ? `${sla.tempo_medio_dias} dias` : `${sla.tempo_medio_horas} horas`}</span>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="lg:col-span-6 bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
          <div className="flex items-center space-x-2 mb-3 border-b border-slate-100 pb-2">
            <AlertCircle className="w-4 h-4 text-rose-600" />
            <h3 className="text-sm font-bold text-slate-900">Escalações para a Ouvidoria Setorial ANEEL</h3>
          </div>

          <div className="space-y-3 text-xs">
            {ouvidoria_aneel.map((ouv: any, idx: number) => (
              <div key={idx} className="p-3 rounded-lg border border-slate-200 bg-slate-50">
                <div className="flex justify-between font-bold text-slate-800">
                  <span>{ouv.tipologia}</span>
                  <span className="text-rose-600 font-bold">{ouv.pct_total}%</span>
                </div>
                <div className="flex justify-between text-[11px] text-slate-500 mt-1">
                  <span>Volume: {ouv.reclamacoes_mes.toLocaleString()} / mês</span>
                  <span>Tempo de Resolução: {ouv.tempo_resolucao_dias} dias</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
};
