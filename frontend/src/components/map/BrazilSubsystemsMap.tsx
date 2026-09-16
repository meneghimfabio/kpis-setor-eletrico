import React, { useState } from 'react';
import type { SubsystemId } from '../../types';

interface SubsystemData {
  id: SubsystemId;
  name: string;
  ear_pct: number;
  cmo: number;
  pld: number;
  peso_carga: number;
  status: string;
}

const SUBSYSTEM_INFO: Record<string, SubsystemData> = {
  SE_CO: { id: 'SE_CO', name: 'Sudeste / Centro-Oeste', ear_pct: 64.8, cmo: 68.42, pld: 68.42, peso_carga: 58, status: 'Favorável' },
  S: { id: 'S', name: 'Sul', ear_pct: 78.2, cmo: 65.10, pld: 65.10, peso_carga: 17, status: 'Favorável' },
  NE: { id: 'NE', name: 'Nordeste', ear_pct: 56.4, cmo: 74.90, pld: 74.90, peso_carga: 18, status: 'Atenção Moderada' },
  N: { id: 'N', name: 'Norte', ear_pct: 82.5, cmo: 63.80, pld: 63.80, peso_carga: 7, status: 'Favorável' }
};

interface BrazilMapProps {
  selectedSubsystem?: SubsystemId;
  onSelectSubsystem?: (id: SubsystemId) => void;
}

