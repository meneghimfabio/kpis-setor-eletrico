import React from 'react';

interface BadgeProps {
  variant?: 'sucesso' | 'alerta' | 'critico' | 'info' | 'neutro';
  children: React.ReactNode;
  className?: string;
}

export const Badge: React.FC<BadgeProps> = ({ variant = 'neutro', children, className = '' }) => {
  const styles = {
    sucesso: 'bg-emerald-50 text-emerald-700 border-emerald-200',
    alerta: 'bg-amber-50 text-amber-700 border-amber-200',
    critico: 'bg-rose-50 text-rose-700 border-rose-200',
    info: 'bg-blue-50 text-blue-700 border-blue-200',
    neutro: 'bg-slate-100 text-slate-700 border-slate-200',
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${styles[variant]} ${className}`}>
      {children}
    </span>
  );
};
