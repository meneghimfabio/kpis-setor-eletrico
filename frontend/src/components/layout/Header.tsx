import React from 'react';
import { Database, RefreshCw, Zap } from 'lucide-react';
import type { SubsystemId } from '../../types';

interface HeaderProps {
  selectedSubsystem: SubsystemId;
  onSelectSubsystem: (sub: SubsystemId) => void;
  onRefresh: () => void;
  isRefreshing?: boolean;
}

export const Header: React.FC<HeaderProps> = ({
  selectedSubsystem,
  onSelectSubsystem,
  onRefresh,
  isRefreshing = false
}) => {
  return (
    <header className="bg-white border-b border-slate-200 sticky top-0 z-30 px-6 py-3.5">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
        {/* Title and GCP BigQuery indicator */}
        <div className="flex items-center space-x-3">
          <div className="p-2 bg-blue-700 text-white rounded-lg shadow-sm">
            <Zap className="w-5 h-5" />
          </div>
          <div>
            <div className="flex items-center space-x-2">
              <h1 className="text-lg font-bold text-slate-900 tracking-tight">Painel do Setor Elétrico Brasileiro</h1>
              <span className="px-2 py-0.5 text-[10px] font-bold rounded bg-slate-100 text-slate-700 border border-slate-200">
                v1.0
              </span>
            </div>
            <div className="flex flex-wrap items-center gap-2 text-xs text-slate-500 mt-0.5">
              <span className="flex items-center text-emerald-700 font-medium bg-emerald-50 px-2 py-0.5 rounded border border-emerald-200">
                <Database className="w-3.5 h-3.5 mr-1 text-emerald-600" />
                BigQuery: <code className="ml-1 text-slate-800 font-semibold">kpisetoreletrico</code>
              </span>
              <span className="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-semibold bg-blue-50 text-blue-700 border border-blue-200">
                <span className="w-1.5 h-1.5 rounded-full bg-blue-500 animate-pulse mr-1.5"></span>
                Lakehouse ANEEL: Bronze (GCS) • Silver • Gold (BI Engine)
              </span>
            </div>
          </div>
        </div>

        {/* Global Controls: Subsystem Filter & Refresh */}
        <div className="flex items-center space-x-3">
          <div className="flex items-center bg-slate-100 p-1 rounded-lg border border-slate-200 text-xs">
            {(['SIN', 'SE_CO', 'S', 'NE', 'N'] as SubsystemId[]).map((sub) => (
              <button
                key={sub}
                onClick={() => onSelectSubsystem(sub)}
                className={`px-3 py-1 rounded-md font-semibold transition-colors ${
                  selectedSubsystem === sub
                    ? 'bg-white text-blue-700 shadow-sm'
                    : 'text-slate-600 hover:text-slate-900'
                }`}
              >
                {sub === 'SIN' ? 'Brasil (SIN)' : sub.replace('_', '/')}
              </button>
            ))}
          </div>

          <button
            onClick={onRefresh}
            disabled={isRefreshing}
            className="flex items-center space-x-1.5 px-3 py-1.5 text-xs font-semibold text-slate-700 bg-white border border-slate-200 rounded-lg hover:bg-slate-50 transition-colors shadow-sm disabled:opacity-50"
            title="Atualizar dados do BigQuery"
          >
            <RefreshCw className={`w-3.5 h-3.5 ${isRefreshing ? 'animate-spin text-blue-600' : ''}`} />
            <span>{isRefreshing ? 'Atualizando...' : 'Atualizar'}</span>
          </button>
        </div>
      </div>
    </header>
  );
};
