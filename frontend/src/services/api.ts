import type { ProretInput, ProretResult } from '../types';

const API_BASE = '/api/v1';

async function fetchJson<T>(url: string): Promise<T> {
  const res = await fetch(`${API_BASE}${url}`);
  if (!res.ok) {
    throw new Error(`Erro na API (${res.status}): ${res.statusText}`);
  }
  return res.json();
}

export const apiService = {
  getExecutiveSummary: (subsystem: string = 'SIN') => fetchJson<any>(`/executive/summary?subsystem=${subsystem}`),
  getSinOverview: () => fetchJson<any>('/sin/overview'),
  getCceeOverview: () => fetchJson<any>('/ccee/overview'),
  getTransmissaoOverview: () => fetchJson<any>('/transmissao/overview'),
  getDistribuicaoOverview: () => fetchJson<any>('/distribuicao/overview'),
  getPerdasMmgdOverview: () => fetchJson<any>('/perdas-mmgd/overview'),
  getAtendimentoOverview: () => fetchJson<any>('/atendimento/overview'),
  getFinanceiroOverview: () => fetchJson<any>('/financeiro-proret/overview'),
  getAlerts: () => fetchJson<any>('/alerts/'),
  
  simulateProret: async (params: ProretInput): Promise<ProretResult> => {
    const res = await fetch(`${API_BASE}/financeiro-proret/simulate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params),
    });
    if (!res.ok) {
      throw new Error(`Erro na simulação PRORET: ${res.statusText}`);
    }
    return res.json();
  },

  triggerSinIngestion: async (years: number[] = [2025, 2026]) => {
    const res = await fetch(`${API_BASE}/ingestion/sin/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ years, async_mode: false }),
    });
    if (!res.ok) {
      throw new Error(`Erro ao disparar ingestão ONS: ${res.statusText}`);
    }
    return res.json();
  },

  getSinIngestionStatus: () => fetchJson<any>('/ingestion/sin/status'),

  triggerCceeIngestion: async () => {
    const res = await fetch(`${API_BASE}/ingestion/ccee/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) {
      throw new Error(`Erro ao disparar ingestão CCEE: ${res.statusText}`);
    }
    return res.json();
  },

  getCceeIngestionStatus: () => fetchJson<any>('/ingestion/ccee/status'),

  triggerDistribuicaoIngestion: async () => {
    const res = await fetch(`${API_BASE}/ingestion/distribuicao/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) {
      throw new Error(`Erro ao disparar ingestão ANEEL PRODIST: ${res.statusText}`);
    }
    return res.json();
  },

  getDistribuicaoIngestionStatus: () => fetchJson<any>('/ingestion/distribuicao/status'),

  triggerPerdasMmgdIngestion: async () => {
    const res = await fetch(`${API_BASE}/ingestion/perdas-mmgd/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
    });
    if (!res.ok) {
      throw new Error(`Erro ao disparar ingestão ANEEL Perdas & MMGD: ${res.statusText}`);
    }
    return res.json();
  },

  getPerdasMmgdIngestionStatus: () => fetchJson<any>('/ingestion/perdas-mmgd/status'),
};
