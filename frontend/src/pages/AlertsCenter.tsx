import React, { useEffect, useState } from 'react';
import { apiService } from '../services/api';
import { Badge } from '../components/common/Badge';
import { AlertOctagon, Filter } from 'lucide-react';

export const AlertsCenter: React.FC = () => {
  const [alerts, setAlerts] = useState<any[]>([]);
  const [filter, setFilter] = useState<string>('todos');

  useEffect(() => {
    apiService.getAlerts()
      .then(res => setAlerts(res.alertas || []))
      .catch(err => console.error(err));
  }, []);

  const filteredAlerts = alerts.filter(a => {
    if (filter === 'todos') return true;
    return a.nivel === filter;
  });

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div className="flex items-center space-x-2">
            <span className="p-2 bg-rose-50 text-rose-700 rounded-lg">
              <AlertOctagon className="w-5 h-5" />
            </span>
            <div>
              <h2 className="text-lg font-bold text-slate-900">Centro de Alertas & Semáforo Regulatório</h2>
              <p className="text-xs text-slate-500">
                Monitoramento de inconformidades, limites ultrapassados de DEC/FEC, risco hidrológico (GSF), perdas e curtailment
              </p>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <Filter className="w-4 h-4 text-slate-400" />
            <div className="flex bg-slate-100 p-1 rounded-lg border border-slate-200 text-xs">
              {['todos', 'critico', 'alerta', 'info'].map((f) => (
                <button
                  key={f}
                  onClick={() => setFilter(f)}
                  className={`px-3 py-1 rounded-md font-semibold capitalize transition-colors ${
                    filter === f
                      ? 'bg-white text-blue-700 shadow-sm'
                      : 'text-slate-600 hover:text-slate-900'
                  }`}
                >
                  {f === 'todos' ? 'Todos' : f === 'critico' ? 'Críticos' : f === 'alerta' ? 'Alertas' : 'Informativos'}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>

      <div className="space-y-3">
        {filteredAlerts.map((alt) => (
          <div
            key={alt.id}
            className={`p-5 rounded-xl border transition-all ${
              alt.nivel === 'critico'
                ? 'bg-rose-50/50 border-rose-200 shadow-sm'
                : alt.nivel === 'alerta'
                ? 'bg-amber-50/50 border-amber-200 shadow-sm'
                : 'bg-blue-50/50 border-blue-200 shadow-sm'
            }`}
          >
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-2 mb-2">
              <div className="flex items-center space-x-2">
                <Badge variant={alt.nivel === 'critico' ? 'critico' : alt.nivel === 'alerta' ? 'alerta' : 'info'}>
                  {alt.nivel.toUpperCase()}
                </Badge>
                <span className="text-xs font-bold text-slate-600">[{alt.modulo}]</span>
                <span className="text-sm font-bold text-slate-900">{alt.titulo}</span>
              </div>
              <span className="text-xs text-slate-500 font-mono">{alt.data_evento} • ID: {alt.id}</span>
            </div>
            <p className="text-xs text-slate-700 leading-relaxed pl-1">
              {alt.descricao}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
};
