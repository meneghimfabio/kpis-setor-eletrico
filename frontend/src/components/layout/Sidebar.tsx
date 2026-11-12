import React from 'react';
import {
  LayoutDashboard,
  Activity,
  TrendingUp,
  Radio,
  Zap,
  Percent,
  Headphones,
  DollarSign,
  AlertOctagon,
  Sparkles,
  BookOpen
} from 'lucide-react';

export type TabKey =
  | 'executive'
  | 'sin'
  | 'ccee'
  | 'transmissao'
  | 'distribuicao'
  | 'perdas_mmgd'
  | 'atendimento'
  | 'financeiro_proret'
  | 'alerts'
  | 'project_story';

interface SidebarProps {
  activeTab: TabKey;
  onSelectTab: (tab: TabKey) => void;
  alertCount?: number;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, onSelectTab, alertCount = 5 }) => {
  const menuItems = [
    {
      key: 'executive' as TabKey,
      label: 'Visão Executiva (C-Level)',
      icon: LayoutDashboard,
      owner: 'CEO / COO / CFO'
    },
    {
      key: 'sin' as TabKey,
      label: 'Operação do SIN',
      icon: Activity,
      owner: 'COO / Operação'
    },
    {
      key: 'ccee' as TabKey,
      label: 'Mercado & CCEE',
      icon: TrendingUp,
      owner: 'CFO / Trading'
    },
    {
      key: 'transmissao' as TabKey,
      label: 'Transmissão & RAP',
      icon: Radio,
      owner: 'COO / CFO'
    },
    {
      key: 'distribuicao' as TabKey,
      label: 'Distribuição (PRODIST)',
      icon: Zap,
      owner: 'COO / Regulação'
    },
    {
      key: 'perdas_mmgd' as TabKey,
      label: 'Perdas & MMGD (GD)',
      icon: Percent,
      owner: 'COO / Comercial'
    },
    {
      key: 'atendimento' as TabKey,
      label: 'Atendimento & Ouvidoria',
      icon: Headphones,
      owner: 'COO / Clientes'
    },
    {
      key: 'financeiro_proret' as TabKey,
      label: 'Financeiro & PRORET',
      icon: DollarSign,
      owner: 'CEO / CFO / Tarifas'
    },
    {
      key: 'alerts' as TabKey,
      label: 'Centro de Alertas',
      icon: AlertOctagon,
      badge: alertCount,
      owner: 'Conformidade'
    },
  ];

  return (
    <aside className="w-64 bg-slate-900 text-slate-300 flex flex-col shrink-0 min-h-screen border-r border-slate-800">
      <div className="p-5 border-b border-slate-800 flex items-center space-x-3">
        <div className="w-8 h-8 rounded-lg bg-blue-600 flex items-center justify-center text-white font-black text-base shadow-md">
          ⚡
        </div>
        <div>
          <h2 className="text-sm font-bold text-white tracking-wide">PAINEL EXECUTIVO</h2>
          <p className="text-[11px] text-slate-400">Setor Elétrico Brasileiro</p>
        </div>
      </div>

      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <div className="px-3 pb-2 text-[10px] font-bold uppercase tracking-wider text-slate-400">
          Módulos Setoriais
        </div>

        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.key;
          return (
            <button
              key={item.key}
              onClick={() => onSelectTab(item.key)}
              className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-semibold transition-all ${
                isActive
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-300 hover:bg-slate-800 hover:text-white'
              }`}
            >
              <div className="flex items-center space-x-3 truncate">
                <Icon className={`w-4 h-4 shrink-0 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                <div className="text-left truncate">
                  <div className="truncate">{item.label}</div>
                  <div className={`text-[10px] font-normal ${isActive ? 'text-blue-200' : 'text-slate-500'}`}>
                    {item.owner}
                  </div>
                </div>
              </div>
              {item.badge !== undefined && (
                <span className={`px-1.5 py-0.5 rounded-full text-[10px] font-bold ${
                  isActive ? 'bg-white text-blue-700' : 'bg-rose-500/20 text-rose-300 border border-rose-500/30'
                }`}>
                  {item.badge}
                </span>
              )}
            </button>
          );
        })}

        {/* Módulo Especial de Apresentação & Case */}
        <div className="pt-3 pb-1">
          <div className="px-3 pb-2 text-[10px] font-bold uppercase tracking-wider text-amber-400 flex items-center justify-between">
            <span>Special Showcase</span>
            <span className="text-[9px] bg-amber-500/20 text-amber-300 px-1.5 py-0.5 rounded border border-amber-500/30 flex items-center gap-1 font-semibold">
              <Sparkles className="w-2.5 h-2.5" />
              Antigravity+Gemini
            </span>
          </div>
          <button
            onClick={() => onSelectTab('project_story')}
            className={`w-full flex items-center justify-between px-3 py-2.5 rounded-lg text-xs font-semibold transition-all border ${
              activeTab === 'project_story'
                ? 'bg-gradient-to-r from-blue-600 to-indigo-600 text-white shadow-md border-blue-400'
                : 'text-slate-300 hover:bg-slate-800/80 hover:text-white border-amber-500/20 bg-amber-500/5'
            }`}
          >
            <div className="flex items-center space-x-3 truncate">
              <BookOpen className={`w-4 h-4 shrink-0 ${activeTab === 'project_story' ? 'text-white' : 'text-amber-400'}`} />
              <div className="text-left truncate">
                <div className="truncate flex items-center gap-1.5 font-bold">
                  <span>📖 História & Arquitetura</span>
                </div>
                <div className={`text-[10px] font-normal ${activeTab === 'project_story' ? 'text-blue-200' : 'text-slate-400'}`}>
                  Fases, Stack & Antigravity+Gemini
                </div>
              </div>
            </div>
            <span className={`px-1.5 py-0.5 rounded-full text-[10px] font-bold ${
              activeTab === 'project_story' ? 'bg-white text-indigo-700' : 'bg-amber-500/20 text-amber-300 border border-amber-500/40'
            }`}>
              Showcase
            </span>
          </button>
        </div>
      </nav>

      <div className="p-4 border-t border-slate-800 text-[11px] text-slate-500 bg-slate-950/50">
        <div className="flex items-center justify-between font-semibold text-slate-400">
          <span>BigQuery GCP</span>
          <span className="text-emerald-400 flex items-center">● Online</span>
        </div>
        <div className="text-[10px] text-slate-500 mt-1">
          Projeto: <span className="text-slate-300">kpisetoreletrico</span>
        </div>
      </div>
    </aside>
  );
};