export const BrazilSubsystemsMap: React.FC<BrazilMapProps> = ({
  selectedSubsystem,
  onSelectSubsystem
}) => {
  const [hovered, setHovered] = useState<SubsystemId | null>(null);

  const activeId = hovered || selectedSubsystem || 'SE_CO';
  const activeData = SUBSYSTEM_INFO[activeId] || SUBSYSTEM_INFO.SE_CO;

  const getColor = (id: SubsystemId) => {
    const isSelected = selectedSubsystem === id;
    const isHovered = hovered === id;
    if (isSelected || isHovered) return '#2563EB';

    switch (id) {
      case 'SE_CO': return '#93C5FD';
      case 'S': return '#60A5FA';
      case 'NE': return '#FCD34D';
      case 'N': return '#86EFAC';
      default: return '#CBD5E1';
    }
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
      <div className="flex items-center justify-between mb-4 border-b border-slate-100 pb-3">
        <div>
          <h3 className="text-sm font-bold text-slate-800 uppercase tracking-wider">Topologia e Subsistemas do SIN</h3>
          <p className="text-xs text-slate-500">Passe o cursor ou clique para inspecionar métricas do subsistema</p>
        </div>
        <div className="flex items-center space-x-2 text-xs">
          <span className="flex items-center"><span className="w-2.5 h-2.5 rounded-full bg-blue-500 inline-block mr-1"></span> SE/CO</span>
          <span className="flex items-center"><span className="w-2.5 h-2.5 rounded-full bg-blue-400 inline-block mr-1"></span> Sul</span>
          <span className="flex items-center"><span className="w-2.5 h-2.5 rounded-full bg-amber-400 inline-block mr-1"></span> Nordeste</span>
          <span className="flex items-center"><span className="w-2.5 h-2.5 rounded-full bg-emerald-400 inline-block mr-1"></span> Norte</span>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
        <div className="lg:col-span-7 flex justify-center">
          <svg viewBox="0 0 500 500" className="w-full max-w-[380px] h-auto filter drop-shadow-sm">
            <path
              d="M 60,110 L 170,45 L 290,65 L 340,110 L 310,195 L 240,210 L 160,230 L 110,210 L 45,160 Z"
              fill={getColor('N')}
              stroke="#FFFFFF"
              strokeWidth="2.5"
              className="cursor-pointer transition-colors duration-200 hover:opacity-90"
              onMouseEnter={() => setHovered('N')}
              onMouseLeave={() => setHovered(null)}
              onClick={() => onSelectSubsystem && onSelectSubsystem('N')}
            />
            <text x="180" y="140" fill="#1E293B" fontSize="14" fontWeight="bold" pointerEvents="none">NORTE (N)</text>

            <path
              d="M 310,110 L 450,130 L 475,200 L 410,285 L 350,280 L 310,195 Z"
              fill={getColor('NE')}
              stroke="#FFFFFF"
              strokeWidth="2.5"
              className="cursor-pointer transition-colors duration-200 hover:opacity-90"
              onMouseEnter={() => setHovered('NE')}
              onMouseLeave={() => setHovered(null)}
              onClick={() => onSelectSubsystem && onSelectSubsystem('NE')}
            />
            <text x="365" y="200" fill="#1E293B" fontSize="14" fontWeight="bold" pointerEvents="none">NORDESTE (NE)</text>

            <path
              d="M 160,230 L 240,210 L 310,195 L 350,280 L 410,285 L 380,380 L 290,410 L 210,380 L 150,330 L 140,270 Z"
              fill={getColor('SE_CO')}
              stroke="#FFFFFF"
              strokeWidth="2.5"
              className="cursor-pointer transition-colors duration-200 hover:opacity-90"
              onMouseEnter={() => setHovered('SE_CO')}
              onMouseLeave={() => setHovered(null)}
              onClick={() => onSelectSubsystem && onSelectSubsystem('SE_CO')}
            />
            <text x="245" y="310" fill="#1E293B" fontSize="14" fontWeight="bold" pointerEvents="none">SE / CO</text>

            <path
              d="M 210,380 L 290,410 L 280,480 L 220,495 L 185,440 Z"
              fill={getColor('S')}
              stroke="#FFFFFF"
              strokeWidth="2.5"
              className="cursor-pointer transition-colors duration-200 hover:opacity-90"
              onMouseEnter={() => setHovered('S')}
              onMouseLeave={() => setHovered(null)}
              onClick={() => onSelectSubsystem && onSelectSubsystem('S')}
            />
            <text x="230" y="445" fill="#1E293B" fontSize="13" fontWeight="bold" pointerEvents="none">SUL (S)</text>

            <line x1="240" y1="210" x2="310" y2="195" stroke="#1E40AF" strokeWidth="2" strokeDasharray="4 3" />
            <line x1="310" y1="195" x2="350" y2="280" stroke="#1E40AF" strokeWidth="2" strokeDasharray="4 3" />
            <line x1="240" y1="210" x2="250" y2="300" stroke="#1E40AF" strokeWidth="2" strokeDasharray="4 3" />
            <line x1="250" y1="360" x2="245" y2="420" stroke="#1E40AF" strokeWidth="2" strokeDasharray="4 3" />
          </svg>
        </div>

        <div className="lg:col-span-5 bg-slate-50 border border-slate-200 rounded-lg p-4">
          <div className="flex items-center justify-between mb-3 border-b border-slate-200 pb-2">
            <div>
              <span className="text-xs uppercase text-slate-500 font-semibold">Subsistema Selecionado</span>
              <h4 className="text-base font-bold text-slate-900">{activeData.name}</h4>
            </div>
            <span className="px-2 py-0.5 text-xs font-semibold rounded bg-blue-100 text-blue-800">
              {activeData.peso_carga}% da Carga do SIN
            </span>
          </div>

          <div className="space-y-3 text-xs">
            <div className="flex items-center justify-between bg-white p-2 rounded border border-slate-200">
              <span className="text-slate-600 font-medium">Energia Armazenada (EAR):</span>
              <span className="text-slate-900 font-bold text-sm">{activeData.ear_pct}%</span>
            </div>
            <div className="flex items-center justify-between bg-white p-2 rounded border border-slate-200">
              <span className="text-slate-600 font-medium">Custo Marginal Operação (CMO):</span>
              <span className="text-slate-900 font-bold text-sm">R$ {activeData.cmo.toFixed(2)}/MWh</span>
            </div>
            <div className="flex items-center justify-between bg-white p-2 rounded border border-slate-200">
              <span className="text-slate-600 font-medium">Preço Liquidação Diferenças (PLD):</span>
              <span className="text-slate-900 font-bold text-sm">R$ {activeData.pld.toFixed(2)}/MWh</span>
            </div>
            <div className="flex items-center justify-between bg-white p-2 rounded border border-slate-200">
              <span className="text-slate-600 font-medium">Status Operativo:</span>
              <span className="font-semibold text-emerald-700">{activeData.status}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
