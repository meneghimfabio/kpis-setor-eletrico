import React from 'react';
import { Badge } from './Badge';

interface StatCardProps {
  title: string;
  value: string | number;
  unit?: string;
  statusText?: string;
  statusVariant?: 'sucesso' | 'alerta' | 'critico' | 'info' | 'neutro';
  subtitle?: string;
  icon?: React.ReactNode;
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  unit,
  statusText,
  statusVariant = 'neutro',
  subtitle,
  icon
}) => {
  return (
    <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm hover:shadow transition-shadow">
      <div className="flex items-center justify-between text-slate-500 mb-2">
        <span className="text-xs font-semibold uppercase tracking-wider">{title}</span>
        {icon && <div className="text-slate-400">{icon}</div>}
      </div>
      <div className="flex items-baseline space-x-2">
        <span className="text-2xl font-bold text-slate-900 tracking-tight">{value}</span>
        {unit && <span className="text-xs font-medium text-slate-500">{unit}</span>}
      </div>
      {(statusText || subtitle) && (
        <div className="mt-3 flex items-center justify-between text-xs pt-2 border-t border-slate-100">
          {subtitle && <span className="text-slate-500">{subtitle}</span>}
          {statusText && <Badge variant={statusVariant}>{statusText}</Badge>}
        </div>
      )}
    </div>
  );
};
