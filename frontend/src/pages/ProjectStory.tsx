import React, { useState, useEffect } from 'react';
import {
  Sparkles,
  Layers,
  Cpu,
  Database,
  Workflow,
  CheckCircle2,
  Coins,
  Download,
  ChevronRight,
  ChevronLeft,
  ShieldCheck,
  TrendingUp,
  Server,
  Maximize2,
  ExternalLink,
  BookOpen,
  Filter,
  CheckCircle,
  BarChart3,
  Calendar,
  Terminal,
  Table,
  LayoutGrid,
  Briefcase,
  Shield,
  Wrench,
  Users,
  Trophy
} from 'lucide-react';

import type { TabKey } from '../components/layout/Sidebar';

interface ProjectStoryProps {
  onNavigateTab?: (tab: TabKey) => void;
}

export type StoryPersona = 'all' | 'business' | 'cdo' | 'engineer';

export const ProjectStory: React.FC<ProjectStoryProps> = ({ onNavigateTab }) => {
  const [viewMode, setViewMode] = useState<'slides' | 'dossier'>('slides');
  const [currentSlide, setCurrentSlide] = useState(0);
  const [selectedPersona, setSelectedPersona] = useState<StoryPersona>('all');
  const [selectedSprintFilter, setSelectedSprintFilter] = useState<string>('all');
  const [activeSwimlane, setActiveSwimlane] = useState<number | null>(null);
  const [isDownloading, setIsDownloading] = useState(false);
  const [impactViewMode, setImpactViewMode] = useState<'table' | 'cards'>('table');

  const totalSlides = 9;

  // Atalhos de teclado para navegação de slides
  useEffect(() => {
    if (viewMode !== 'slides') return;

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'ArrowRight' || e.key === ' ') {
        e.preventDefault();
        setCurrentSlide((prev) => Math.min(prev + 1, totalSlides - 1));
      } else if (e.key === 'ArrowLeft') {
        e.preventDefault();
        setCurrentSlide((prev) => Math.max(prev - 1, 0));
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [viewMode, totalSlides]);

  // Função para baixar a apresentação HTML autônoma
  const handleDownloadStandaloneHtml = () => {
    setIsDownloading(true);
    setTimeout(() => {
      const link = document.createElement('a');
      link.href = '/apresentacao_historia_kpis.html';
      link.download = 'Apresentacao_Setor_Eletrico_Antigravity_Gemini.html';
      link.target = '_blank';
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      setIsDownloading(false);
    }, 600);
  };

  // Dados das Sprints do Projeto
  const sprintsData = [
    {
      id: 'fase-0',
      title: 'Fase 0: Gênese & Setup do Medallion Lakehouse',
      period: 'Setembro 2026',
      badge: 'Fundação',
      badgeColor: 'bg-blue-100 text-blue-800 border-blue-200',
      commitHash: 'a3d0f77',
      description: 'Engenharia reversa dos dados abertos regulatórios da ANEEL e estruturação das camadas Bronze (GCS) e Silver (BigQuery).',
      deliverables: [
        'Ingestor DEC/FEC PRODIST (Parquet oficial com 340 conjuntos)',
        'Ingestor MMGD SISGD (Lei 14.300 com conexões solares em 27 UFs)',
        'Ingestor de Tarifas Homologadas PRORET (103 concessionárias)',
        'Ingestor de Ouvidoria & Prêmio IASC (Reclamações Nível 2)',
        'Primeiro MVP com FastAPI + React 18 e BigQuery client resiliente'
      ],
      aiRole: 'O Data Cloud Tool Kit mapeou esquemas heterogêneos de 4 bases distintas da ANEEL, identificando partições e deduplicações idempotentes via MERGE sem semanas de discovery manual.'
    },
    {
      id: 'fase-1',
      title: 'Fase 1: Orquestração Serverless & Docker Cloud Run',
      period: 'Setembro 2026',
      badge: 'Infra & FinOps',
      badgeColor: 'bg-emerald-100 text-emerald-800 border-emerald-200',
      commitHash: '0faa69b • fab4a1d',
      description: 'Implementação da orquestração dual: Cloud Scheduler (Zero-Cost Serverless) e DAGs no Cloud Composer 3 / Apache Airflow.',
      deliverables: [
        'Setup de 10 Cron Jobs no Google Cloud Scheduler com autenticação OIDC',
        'DAGs completas em Python para Cloud Composer 3 / Airflow',
        'Docker multi-stage build (Node 22 para build Vite + Python 3.11 Uvicorn)',
        'Deploy no Cloud Run com política Scale-to-Zero (Custo base R$ 0,00)'
      ],
      aiRole: 'Antigravity gerou a matriz de agendamentos cron, os scripts de infraestrutura como código (IaC) e o Dockerfile multi-stage com balanceamento de memória otimizado.'
    },
    {
      id: 'sprint-1',
      title: 'Sprint 1: Alertas Analíticos, Hidrologia SIN & BCB SGS',
      period: 'Outubro 2026',
      badge: 'Live Data',
      badgeColor: 'bg-purple-100 text-purple-800 border-purple-200',
      commitHash: '292186e',
      description: 'Substituição completa de mocks por queries Gold analíticas em tempo real, integração com dados abertos ONS S3 e API do Banco Central.',
      deliverables: [
        'Eliminação de mocks ALT-001..ALT-005: Alertas gerados via query SQLX Gold',
        'Ingestão ao vivo da Hidrologia SIN via bucket ONS S3 (EAR %, ENA %, CMO)',
        'Ingestão dos índices macroeconômicos do BCB SGS (Selic 432 e IPCA 13522)',
        'Criação de novos modelos analíticos no BigQuery com aceleração BI Engine'
      ],
      aiRole: 'Data Cloud Tool Kit estruturou o parser resiliente para o bucket ONS S3 e a API REST do Banco Central com tratamento de timeouts e cache in-memory.'
    },
    {
      id: 'sprint-2',
      title: 'Sprint 2: Transmissão (RAP/PVd) & SLAs REN 1.000/2021',
      period: 'Outubro 2026',
      badge: 'Regulação',
      badgeColor: 'bg-amber-100 text-amber-800 border-amber-200',
      commitHash: '292186e',
      description: 'Mapeamento do segmento de Transmissão de Energia e auditoria de SLAs comerciais das distribuidoras conforme a Resolução Normativa ANEEL 1.000/2021.',
      deliverables: [
        'Ingestor CKAN ANEEL para Receita Anual Permitida (RAP) e Parcela Variável (PVd)',
        'Mapeamento de 176 concessionárias de transmissão e 160 mil km de linhas',
        'Métricas de conformidade comercial: Prazos de ligação nova, religação e vistorias',
        'Telas especializadas no Frontend com gráficos de dispersão e rankings'
      ],
      aiRole: 'Antigravity codificou a lógica regulatória da REN 1.000/2021 e construiu os testes automatizados garantindo conformidade matemática das metas homologadas.'
    },
    {
      id: 'sprint-3',
      title: 'Sprint 3: Mercado de Capitais CVM DFP/ITR (8 Companhias)',
      period: 'Outubro 2026',
      badge: 'Financeiro Auditado',
      badgeColor: 'bg-indigo-100 text-indigo-800 border-indigo-200',
      commitHash: '292186e',
      description: 'Conexão com os Dados Abertos da CVM para extrair demonstrativos financeiros auditados (DRE/Balanço Patrimonial) de gigantes do setor.',
      deliverables: [
        'Ingestor de demonstrativos contábeis CVM DFP e ITR via ZIP oficial',
        'Extração de Receita Líquida, EBITDA, Margem, Lucro Líquido e Dívida Líquida',
        'Cobertura de 8 companhias listadas (Eletrobras, CPFL, Neoenergia, Cemig, Copel, Equatorial, Engie e Energisa)',
        'Materialização no dataset Gold com partições por ano e trimestre'
      ],
      aiRole: 'A IA agêntica criou o parser de arquivos padronizados CVM e mapeou as contas contábeis do Plano de Contas Padrão (receita operacional, depreciação e endividamento).'
    },
    {
      id: 'fase-proret',
      title: 'Refinamento: Motor Matemático PRORET & Resiliência',
      period: 'Outubro 2026',
      badge: 'Simulação C-Level',
      badgeColor: 'bg-rose-100 text-rose-800 border-rose-200',
      commitHash: 'a64ead0',
      description: 'Modelagem do motor oficial de Revisão Tarifária Periódica (PRORET Submódulo 2.1) e robustecimento determinístico no frontend.',
      deliverables: [
        'Implementação da fórmula: Receita Requerida = [BRR × WACC] + OPEX - X ± Q',
        'Simulador interativo de faturas com decomposição Parcela A vs Parcela B',
        'Suíte de 34 testes automatizados 100% aprovados',
        'Fallback determinístico resiliente para garantir disponibilidade contínua'
      ],
      aiRole: 'Auditoria algorítmica pelo Antigravity da fórmula da ANEEL, garantindo cálculo exato de faturas e simulações de impacto financeiro em sub-segundo.'
    }
  ];

  // Mapa de Impacto da IA Agêntica (Jetski & Data Cloud Tool Kit)
  const aiImpactMap = [
    {
      id: 1,
      phaseNumber: '1',
      phase: '1. Concepção & Engenharia Reversa Regulatória',
      shortTitle: 'Engenharia Reversa Regulatória',
      badge: 'Discovery & Schemas',
      badgeColor: 'bg-blue-100 text-blue-800 border-blue-200',
      icon: Database,
      bullets: [
        'Engenharia reversa dos esquemas de dados abertos da ANEEL (PRODIST, SISGD, PRORET, Ouvidoria). Mapeamento de chaves colunares, tipos de dados e regras de negócio sem semanas de pesquisa manual.'
      ],
      deliverable: 'Mapeamento colunar de 4 bases oficiais sem semanas de pesquisa manual'
    },
    {
      id: 2,
      phaseNumber: '2',
      phase: '2. Arquitetura Medallion & FinOps Serverless Custo R$0',
      shortTitle: 'Medallion & FinOps R$ 0,00',
      badge: 'Arquitetura & FinOps',
      badgeColor: 'bg-emerald-100 text-emerald-800 border-emerald-200',
      icon: Coins,
      bullets: [
        'Desenho automático da topologia Bronze (GCS) ➔ Silver (BigQuery) ➔ Gold (BI Engine 2GB).',
        'Scripts de infraestrutura como código (IaC), políticas de Lifecycle e arquitetura Scale-to-Zero eliminando custos de clusters ociosos.'
      ],
      deliverable: 'Topologia Scale-to-Zero e BI Engine in-memory eliminando clusters ociosos'
    },
    {
      id: 3,
      phaseNumber: '3',
      phase: '3. Orquestração Dual (Scheduler vs Composer)',
      shortTitle: 'Orquestração Dual & Dataform',
      badge: 'Serverless vs Airflow',
      badgeColor: 'bg-purple-100 text-purple-800 border-purple-200',
      icon: Workflow,
      bullets: [
        'Geração dos 10 cron jobs serverless com OIDC no Cloud Scheduler.',
        'Criação simultânea de DAGs completas prontas para Cloud Composer 3.',
        'Pipelines analíticos em Dataform SQLX com assertions automáticas.'
      ],
      deliverable: '10 cron jobs serverless OIDC + DAGs Airflow + Dataform SQLX com assertions'
    },
    {
      id: 4,
      phaseNumber: '4',
      phase: '4. Sprints Ágeis de Dados Vivos',
      shortTitle: 'Sprints de Dados Vivos',
      badge: 'Live Data & APIs',
      badgeColor: 'bg-amber-100 text-amber-800 border-amber-200',
      icon: TrendingUp,
      bullets: [
        'Sprint 1: Integração live ONS S3 (hidrologia) e BCB SGS (Selic/IPCA).',
        'Sprint 2: Ingestão de Transmissão (RAP/PVd) e SLAs da REN 1.000/2021.',
        'Sprint 3: Parser de balanços auditados CVM DFP/ITR de 8 companhias.'
      ],
      deliverable: 'Unificação em tempo recorde de ONS S3, Banco Central, CKAN ANEEL e dados CVM'
    },
    {
      id: 5,
      phaseNumber: '5',
      phase: '5. Motor de Simulação Regulatório PRORET',
      shortTitle: 'Motor PRORET de Tarifas',
      badge: 'Algoritmo Regulatório',
      badgeColor: 'bg-rose-100 text-rose-800 border-rose-200',
      icon: Cpu,
      bullets: [
        'Tradução rigorosa da fórmula oficial da ANEEL de Revisão Tarifária para Python/TypeScript: Receita = [BRR × WACC] + OPEX - X ± Q.',
        'Implementação de fallbacks determinísticos e simulação paramétrica.'
      ],
      deliverable: 'Fórmula oficial da Receita Requerida com cálculo paramétrico em sub-segundo'
    },
    {
      id: 6,
      phaseNumber: '6',
      phase: '6. Engenharia de Qualidade & Self-Healing CI/CD',
      shortTitle: 'Qualidade & Self-Healing CI/CD',
      badge: '34 Testes Pass',
      badgeColor: 'bg-teal-100 text-teal-800 border-teal-200',
      icon: ShieldCheck,
      bullets: [
        'Construção e execução de 34 testes automatizados (100% aprovados).',
        'Diagnóstico autônomo de bugs de concorrência, tipos e resiliência.',
        'Docker multi-stage build (Node 22 + Python 3.11) para o Cloud Run.'
      ],
      deliverable: 'Suíte automatizada com 34 testes 100% aprovados e Docker multi-stage'
    },
    {
      id: 7,
      phaseNumber: '7',
      phase: '7. Executive Frontend Design System',
      shortTitle: 'Frontend Design System C-Level',
      badge: 'React 18 + Recharts',
      badgeColor: 'bg-indigo-100 text-indigo-800 border-indigo-200',
      icon: Server,
      bullets: [
        'Implementação do design system executivo (React 18 + TailwindCSS + Recharts), mapa vetorial do SIN e visões especializadas C-Level.'
      ],
      deliverable: 'Cockpit executivo integrado com 9 módulos, mapa vetorial do SIN e visualizações C-Level'
    }
  ];

  // Raias de Arquitetura Interativas
  const swimlanes = [
    {
      id: 1,
      title: '1. Fontes Externas Oficiais',
      color: 'border-blue-500 bg-blue-50/50',
      icon: Database,
      tag: 'Regulatório & Mercado',
      nodes: [
        { name: 'ANEEL (PRODIST, SISGD, PRORET, Ouvidoria)', desc: 'Bases colunares oficiais em Parquet e CSV (214 MB totais).' },
        { name: 'ONS (Hidrologia SIN & CMO)', desc: 'Bucket S3 de dados abertos com EAR, ENA, CMO e despacho térmico.' },
        { name: 'CCEE (Mercado & PLD)', desc: 'Preço horário, GSF, Curtailment e Bandeiras Tarifárias.' },
        { name: 'CVM & BCB (DFP/ITR & SGS)', desc: 'Balanços auditados de 8 empresas abertas + Selic e IPCA.' }
      ]
    },
    {
      id: 2,
      title: '2. Ingestão & Orquestração Dual',
      color: 'border-emerald-500 bg-emerald-50/50',
      icon: Workflow,
      tag: 'Serverless vs Enterprise',
      nodes: [
        { name: 'Cloud Scheduler (10 Cron Jobs)', desc: 'Orquestração ativa serverless com OIDC token sem custo de cluster (R$ 0,00).' },
        { name: 'Cloud Composer 3 / Airflow DAGs', desc: 'Opção enterprise corporativa com retries granulares e console visual.' },
        { name: 'Ingestores Python Otimizados', desc: 'Pipelines modulares com validação de esquema, deduplicação e MERGE.' }
      ]
    },
    {
      id: 3,
      title: '3. Data Lakehouse Medallion',
      color: 'border-purple-500 bg-purple-50/50',
      icon: Layers,
      tag: 'GCS + BigQuery',
      nodes: [
        { name: 'Bronze (Google Cloud Storage)', desc: 'Bucket gs://kpisetoreletrico-datalake-bronze com regras de Lifecycle.' },
        { name: 'Silver (BigQuery aneel_silver)', desc: 'Datasets particionados por data_referencia e clustered por concessionária/UF.' },
        { name: 'Gold (BigQuery gold_kpis)', desc: 'Tabelas analíticas agregadas com SLAs e indicadores consolidados.' },
        { name: 'BigQuery BI Engine (2 GB)', desc: 'Reserva in-memory na us-central1 entregando queries analíticas sub-200ms.' }
      ]
    },
    {
      id: 4,
      title: '4. Camada de Inteligência Agêntica (Antigravity+Gemini)',
      color: 'border-amber-500 bg-amber-50/50',
      icon: Sparkles,
      tag: 'Antigravity + Tool Kit',
      nodes: [
        { name: 'Antigravity Agentic Engine', desc: 'Raciocínio contínuo, geração de código, resolução de testes e self-healing.' },
        { name: 'Data Cloud Tool Kit', desc: 'Otimização de SQL BigQuery, Dataform SQLX, Knowledge Catalog e FinOps.' },
        { name: 'Motor PRORET de Tarifas', desc: 'Cálculo regulatório matemático da Receita Requerida com WACC e BRR.' }
      ]
    },
    {
      id: 5,
      title: '5. Serving, Frontend & Governança',
      color: 'border-indigo-500 bg-indigo-50/50',
      icon: Server,
      tag: 'Cloud Run & React SPA',
      nodes: [
        { name: 'Cloud Run (Serverless Scale-to-Zero)', desc: 'Instância multi-stage em produção com 1 vCPU e 1 GB RAM.' },
        { name: 'FastAPI Backend REST', desc: 'Rotas assíncronas documentadas no Swagger com metadados de procedência.' },
        { name: 'Frontend React 18 + Vite + Tailwind', desc: 'Cockpit executivo com 9 módulos, mapa do SIN e Recharts interativos.' },
        { name: '34 Testes Automatizados (100% Pass)', desc: 'Qualidade contínua validada em cada merge e sprint.' }
      ]
    }
  ];

  // Matriz comparativa de esforço
  const comparisonData = [
    {
      metric: 'Tempo Total de Construção',
      traditional: '4 a 6 meses de squad multidisciplinar',
      antigravity_gemini: 'Poucos dias de sprints agênticas iterativas',
      multiplier: '15x mais ágil',
      highlight: true
    },
    {
      metric: 'Custo Mensal de Infraestrutura',
      traditional: 'R$ 8.000+ / mês (Clusters 24/7 de VMs/Airflow)',
      antigravity_gemini: 'R$ 0,00 a R$ 5,00 / mês (Serverless Zero-Cost)',
      multiplier: 'Redução de 99,9%',
      highlight: true
    },
    {
      metric: 'Cobertura & Qualidade de Testes',
      traditional: 'Testes manuais ou parciais postergados',
      antigravity_gemini: '34 testes automatizados 100% aprovados gerados pela IA',
      multiplier: '100% de cobertura crítica',
      highlight: false
    },
    {
      metric: 'Integração de Fontes Regulatórias',
      traditional: 'Semana de análise de cada documentação ANEEL/ONS',
      antigravity_gemini: 'Mapeamento autônomo colunar via Data Cloud Tool Kit',
      multiplier: 'Instantâneo',
      highlight: false
    },
    {
      metric: 'Velocidade de Consulta Analítica',
      traditional: 'Segundos a minutos (scans recorrentes caros)',
      antigravity_gemini: '< 200 ms via reserva BigQuery BI Engine in-memory',
      multiplier: 'Sub-segundo garantido',
      highlight: false
    }
  ];

  // Títulos dos 9 Atos da Jornada do Herói
  const slideTitles = [
    'Ato 1: O Chamado — A Crise Invisível do Setor Elétrico',
    'Ato 2: O Abismo do Modelo Tradicional (O Mundo Ordinário)',
    'Ato 3: O Encontro com o Mentor — A Era da IA Agêntica',
    'Ato 4: O Mapa de Impacto da IA Agêntica — As 7 Fases',
    'Ato 5: A Travessia da Arquitetura — Medallion & FinOps R$ 0,00',
    'Ato 6: A Linha de Batalha das Sprints no Git',
    'Ato 7: A Provação Suprema — Motor PRORET & 34 Testes',
    'Ato 8: O Retorno com o Elixir — Cockpit C-Level com 9 Módulos',
    'Ato 9: O Legado — Síntese Tridimensional de Valor'
  ];

  // Matriz de Insights Específicos por Persona para cada Ato (0 a 8)
  const personaInsights = [
    // Slide 0 (Ato 1: O Chamado)
    {
      business: {
        role: 'CEO / CFO / Dir. Regulatório',
        focus: 'Risco de multas e glosas de R$ 50M+',
        takeaway: 'Tomar decisões com dados defasados em 45 dias impede antecipar compensações financeiras de DEC/FEC e simular o impacto de MMGD solar no faturamento da concessão.',
        metric: 'R$ 50M+ em risco anual'
      },
      cdo: {
        role: 'Chief Data Officer',
        focus: 'Silos federais & Falta de Single Source of Truth',
        takeaway: '5 órgãos reguladores independentes (ANEEL, ONS, CCEE, CVM, BCB) com tabelas desconexas, sem linhagem e sem governança unificada de dados abertos.',
        metric: '5 órgãos federais isolados'
      },
      engineer: {
        role: 'Líder de Engenharia de Dados',
        focus: 'Débito técnico & Falhas em rotinas legadas',
        takeaway: 'Pipelines manuais e scripts vulneráveis que quebram na madrugada, exigindo retrabalho exaustivo de decifrar regras colunares dispersas.',
        metric: '600+ págs de resoluções'
      }
    },
    // Slide 1 (Ato 2: O Abismo do Modelo Tradicional)
    {
      business: {
        role: 'CEO / CFO / Dir. Regulatório',
        focus: 'Custo de inércia & Perda de timing estratégico',
        takeaway: 'Squads tradicionais levam de 4 a 6 meses com custo superior a R$ 400k de folha e perda de timing estratégico nas revisões tarifárias e audiências públicas.',
        metric: '4 a 6 meses de atraso'
      },
      cdo: {
        role: 'Chief Data Officer',
        focus: 'Dados conflitantes em reuniões de diretoria',
        takeaway: 'Relatórios manuais em Excel e PDF criam números divergentes nas reuniões de conselho, destruindo a confiança nos dados e na tomada de decisão.',
        metric: 'Divergência crítica de dados'
      },
      engineer: {
        role: 'Líder de Engenharia de Dados',
        focus: 'R$ 8.000+/mês em clusters ociosos 24/7',
        takeaway: 'Infraestrutura cara com máquinas virtuais subutilizadas e Airflow ligado 24/7 sem necessidade enquanto o squad decifra regras manuais.',
        metric: 'R$ 8.000+/mês desperdiçados'
      }
    },
    // Slide 2 (Ato 3: O Encontro com o Mentor)
    {
      business: {
        role: 'CEO / CFO / Dir. Regulatório',
        focus: 'Time-to-market 15x mais ágil',
        takeaway: 'Redução radical do ciclo de desenvolvimento de meses para dias, permitindo respostas imediatas a mudanças na regulação e proteção de EBITDA.',
        metric: '15x mais ágil que squad'
      },
      cdo: {
        role: 'Chief Data Officer',
        focus: 'Engenharia reversa inteligente & Governança',
        takeaway: 'O Data Cloud Tool Kit mapeou esquemas da ANEEL e estruturou um catálogo governado sem a lentidão e o custo de consultorias externas.',
        metric: 'Zero discovery manual'
      },
      engineer: {
        role: 'Líder de Engenharia de Dados',
        focus: 'Par de engenharia de elite 24/7 & Self-healing',
        takeaway: 'O Antigravity agiu como par sênior, gerando IaC, Dataform SQLX, testes automatizados e corrigindo falhas de concorrência autonomamente.',
        metric: 'Self-healing ativo'
      }
    },
    // Slide 3 (Ato 4: O Mapa de Impacto da IA)
    {
      business: {
        role: 'CEO / CFO / Dir. Regulatório',
        focus: 'Visibilidade completa do investimento',
        takeaway: 'Cada uma das 7 fases do projeto gerou entregáveis de valor claros, desde a modelagem regulatória até o simulador de tarifas em produção.',
        metric: '7 fases estruturadas'
      },
      cdo: {
        role: 'Chief Data Officer',
        focus: 'Governança e conformidade em 100% das etapas',
        takeaway: 'Rastreabilidade total das regras de negócio aplicadas, garantindo que métricas de DEC/FEC e RAP batam com as resoluções da ANEEL.',
        metric: '100% de conformidade'
      },
      engineer: {
        role: 'Líder de Engenharia de Dados',
        focus: 'Orquestração dual & Portabilidade',
        takeaway: 'Cron jobs serverless no Scheduler com OIDC gerados em paridade com DAGs para Composer 3, garantindo portabilidade e zero lock-in.',
        metric: 'Scheduler OIDC + Composer'
      }
    },
    // Slide 4 (Ato 5: A Travessia da Arquitetura)
    {
      business: {
        role: 'CEO / CFO / Dir. Regulatório',
        focus: 'FinOps Serverless com R$ 0,00 de custo fixo',
        takeaway: 'Eliminação de custos com servidores ociosos: a empresa só paga por queries ativas, com o free tier cobrindo toda a operação base.',
        metric: 'R$ 0,00 custo base GCP'
      },
      cdo: {
        role: 'Chief Data Officer',
        focus: 'Arquitetura Medallion: Bronze ➔ Silver ➔ Gold',
        takeaway: 'Camadas de dados isoladas: Bronze bruto no GCS, Silver tipado no BigQuery e Gold in-memory com BI Engine para governança absoluta.',
        metric: 'Medallion Lakehouse'
      },
      engineer: {
        role: 'Líder de Engenharia de Dados',
        focus: 'BI Engine 2GB in-memory & Particionamento',
        takeaway: 'Queries analíticas pesadas respondendo em menos de 200ms graças à aceleração in-memory e clustering inteligente por UF e concessionária.',
        metric: '< 200 ms latência analítica'
      }
    },
    // Slide 5 (Ato 6: A Linha de Batalha das Sprints)
    {
      business: {
        role: 'CEO / CFO / Dir. Regulatório',
        focus: 'Entregas verificáveis e contínuas de valor',
        takeaway: 'A cada sprint, um novo componente vital do setor foi integrado: primeiro qualidade ANEEL, depois hidrologia ONS, e balanços CVM.',
        metric: 'Commits reais no Git'
      },
      cdo: {
        role: 'Chief Data Officer',
        focus: 'Integração federada de bases públicas',
        takeaway: 'Unificação em tempo recorde de dados abertos do ONS (S3), Banco Central (SGS), ANEEL (CKAN) e CVM (DFP/ITR).',
        metric: '5 bases públicas unificadas'
      },
      engineer: {
        role: 'Líder de Engenharia de Dados',
        focus: 'Pipelines idempotentes e MERGE deduplicado',
        takeaway: 'Cargas diárias e mensais que garantem idempotência absoluta via SQL MERGE sem risco de dados duplicados nas tabelas Silver.',
        metric: 'Idempotência via MERGE'
      }
    },
    // Slide 6 (Ato 7: A Provação Suprema)
    {
      business: {
        role: 'CEO / CFO / Dir. Regulatório',
        focus: 'Simulação paramétrica de WACC e Receita',
        takeaway: 'Capacidade de simular cenários de revisão tarifária com a fórmula oficial da ANEEL antes de audiências públicas, protegendo o EBITDA.',
        metric: 'WACC & BRR paramétricos'
      },
      cdo: {
        role: 'Chief Data Officer',
        focus: 'Confiabilidade matemática & Conformidade regulatória',
        takeaway: 'Cálculo auditável e aderente aos submódulos PRORET da ANEEL, com garantias de conformidade com a regulação setorial.',
        metric: 'Fórmula oficial PRORET'
      },
      engineer: {
        role: 'Líder de Engenharia de Dados',
        focus: '34 testes automatizados (100% Pass) & Resiliência',
        takeaway: 'Suíte completa de testes no backend validando contratos Pydantic, consultas BigQuery e fallbacks determinísticos sem regressões.',
        metric: '34/34 testes 100% OK'
      }
    },
    // Slide 7 (Ato 8: O Retorno com o Elixir)
    {
      business: {
        role: 'CEO / CFO / Dir. Regulatório',
        focus: 'Cockpit C-Level unificado com 9 módulos',
        takeaway: 'Acesso instantâneo a todos os pilares do setor elétrico (distribuição, transmissão, comercialização, geração distribuída e financeiro).',
        metric: '9 módulos ao vivo'
      },
      cdo: {
        role: 'Chief Data Officer',
        focus: 'Single Source of Truth para toda a companhia',
        takeaway: 'Todas as diretorias consom a mesma verdade regulatória e financeira, eliminando relatórios divergentes e retrabalho.',
        metric: 'Single Source of Truth'
      },
      engineer: {
        role: 'Líder de Engenharia de Dados',
        focus: 'Cloud Run com Docker multi-stage & React SPA',
        takeaway: 'Deploy escalável e moderno em Cloud Run com 1 vCPU e 1 GB RAM, servindo o backend FastAPI e frontend React 18 com alta fidelidade.',
        metric: 'Docker multi-stage Cloud Run'
      }
    },
    // Slide 8 (Ato 9: O Legado)
    {
      business: {
        role: 'CEO / CFO / Dir. Regulatório',
        focus: 'Vantagem competitiva & Eficiência de capital',
        takeaway: 'Adoção pioneira de IA agêntica reduz custos de consultoria em 90% e acelera tomadas de decisão regulatória e tarifária com capex zero.',
        metric: 'ROI Exponencial & Capex Zero'
      },
      cdo: {
        role: 'Chief Data Officer',
        focus: 'Fundação pronta para Agentes de Dados Autônomos',
        takeaway: 'Data Lakehouse catalogado e estruturado, pronto para receber agentes conversacionais de BI (Gemini Data Agents) com confiança.',
        metric: 'Data Agent Ready'
      },
      engineer: {
        role: 'Líder de Engenharia de Dados',
        focus: 'Novo padrão de engenharia com assistência de IA',
        takeaway: 'Desenvolvimento determinístico assistido por IA eleva a produtividade do time para um novo patamar com zero débito técnico.',
        metric: 'Padrão ouro de engenharia'
      }
    }
  ];

  // Helper para renderizar a caixa contextual da persona no slide ativo
  const renderPersonaCallout = (slideIdx: number) => {
    const insight = personaInsights[slideIdx];
    if (!insight) return null;

    if (selectedPersona === 'all') {
      return (
        <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200 space-y-2 mt-4">
          <div className="flex items-center justify-between">
            <span className="text-[11px] font-bold uppercase tracking-wider text-slate-700 flex items-center gap-1.5">
              <Users className="w-3.5 h-3.5 text-blue-600" />
              Impacto Tridimensional deste Ato:
            </span>
            <span className="text-[10px] text-slate-400">Clique nas personas acima para filtrar a visão</span>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-2.5 text-xs">
            <div className="p-2.5 rounded-lg bg-white border border-amber-200/80 shadow-2xs">
              <div className="flex items-center gap-1.5 text-amber-800 font-bold mb-1">
                <Briefcase className="w-3 h-3 text-amber-600" />
                <span>👔 Negócio (CEO/CFO):</span>
              </div>
              <p className="text-[11px] text-slate-600 leading-relaxed">{insight.business.takeaway}</p>
              <div className="mt-1.5 text-[10px] font-semibold text-amber-700 font-mono">
                🎯 {insight.business.metric}
              </div>
            </div>
            <div className="p-2.5 rounded-lg bg-white border border-indigo-200/80 shadow-2xs">
              <div className="flex items-center gap-1.5 text-indigo-800 font-bold mb-1">
                <Shield className="w-3 h-3 text-indigo-600" />
                <span>🛡️ CDO (Governança):</span>
              </div>
              <p className="text-[11px] text-slate-600 leading-relaxed">{insight.cdo.takeaway}</p>
              <div className="mt-1.5 text-[10px] font-semibold text-indigo-700 font-mono">
                🎯 {insight.cdo.metric}
              </div>
            </div>
            <div className="p-2.5 rounded-lg bg-white border border-emerald-200/80 shadow-2xs">
              <div className="flex items-center gap-1.5 text-emerald-800 font-bold mb-1">
                <Wrench className="w-3 h-3 text-emerald-600" />
                <span>⚙️ Engenharia de Dados:</span>
              </div>
              <p className="text-[11px] text-slate-600 leading-relaxed">{insight.engineer.takeaway}</p>
              <div className="mt-1.5 text-[10px] font-semibold text-emerald-700 font-mono">
                🎯 {insight.engineer.metric}
              </div>
            </div>
          </div>
        </div>
      );
    }

    if (selectedPersona === 'business') {
      return (
        <div className="p-4 rounded-xl bg-amber-500/10 border border-amber-500/40 space-y-1.5 mt-4 animate-fadeIn">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-amber-900 uppercase tracking-wide flex items-center gap-1.5">
              <Briefcase className="w-4 h-4 text-amber-600" />
              Perspectiva do Executivo de Negócio (CEO / CFO / Dir. Regulatório)
            </span>
            <span className="text-xs font-bold font-mono px-2.5 py-0.5 rounded-md bg-amber-200 text-amber-900 border border-amber-300">
              {insight.business.metric}
            </span>
          </div>
          <div className="text-xs text-slate-800 leading-relaxed">
            <strong className="text-amber-950 font-bold">Foco:</strong> {insight.business.focus} — {insight.business.takeaway}
          </div>
        </div>
      );
    }

    if (selectedPersona === 'cdo') {
      return (
        <div className="p-4 rounded-xl bg-indigo-500/10 border border-indigo-500/40 space-y-1.5 mt-4 animate-fadeIn">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-indigo-900 uppercase tracking-wide flex items-center gap-1.5">
              <Shield className="w-4 h-4 text-indigo-600" />
              Perspectiva do Chief Data Officer (CDO & Governança)
            </span>
            <span className="text-xs font-bold font-mono px-2.5 py-0.5 rounded-md bg-indigo-200 text-indigo-900 border border-indigo-300">
              {insight.cdo.metric}
            </span>
          </div>
          <div className="text-xs text-slate-800 leading-relaxed">
            <strong className="text-indigo-950 font-bold">Foco:</strong> {insight.cdo.focus} — {insight.cdo.takeaway}
          </div>
        </div>
      );
    }

    if (selectedPersona === 'engineer') {
      return (
        <div className="p-4 rounded-xl bg-emerald-500/10 border border-emerald-500/40 space-y-1.5 mt-4 animate-fadeIn">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-emerald-900 uppercase tracking-wide flex items-center gap-1.5">
              <Wrench className="w-4 h-4 text-emerald-600" />
              Perspectiva do Líder de Engenharia de Dados & FinOps
            </span>
            <span className="text-xs font-bold font-mono px-2.5 py-0.5 rounded-md bg-emerald-200 text-emerald-900 border border-emerald-300">
              {insight.engineer.metric}
            </span>
          </div>
          <div className="text-xs text-slate-800 leading-relaxed">
            <strong className="text-emerald-950 font-bold">Foco:</strong> {insight.engineer.focus} — {insight.engineer.takeaway}
          </div>
        </div>
      );
    }

    return null;
  };

  const filteredSprints =
    selectedSprintFilter === 'all'
      ? sprintsData
      : sprintsData.filter((s) => s.id === selectedSprintFilter);

  return (
    <div className="space-y-6">
      {/* Barra de Título & Controles de Modo */}
      <div className="bg-white border border-slate-200 rounded-2xl p-6 lg:p-8 text-slate-900 shadow-sm relative overflow-hidden">
        {/* Efeito visual de fundo suave */}
        <div className="absolute top-0 right-0 w-96 h-96 bg-gradient-to-br from-blue-100/60 via-purple-100/40 to-transparent rounded-full blur-3xl pointer-events-none" />
        <div className="absolute -bottom-10 -left-10 w-72 h-72 bg-gradient-to-tr from-amber-100/50 to-transparent rounded-full blur-2xl pointer-events-none" />

        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 mb-2">
              <span className="px-3 py-1 rounded-full text-xs font-bold tracking-wide uppercase bg-amber-100 text-amber-900 border border-amber-300 flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-amber-600" />
                Case & Storytelling • Antigravity+Gemini
              </span>
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-blue-100 text-blue-800 border border-blue-200">
                Google Cloud Platform
              </span>
              <span className="px-3 py-1 rounded-full text-xs font-semibold bg-emerald-100 text-emerald-800 border border-emerald-200">
                FinOps R$ 0,00
              </span>
            </div>
            <h1 className="text-2xl lg:text-3xl font-black tracking-tight text-slate-900 flex items-center gap-3">
              A História da Construção do Painel do Setor Elétrico
            </h1>
            <p className="text-slate-600 text-sm lg:text-base mt-1.5 max-w-3xl leading-relaxed">
              Como a união entre a complexidade regulatória do setor elétrico e a IA Agêntica{' '}
              <strong className="text-slate-900 font-bold">Antigravity+Gemini (Google DeepMind + Data Cloud Tool Kit)</strong> deu
              origem a um Lakehouse corporativo Medallion de alta fidelidade e custo zero.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2.5 shrink-0">
            {/* Seletor de Modo */}
            <div className="bg-slate-100 p-1.5 rounded-xl border border-slate-200 flex items-center">
              <button
                onClick={() => setViewMode('slides')}
                className={`px-3.5 py-2 rounded-lg text-xs lg:text-sm font-bold transition-all flex items-center gap-2 ${
                  viewMode === 'slides'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/80'
                }`}
              >
                <Maximize2 className="w-4 h-4" />
                Modo Apresentação (Slides)
              </button>
              <button
                onClick={() => setViewMode('dossier')}
                className={`px-3.5 py-2 rounded-lg text-xs lg:text-sm font-bold transition-all flex items-center gap-2 ${
                  viewMode === 'dossier'
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-slate-600 hover:text-slate-900 hover:bg-white/80'
                }`}
              >
                <BookOpen className="w-4 h-4" />
                Modo Dossiê (Linha do Tempo)
              </button>
            </div>

            {/* Botão de Exportação HTML Autônomo */}
            <button
              onClick={handleDownloadStandaloneHtml}
              disabled={isDownloading}
              title="Baixar arquivo HTML autocontido pronto para projeção offline"
              className="px-4 py-2 rounded-xl text-xs lg:text-sm font-bold bg-white hover:bg-slate-50 text-slate-800 border border-slate-200 shadow-2xs transition-all flex items-center gap-2"
            >
              <Download className={`w-4 h-4 text-amber-600 ${isDownloading ? 'animate-bounce' : ''}`} />
              {isDownloading ? 'Baixando...' : 'Baixar HTML Autônomo'}
            </button>
          </div>
        </div>
      </div>

      {/* ========================================================================= */}
      {/* MODO 1: APRESENTAÇÃO DE SLIDES INTERATIVA (PITCH DECK)                    */}
      {/* ========================================================================= */}
      {viewMode === 'slides' && (
        <div className="space-y-4">
          {/* Barra de Progresso e Navegação dos Slides */}
          <div className="bg-white rounded-xl p-3.5 border border-slate-200 shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-700">
              <span className="w-7 h-7 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center font-black">
                {currentSlide + 1}
              </span>
              <span className="text-slate-400">/</span>
              <span className="text-slate-500">{totalSlides}</span>
              <span className="ml-2 font-semibold text-slate-800 hidden sm:inline">
                {slideTitles[currentSlide]}
              </span>
            </div>

            {/* Stepper com bolinhas clicáveis */}
            <div className="flex items-center gap-1.5">
              {Array.from({ length: totalSlides }).map((_, index) => (
                <button
                  key={index}
                  onClick={() => setCurrentSlide(index)}
                  className={`h-2 rounded-full transition-all ${
                    currentSlide === index
                      ? 'w-8 bg-blue-600'
                      : 'w-2 bg-slate-200 hover:bg-slate-300'
                  }`}
                  aria-label={`Slide ${index + 1}`}
                  title={slideTitles[index]}
                />
              ))}
            </div>

            {/* Controles Anterior / Próximo */}
            <div className="flex items-center gap-1.5 shrink-0">
              <button
                onClick={() => setCurrentSlide((prev) => Math.max(prev - 1, 0))}
                disabled={currentSlide === 0}
                className="p-1.5 rounded-lg border border-slate-200 hover:bg-slate-100 disabled:opacity-40 disabled:pointer-events-none transition-colors"
                title="Slide Anterior (ou seta esquerda)"
              >
                <ChevronLeft className="w-4 h-4 text-slate-700" />
              </button>
              <button
                onClick={() => setCurrentSlide((prev) => Math.min(prev + 1, totalSlides - 1))}
                disabled={currentSlide === totalSlides - 1}
                className="px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white font-bold text-xs flex items-center gap-1.5 disabled:opacity-40 disabled:pointer-events-none transition-all shadow-sm"
                title="Próximo Slide (ou seta direita/espaço)"
              >
                <span>Avançar</span>
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>

          {/* Barra de Seleção de Persona Executiva */}
          <div className="bg-slate-50 border border-slate-200 rounded-xl p-2.5 flex flex-wrap items-center justify-between gap-2.5">
            <div className="flex items-center gap-2 text-xs font-bold text-slate-700">
              <Users className="w-4 h-4 text-blue-600" />
              <span>Personalizar Narrativa por Persona:</span>
            </div>
            <div className="flex flex-wrap items-center gap-1.5">
              <button
                onClick={() => setSelectedPersona('all')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 ${
                  selectedPersona === 'all'
                    ? 'bg-blue-600 text-white shadow-xs'
                    : 'bg-white text-slate-600 hover:text-slate-900 border border-slate-200'
                }`}
              >
                <span>🌐 Visão Global (Todas)</span>
              </button>
              <button
                onClick={() => setSelectedPersona('business')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 ${
                  selectedPersona === 'business'
                    ? 'bg-amber-600 text-white shadow-xs'
                    : 'bg-white text-slate-600 hover:text-slate-900 border border-slate-200'
                }`}
              >
                <Briefcase className="w-3.5 h-3.5 text-amber-500" />
                <span>👔 Executivo de Negócio (CEO/CFO)</span>
              </button>
              <button
                onClick={() => setSelectedPersona('cdo')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 ${
                  selectedPersona === 'cdo'
                    ? 'bg-indigo-600 text-white shadow-xs'
                    : 'bg-white text-slate-600 hover:text-slate-900 border border-slate-200'
                }`}
              >
                <Shield className="w-3.5 h-3.5 text-indigo-500" />
                <span>🛡️ Chief Data Officer (CDO)</span>
              </button>
              <button
                onClick={() => setSelectedPersona('engineer')}
                className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all flex items-center gap-1.5 ${
                  selectedPersona === 'engineer'
                    ? 'bg-emerald-600 text-white shadow-xs'
                    : 'bg-white text-slate-600 hover:text-slate-900 border border-slate-200'
                }`}
              >
                <Wrench className="w-3.5 h-3.5 text-emerald-500" />
                <span>⚙️ Líder de Engenharia de Dados</span>
              </button>
            </div>
          </div>

          {/* Área do Slide em Destaque */}
          <div className="bg-white rounded-2xl border border-slate-200 shadow-md p-6 lg:p-8 min-h-[540px] flex flex-col justify-between">
            {/* SLIDE 0: ATO 1 - O CHAMADO */}
            {currentSlide === 0 && (
              <div className="space-y-5 animate-fadeIn">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-4 gap-2">
                  <div className="flex items-center gap-2.5">
                    <span className="w-8 h-8 rounded-lg bg-rose-100 text-rose-700 flex items-center justify-center font-bold text-sm">
                      01
                    </span>
                    <div>
                      <h2 className="text-xl font-black text-slate-900">
                        Ato 1: O Chamado — A Crise Invisível do Setor Elétrico
                      </h2>
                      <p className="text-xs text-slate-500">
                        Um setor vital de escala continental refém de silos de dados e assimetria regulatória
                      </p>
                    </div>
                  </div>
                  <span className="text-xs font-semibold px-2.5 py-1 rounded bg-rose-100 text-rose-800 border border-rose-200">
                    O Chamado & A Dor Tripla
                  </span>
                </div>

                {/* Citação de Impacto */}
                <div className="p-3.5 rounded-xl bg-slate-900 text-white flex items-center gap-3">
                  <div className="w-8 h-8 rounded-lg bg-amber-500/20 text-amber-400 flex items-center justify-center font-black shrink-0 text-base">
                    ⚡
                  </div>
                  <blockquote className="text-xs lg:text-sm italic text-slate-200 font-medium">
                    &ldquo;No setor elétrico brasileiro, 1 segundo sem energia custa milhões. Mas tomar decisões corporativas e regulatórias com dados de 45 dias atrás custa o futuro da concessão.&rdquo;
                  </blockquote>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                    <div className="w-7 h-7 rounded-lg bg-blue-600 text-white flex items-center justify-center font-bold mb-2.5 text-xs">
                      ⚡
                    </div>
                    <h3 className="font-bold text-slate-900 text-xs mb-1">Dimensão Continental</h3>
                    <p className="text-[11px] text-slate-600 leading-relaxed">
                      O Sistema Interligado Nacional (SIN) conta com 4 subsistemas (SE/CO, Sul, NE e Norte), 103 distribuidoras, 176 transmissoras e 160 mil km de linhas de transmissão essenciais para o PIB.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                    <div className="w-7 h-7 rounded-lg bg-amber-500 text-white flex items-center justify-center font-bold mb-2.5 text-xs">
                      🏛️
                    </div>
                    <h3 className="font-bold text-slate-900 text-xs mb-1">O Labirinto dos Silos Federais</h3>
                    <p className="text-[11px] text-slate-600 leading-relaxed">
                      Dados dispersos em 5 órgãos independentes: ANEEL (PRODIST, SISGD, Tarifas), ONS (Hidrologia/CMO), CCEE (PLD/GSF), CVM (Balanços DFP/ITR) e BCB (Selic/IPCA), sem chaves integradas.
                    </p>
                  </div>

                  <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
                    <div className="w-7 h-7 rounded-lg bg-rose-500 text-white flex items-center justify-center font-bold mb-2.5 text-xs">
                      ⏱️
                    </div>
                    <h3 className="font-bold text-slate-900 text-xs mb-1">A Dor Tripla no Conselho</h3>
                    <p className="text-[11px] text-slate-600 leading-relaxed">
                      CEOs e CFOs sofrem com multas de DEC/FEC e simulação tarifária às cegas; CDOs não possuem SSOT governada; e a Engenharia atola mantendo rotinas manuais com clusters caros.
                    </p>
                  </div>
                </div>

                {/* Callout da Persona */}
                {renderPersonaCallout(0)}
              </div>
            )}

            {/* SLIDE 1: ATO 2 - O ABISMO DO MODELO TRADICIONAL */}
            {currentSlide === 1 && (
              <div className="space-y-5 animate-fadeIn">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-4 gap-2">
                  <div className="flex items-center gap-2.5">
                    <span className="w-8 h-8 rounded-lg bg-rose-100 text-rose-700 flex items-center justify-center font-bold text-sm">
                      02
                    </span>
                    <div>
                      <h2 className="text-xl font-black text-slate-900">
                        Ato 2: O Abismo do Modelo Tradicional (O Mundo Ordinário)
                      </h2>
                      <p className="text-xs text-slate-500">
                        O custo invisível da inércia: 6 meses de squad, clusters ociosos 24/7 e divergência em relatórios
                      </p>
                    </div>
                  </div>
                  <span className="text-xs font-semibold px-2.5 py-1 rounded bg-rose-100 text-rose-800 border border-rose-200">
                    O Abismo do Status Quo
                  </span>
                </div>

                {/* Grid Comparativo de Alto Impacto: O Pesadelo vs A Eficiência */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
                  {/* Lado Esquerdo: O Pesadelo Tradicional */}
                  <div className="p-4 rounded-xl bg-rose-50/70 border border-rose-200 space-y-3">
                    <div className="flex items-center gap-2 text-rose-900 font-bold text-xs uppercase tracking-wide">
                      <span className="w-5 h-5 rounded-md bg-rose-200 flex items-center justify-center text-rose-800 font-black">✕</span>
                      O Modelo Tradicional de Engenharia
                    </div>
                    <ul className="space-y-2.5 text-xs text-rose-950">
                      <li className="flex items-start gap-2">
                        <span className="text-rose-600 font-black mt-0.5">•</span>
                        <span><strong>4 a 6 meses de squad:</strong> R$ 400.000+ em folha salarial antes da primeira consulta em produção.</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-rose-600 font-black mt-0.5">•</span>
                        <span><strong>R$ 8.000+/mês em clusters 24/7:</strong> Máquinas virtuais e nós de Airflow ociosos queimando orçamento FinOps.</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-rose-600 font-black mt-0.5">•</span>
                        <span><strong>600+ páginas de resoluções manuais:</strong> Semanas de leitura humana de PRODIST e PRORET propensa a erros de interpretação.</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-rose-600 font-black mt-0.5">•</span>
                        <span><strong>Planilhas desconectadas:</strong> Reuniões de conselho com números conflitantes e zero rastreabilidade de dados.</span>
                      </li>
                    </ul>
                  </div>

                  {/* Lado Direito: A Revolução Agêntica */}
                  <div className="p-4 rounded-xl bg-emerald-50/70 border border-emerald-200 space-y-3">
                    <div className="flex items-center gap-2 text-emerald-900 font-bold text-xs uppercase tracking-wide">
                      <span className="w-5 h-5 rounded-md bg-emerald-200 flex items-center justify-center text-emerald-800 font-black">✓</span>
                      A Aceleração com Antigravity+Gemini
                    </div>
                    <ul className="space-y-2.5 text-xs text-emerald-950">
                      <li className="flex items-start gap-2">
                        <span className="text-emerald-600 font-black mt-0.5">•</span>
                        <span><strong>Poucos dias de sprints ágeis:</strong> Entrega contínua 15x mais veloz que desenvolvimento convencional.</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-emerald-600 font-black mt-0.5">•</span>
                        <span><strong>R$ 0,00 de custo fixo:</strong> Arquitetura serverless Scale-to-Zero (Cloud Run + Cloud Scheduler OIDC).</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-emerald-600 font-black mt-0.5">•</span>
                        <span><strong>Engenharia reversa autônoma:</strong> Mapeamento instantâneo de 214 MB de dados abertos ANEEL colunares.</span>
                      </li>
                      <li className="flex items-start gap-2">
                        <span className="text-emerald-600 font-black mt-0.5">•</span>
                        <span><strong>34 testes automatizados 100% aprovados:</strong> Contratos de dados estritos com Pydantic e TypeScript.</span>
                      </li>
                    </ul>
                  </div>
                </div>

                {/* Callout da Persona */}
                {renderPersonaCallout(1)}
              </div>
            )}

            {/* SLIDE 2: ATO 3 - O ENCONTRO COM O MENTOR */}
            {currentSlide === 2 && (
              <div className="space-y-5 animate-fadeIn">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-4 gap-2">
                  <div className="flex items-center gap-2.5">
                    <span className="w-8 h-8 rounded-lg bg-amber-100 text-amber-700 flex items-center justify-center font-bold text-sm">
                      03
                    </span>
                    <div>
                      <h2 className="text-xl font-black text-slate-900">
                        Ato 3: O Encontro com o Mentor — A Era da IA Agêntica
                      </h2>
                      <p className="text-xs text-slate-500">
                        Google DeepMind Antigravity aliado ao ferramental corporativo do Data Cloud Tool Kit
                      </p>
                    </div>
                  </div>
                  <span className="text-xs font-bold px-2.5 py-1 rounded bg-amber-100 text-amber-800 border border-amber-200 flex items-center gap-1">
                    <Sparkles className="w-3.5 h-3.5" />
                    DeepMind + Data Tool Kit
                  </span>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-5">
                  <div className="space-y-3">
                    <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                      <Cpu className="w-4 h-4 text-blue-600" />
                      Engenharia Agêntica Autônoma com Ferramentas
                    </h3>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      Diferente de assistentes de chat genéricos, a IA <strong>Antigravity+Gemini</strong> opera com capacidades agênticas completas: raciocínio avançado, inspeção de esquemas de dados, geração de código com tipagem estrita e execução de testes em sandbox determinística.
                    </p>

                    <div className="p-3 rounded-lg bg-slate-50 border border-slate-200 space-y-2">
                      <div className="text-xs font-bold text-slate-800">
                        Os 3 Superpoderes da IA no Projeto:
                      </div>
                      <div className="flex items-start gap-2 text-xs text-slate-700">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                        <span>
                          <strong>1. Engenharia Reversa Regulatória:</strong> Decifrou bases complexas da ANEEL sem semanas de discovery manual.
                        </span>
                      </div>
                      <div className="flex items-start gap-2 text-xs text-slate-700">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                        <span>
                          <strong>2. FinOps Serverless Custo Zero:</strong> Projetou pipelines Medallion e Cloud Run com política Scale-to-Zero.
                        </span>
                      </div>
                      <div className="flex items-start gap-2 text-xs text-slate-700">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                        <span>
                          <strong>3. Confiabilidade com Self-Healing:</strong> Escreveu e executou 34 testes automatizados com correção autônoma de quebras.
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="space-y-3">
                    <h3 className="text-xs font-bold text-slate-900 uppercase tracking-wider flex items-center gap-1.5">
                      <BarChart3 className="w-4 h-4 text-emerald-600" />
                      Métricas Quantitativas de Sucesso
                    </h3>

                    <div className="grid grid-cols-2 gap-3">
                      <div className="p-3 rounded-xl bg-blue-50 border border-blue-200">
                        <div className="text-[10px] font-bold text-blue-800 uppercase">Velocidade</div>
                        <div className="text-2xl font-black text-blue-900 mt-1">15x</div>
                        <div className="text-[11px] text-blue-700 mt-0.5">Mais ágil que squad tradicional</div>
                      </div>
                      <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200">
                        <div className="text-[10px] font-bold text-emerald-800 uppercase">Custo Fixo</div>
                        <div className="text-2xl font-black text-emerald-900 mt-1">R$ 0,00</div>
                        <div className="text-[11px] text-emerald-700 mt-0.5">Scale-to-zero serverless</div>
                      </div>
                      <div className="p-3 rounded-xl bg-purple-50 border border-purple-200">
                        <div className="text-[10px] font-bold text-purple-800 uppercase">Testes Aprovados</div>
                        <div className="text-2xl font-black text-purple-900 mt-1">34 / 34</div>
                        <div className="text-[11px] text-purple-700 mt-0.5">100% de sucesso automatizado</div>
                      </div>
                      <div className="p-3 rounded-xl bg-amber-50 border border-amber-200">
                        <div className="text-[10px] font-bold text-amber-800 uppercase">Latência de Query</div>
                        <div className="text-2xl font-black text-amber-900 mt-1">&lt; 200 ms</div>
                        <div className="text-[11px] text-amber-700 mt-0.5">BI Engine 2GB in-memory</div>
                      </div>
                    </div>
                  </div>
                </div>

                {/* Callout da Persona */}
                {renderPersonaCallout(2)}
              </div>
            )}

            {/* SLIDE 3: ATO 4 - O MAPA DE IMPACTO DA IA AGÊNTICA */}
            {currentSlide === 3 && (
              <div className="space-y-4 animate-fadeIn">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-3 gap-2">
                  <div className="flex items-center gap-2.5">
                    <span className="w-8 h-8 rounded-lg bg-amber-100 text-amber-800 flex items-center justify-center font-bold text-sm">
                      04
                    </span>
                    <div>
                      <h2 className="text-xl font-black text-slate-900">
                        Ato 4: O Mapa de Impacto da IA Agêntica — As 7 Fases
                      </h2>
                      <p className="text-xs text-slate-500">
                        Atuação de ponta a ponta da IA no ciclo de vida da plataforma regulatória e analítica
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-2.5">
                    {/* Seletor de visualização Tabela vs Cards */}
                    <div className="bg-slate-100 p-1 rounded-xl border border-slate-200 flex items-center text-xs">
                      <button
                        onClick={() => setImpactViewMode('table')}
                        className={`px-3 py-1.5 rounded-lg font-bold transition-all flex items-center gap-1.5 ${
                          impactViewMode === 'table'
                            ? 'bg-blue-600 text-white shadow-2xs'
                            : 'text-slate-600 hover:text-slate-900'
                        }`}
                      >
                        <Table className="w-3.5 h-3.5" />
                        Tabela Executiva
                      </button>
                      <button
                        onClick={() => setImpactViewMode('cards')}
                        className={`px-3 py-1.5 rounded-lg font-bold transition-all flex items-center gap-1.5 ${
                          impactViewMode === 'cards'
                            ? 'bg-blue-600 text-white shadow-2xs'
                            : 'text-slate-600 hover:text-slate-900'
                        }`}
                      >
                        <LayoutGrid className="w-3.5 h-3.5" />
                        Cards por Fase
                      </button>
                    </div>

                    <span className="text-xs font-bold px-2.5 py-1 rounded bg-amber-100 text-amber-900 border border-amber-300 flex items-center gap-1 shrink-0">
                      <Sparkles className="w-3.5 h-3.5 text-amber-600" />
                      7 Fases Mapeadas
                    </span>
                  </div>
                </div>

                {/* Conteúdo: Tabela Executiva ou Grid de Cards */}
                {impactViewMode === 'table' ? (
                  <div className="overflow-hidden rounded-xl border border-slate-200 bg-white shadow-2xs">
                    <div className="overflow-x-auto max-h-[300px] overflow-y-auto">
                      <table className="w-full text-left text-xs">
                        <thead className="sticky top-0 bg-slate-50 border-b border-slate-200 text-slate-600 uppercase text-[10px] font-bold z-10">
                          <tr>
                            <th className="py-2 px-3 w-1/3">Fase do Projeto</th>
                            <th className="py-2 px-3 w-2/3 text-blue-700">Papel da IA (Antigravity + Data Cloud Tool Kit)</th>
                          </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-100">
                          {aiImpactMap.map((item) => {
                            const Icon = item.icon;
                            return (
                              <tr key={item.id} className="hover:bg-blue-50/20 transition-colors">
                                <td className="py-2.5 px-3 align-top">
                                  <div className="flex items-center gap-2 mb-1">
                                    <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${item.badgeColor}`}>
                                      {item.badge}
                                    </span>
                                    <div className="w-5 h-5 rounded bg-slate-100 flex items-center justify-center text-slate-600">
                                      <Icon className="w-3 h-3 text-blue-600" />
                                    </div>
                                  </div>
                                  <div className="font-bold text-slate-900 text-xs">{item.phase}</div>
                                </td>
                                <td className="py-2.5 px-3 align-top">
                                  <ul className="space-y-1 text-slate-700 text-[11px]">
                                    {item.bullets.map((b, bIdx) => (
                                      <li key={bIdx} className="flex items-start gap-1 leading-relaxed">
                                        <span className="text-blue-600 font-bold">•</span>
                                        <span>{b}</span>
                                      </li>
                                    ))}
                                  </ul>
                                </td>
                              </tr>
                            );
                          })}
                        </tbody>
                      </table>
                    </div>
                  </div>
                ) : (
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-2.5 max-h-[300px] overflow-y-auto pr-1">
                    {aiImpactMap.map((item) => {
                      const Icon = item.icon;
                      return (
                        <div
                          key={item.id}
                          className="p-3 rounded-xl border border-slate-200 bg-slate-50/80 hover:bg-slate-50 transition-all flex flex-col justify-between space-y-2 shadow-2xs"
                        >
                          <div className="space-y-1">
                            <div className="flex items-center justify-between">
                              <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${item.badgeColor}`}>
                                {item.badge}
                              </span>
                              <div className="w-5 h-5 rounded-md bg-white border border-slate-200 flex items-center justify-center text-slate-600">
                                <Icon className="w-3 h-3 text-blue-600" />
                              </div>
                            </div>
                            <div className="font-bold text-xs text-slate-900">{item.phase}</div>
                            <ul className="space-y-1 text-[11px] text-slate-600">
                              {item.bullets.map((b, bIdx) => (
                                <li key={bIdx} className="flex items-start gap-1">
                                  <span className="text-blue-500 font-bold">•</span>
                                  <span>{b}</span>
                                </li>
                              ))}
                            </ul>
                          </div>
                          <div className="pt-1.5 border-t border-slate-200/80 text-[10px] text-slate-500 font-medium">
                            🎯 {item.deliverable}
                          </div>
                        </div>
                      );
                    })}
                  </div>
                )}

                {/* Callout da Persona */}
                {renderPersonaCallout(3)}
              </div>
            )}

            {/* SLIDE 4: ATO 5 - A TRAVESSIA DA ARQUITETURA */}
            {currentSlide === 4 && (
              <div className="space-y-5 animate-fadeIn">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-4 gap-2">
                  <div className="flex items-center gap-2.5">
                    <span className="w-8 h-8 rounded-lg bg-purple-100 text-purple-700 flex items-center justify-center font-bold text-sm">
                      05
                    </span>
                    <div>
                      <h2 className="text-xl font-black text-slate-900">
                        Ato 5: A Travessia da Arquitetura — Medallion & FinOps R$ 0,00
                      </h2>
                      <p className="text-xs text-slate-500">
                        Topologia Lakehouse corporativa no Google Cloud com aceleração in-memory e custo zero
                      </p>
                    </div>
                  </div>
                  <span className="text-xs font-semibold px-2.5 py-1 rounded bg-purple-100 text-purple-800 border border-purple-200">
                    Google Cloud Platform
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {/* Bronze */}
                  <div className="p-4 rounded-xl border border-blue-200 bg-blue-50/40 relative">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-bold uppercase tracking-wider text-blue-700">
                        Camada Bronze
                      </span>
                      <span className="text-[10px] px-2 py-0.5 bg-blue-200 text-blue-800 rounded font-semibold">
                        GCS
                      </span>
                    </div>
                    <div className="text-sm font-bold text-slate-800 mb-1">Raw Parquet & CSV</div>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      Bucket <code className="text-[11px] bg-white px-1 py-0.5 rounded">gs://kpisetoreletrico-datalake-bronze</code> com migração automática para Nearline/Coldline.
                    </p>
                    <div className="mt-3 text-[11px] text-blue-800 font-semibold">
                      Volumetria: 214 MB particionados por ano/mês
                    </div>
                  </div>

                  {/* Silver */}
                  <div className="p-4 rounded-xl border border-indigo-200 bg-indigo-50/40 relative">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-bold uppercase tracking-wider text-indigo-700">
                        Camada Silver
                      </span>
                      <span className="text-[10px] px-2 py-0.5 bg-indigo-200 text-indigo-800 rounded font-semibold">
                        BigQuery
                      </span>
                    </div>
                    <div className="text-sm font-bold text-slate-800 mb-1">aneel_silver</div>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      Tabelas normalizadas, tipadas e particionadas por data com clustering por concessionária e UF. Cargas idempotentes via comando MERGE.
                    </p>
                    <div className="mt-3 text-[11px] text-indigo-800 font-semibold">
                      4 tabelas estruturadas (DEC/FEC, GD, Tarifas, Ouvidoria)
                    </div>
                  </div>

                  {/* Gold */}
                  <div className="p-4 rounded-xl border border-amber-200 bg-amber-50/40 relative">
                    <div className="flex items-center justify-between mb-2">
                      <span className="text-xs font-bold uppercase tracking-wider text-amber-700">
                        Camada Gold
                      </span>
                      <span className="text-[10px] px-2 py-0.5 bg-amber-200 text-amber-800 rounded font-semibold">
                        BI Engine
                      </span>
                    </div>
                    <div className="text-sm font-bold text-slate-800 mb-1">gold_kpis (In-Memory)</div>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      Modelos analíticos pré-agregados pelo Dataform SQLX com aceleração in-memory de 2 GB. Consultas C-Level resolvidas em menos de 200 ms.
                    </p>
                    <div className="mt-3 text-[11px] text-amber-800 font-semibold">
                      Zero custo de bytes faturados recorrentes
                    </div>
                  </div>
                </div>

                {/* Destaque FinOps */}
                <div className="p-4 rounded-xl bg-slate-900 text-white flex flex-col md:flex-row items-center justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <Coins className="w-4 h-4 text-emerald-400" />
                      <span className="text-xs font-bold uppercase tracking-wider text-emerald-400">
                        Estratégia FinOps Serverless (R$ 0,00 de Infraestrutura Fixa)
                      </span>
                    </div>
                    <p className="text-xs text-slate-300 max-w-2xl leading-relaxed">
                      Eliminamos clusters Kubernetes/Airflow 24/7 (que custariam R$ 8.000+/mês). O sistema opera em{' '}
                      <strong>Cloud Run</strong> com Scale-to-Zero, <strong>Cloud Scheduler</strong> disparando
                      cron jobs serverless via OIDC e <strong>BigQuery BI Engine</strong> gratuito no tier base.
                    </p>
                  </div>
                  <div className="text-right shrink-0">
                    <div className="text-2xl font-black text-emerald-400">R$ 0,00</div>
                    <div className="text-[10px] text-slate-400">Custo base no Google Cloud</div>
                  </div>
                </div>

                {/* Callout da Persona */}
                {renderPersonaCallout(4)}
              </div>
            )}

            {/* SLIDE 5: ATO 6 - A LINHA DE BATALHA DAS SPRINTS NO GIT */}
            {currentSlide === 5 && (
              <div className="space-y-5 animate-fadeIn">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-4 gap-2">
                  <div className="flex items-center gap-2.5">
                    <span className="w-8 h-8 rounded-lg bg-emerald-100 text-emerald-700 flex items-center justify-center font-bold text-sm">
                      06
                    </span>
                    <div>
                      <h2 className="text-xl font-black text-slate-900">
                        Ato 6: A Linha de Batalha das Sprints no Git
                      </h2>
                      <p className="text-xs text-slate-500">
                        Evolução contínua verificável via histórico autêntico de commits no repositório
                      </p>
                    </div>
                  </div>
                  <span className="text-xs font-semibold px-2.5 py-1 rounded bg-slate-100 text-slate-600">
                    Histórico Auditável
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                  <div className="p-3.5 rounded-xl border border-slate-200 bg-slate-50 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-bold text-blue-700 bg-blue-100 px-2 py-0.5 rounded">
                        Set/2026 • Fundação
                      </span>
                      <span className="text-[10px] text-slate-400 font-mono">commit a3d0f77</span>
                    </div>
                    <div className="font-bold text-xs text-slate-800">Gênese & Setup Lakehouse</div>
                    <p className="text-[11px] text-slate-600">
                      Ingestão dos 4 datasets oficiais ANEEL (PRODIST, SISGD MMGD, Tarifas PRORET e Ouvidoria IASC).
                    </p>
                    <div className="text-[10px] text-amber-800 font-semibold bg-amber-50 p-1.5 rounded border border-amber-200/60">
                      ⚡ Antigravity: Engenharia reversa dos dados abertos e modelagem Silver inicial.
                    </div>
                  </div>

                  <div className="p-3.5 rounded-xl border border-slate-200 bg-slate-50 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-bold text-purple-700 bg-purple-100 px-2 py-0.5 rounded">
                        Out/2026 • Sprint 1
                      </span>
                      <span className="text-[10px] text-slate-400 font-mono">commit 292186e</span>
                    </div>
                    <div className="font-bold text-xs text-slate-800">Alertas, ONS S3 & BCB</div>
                    <p className="text-[11px] text-slate-600">
                      Eliminação de mocks; dados de hidrologia SIN live (EAR/ENA/CMO) e índices macroeconômicos (Selic/IPCA).
                    </p>
                    <div className="text-[10px] text-amber-800 font-semibold bg-amber-50 p-1.5 rounded border border-amber-200/60">
                      ⚡ Antigravity: Conexão resiliente ao bucket ONS S3 e APIs públicas com cache.
                    </div>
                  </div>

                  <div className="p-3.5 rounded-xl border border-slate-200 bg-slate-50 space-y-2">
                    <div className="flex items-center justify-between">
                      <span className="text-[11px] font-bold text-indigo-700 bg-indigo-100 px-2 py-0.5 rounded">
                        Out/2026 • Sprint 2 & 3
                      </span>
                      <span className="text-[10px] text-slate-400 font-mono">commit 292186e</span>
                    </div>
                    <div className="font-bold text-xs text-slate-800">Transmissão & CVM DFP/ITR</div>
                    <p className="text-[11px] text-slate-600">
                      RAP/PVd homologados ANEEL, SLAs da REN 1.000/2021 e balanços auditados de 8 companhias abertas.
                    </p>
                    <div className="text-[10px] text-amber-800 font-semibold bg-amber-50 p-1.5 rounded border border-amber-200/60">
                      ⚡ Antigravity: Parser de arquivos CVM e regras de liquidação financeira CCEE.
                    </div>
                  </div>
                </div>

                {/* Refinamento PRORET */}
                <div className="p-3.5 rounded-xl border border-rose-200 bg-rose-50/50 flex items-center justify-between gap-4">
                  <div className="space-y-1">
                    <div className="flex items-center gap-2">
                      <span className="text-xs font-bold text-rose-800 uppercase tracking-wide">
                        Refinamento Final: Motor Regulatório PRORET (Outubro 2026 • commit a64ead0)
                      </span>
                    </div>
                    <p className="text-xs text-slate-600 leading-relaxed">
                      Implementação da fórmula oficial da Receita Requerida com WACC regulatório, Base de Remuneração Regulatória (BRR),
                      OPEX eficiente, Fator X e Componente Q, além de fallbacks determinísticos para robustez contínua.
                    </p>
                  </div>
                  <span className="text-xs font-bold px-3 py-1.5 rounded-lg bg-rose-600 text-white shrink-0 shadow-sm">
                    34 Testes Pass
                  </span>
                </div>

                {/* Callout da Persona */}
                {renderPersonaCallout(5)}
              </div>
            )}

            {/* SLIDE 6: ATO 7 - A PROVAÇÃO SUPREMA: MOTOR PRORET & 34 TESTES */}
            {currentSlide === 6 && (
              <div className="space-y-5 animate-fadeIn">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-4 gap-2">
                  <div className="flex items-center gap-2.5">
                    <span className="w-8 h-8 rounded-lg bg-teal-100 text-teal-700 flex items-center justify-center font-bold text-sm">
                      07
                    </span>
                    <div>
                      <h2 className="text-xl font-black text-slate-900">
                        Ato 7: A Provação Suprema — Motor PRORET & 34 Testes
                      </h2>
                      <p className="text-xs text-slate-500">
                        Cálculo regulatório matemático rigoroso e blindagem de software com testes 100% aprovados
                      </p>
                    </div>
                  </div>
                  <span className="text-xs font-bold px-2.5 py-1 rounded bg-teal-100 text-teal-800 border border-teal-200 flex items-center gap-1">
                    <ShieldCheck className="w-3.5 h-3.5" />
                    34 Testes 100% Pass
                  </span>
                </div>

                {/* Fórmula Oficial PRORET */}
                <div className="p-3.5 rounded-xl bg-slate-900 text-white flex flex-col md:flex-row items-center justify-between gap-3 shadow-2xs">
                  <div className="space-y-1">
                    <div className="text-[11px] font-bold text-amber-400 uppercase tracking-wider">
                      Fórmula Canônica de Revisão Tarifária (ANEEL PRORET Submódulo 2.1)
                    </div>
                    <div className="font-mono text-xs text-slate-200">
                      Receita Requerida (RR) = [BRR × WACC] + OPEX Eficiente - Fator X ± Componente Q
                    </div>
                  </div>
                  <span className="text-[10px] font-mono text-slate-400 bg-slate-800 px-2.5 py-1 rounded border border-slate-700">
                    Parcela A (Incontrolável) vs Parcela B (Gerenciável)
                  </span>
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2.5">
                    <h3 className="font-bold text-xs text-slate-900 flex items-center gap-2">
                      <Terminal className="w-4 h-4 text-slate-700" />
                      Suíte de Testes Automatizados no Backend
                    </h3>
                    <div className="space-y-1.5 text-xs">
                      <div className="p-2 rounded-lg bg-white border border-slate-200 flex items-center justify-between">
                        <span className="font-mono text-slate-700 text-[11px]">test_sprint1_lakehouse.py</span>
                        <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">
                          8 Testes ✓
                        </span>
                      </div>
                      <div className="p-2 rounded-lg bg-white border border-slate-200 flex items-center justify-between">
                        <span className="font-mono text-slate-700 text-[11px]">test_sprint2_lakehouse.py</span>
                        <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">
                          10 Testes ✓
                        </span>
                      </div>
                      <div className="p-2 rounded-lg bg-white border border-slate-200 flex items-center justify-between">
                        <span className="font-mono text-slate-700 text-[11px]">test_cvm_financials_sprint3.py</span>
                        <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">
                          9 Testes ✓
                        </span>
                      </div>
                      <div className="p-2 rounded-lg bg-white border border-slate-200 flex items-center justify-between">
                        <span className="font-mono text-slate-700 text-[11px]">test_ccee_guarantees.py</span>
                        <span className="px-2 py-0.5 rounded bg-emerald-100 text-emerald-800 font-bold text-[10px]">
                          7 Testes ✓
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="p-4 rounded-xl bg-slate-50 border border-slate-200 space-y-2.5">
                    <h3 className="font-bold text-xs text-slate-900 flex items-center gap-2">
                      <CheckCircle className="w-4 h-4 text-emerald-600" />
                      Mecanismos de Resiliência & Integridade
                    </h3>
                    <ul className="space-y-2 text-xs text-slate-600 leading-relaxed">
                      <li className="flex items-start gap-2">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                        <span>
                          <strong>Dataform SQLX Assertions:</strong> Verificação de não-nulidade e unicidade de
                          chaves primárias na materialização da camada Gold.
                        </span>
                      </li>
                      <li className="flex items-start gap-2">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                        <span>
                          <strong>Fallback Determinístico:</strong> Garantia de operação contínua caso portais federais
                          fiquem offline, sem tela branca para o usuário.
                        </span>
                      </li>
                      <li className="flex items-start gap-2">
                        <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                        <span>
                          <strong>Tipagem com Pydantic & TypeScript:</strong> Schemas rigorosos de ponta
                          a ponta entre BigQuery, FastAPI e React 18.
                        </span>
                      </li>
                    </ul>
                  </div>
                </div>

                <div className="p-3 rounded-xl bg-emerald-50 border border-emerald-200 text-xs text-emerald-900 font-medium">
                  ⚡ <strong>Self-Healing Agêntico pelo Antigravity:</strong> Durante o desenvolvimento das Sprints, falhas
                  de concorrência e tipos foram diagnosticadas e resolvidas autonomamente pelo agente, executando a suíte
                  completa de testes a cada iteração sem intervenção manual.
                </div>

                {/* Callout da Persona */}
                {renderPersonaCallout(6)}
              </div>
            )}

            {/* SLIDE 7: ATO 8 - O RETORNO COM O ELIXIR (COCKPIT C-LEVEL) */}
            {currentSlide === 7 && (
              <div className="space-y-5 animate-fadeIn">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-4 gap-2">
                  <div className="flex items-center gap-2.5">
                    <span className="w-8 h-8 rounded-lg bg-blue-100 text-blue-700 flex items-center justify-center font-bold text-sm">
                      08
                    </span>
                    <div>
                      <h2 className="text-xl font-black text-slate-900">
                        Ato 8: O Retorno com o Elixir — Cockpit C-Level com 9 Módulos
                      </h2>
                      <p className="text-xs text-slate-500">
                        O produto final em produção: cockpit executivo interativo com mapa do SIN e alta fidelidade
                      </p>
                    </div>
                  </div>
                  <span className="text-xs font-bold px-2.5 py-1 rounded bg-blue-100 text-blue-800 border border-blue-200">
                    9 Módulos ao Vivo
                  </span>
                </div>

                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2.5">
                  <button
                    onClick={() => onNavigateTab && onNavigateTab('executive')}
                    className="p-3 rounded-xl border border-slate-200 hover:border-blue-400 hover:bg-blue-50/50 text-left transition-all group"
                  >
                    <div className="text-xs font-bold text-slate-900 group-hover:text-blue-700 flex items-center justify-between">
                      <span>1. Visão Executiva (C-Level)</span>
                      <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-blue-600" />
                    </div>
                    <p className="text-[11px] text-slate-500 mt-1">
                      Matriz CEO/COO/CFO e mapa do SIN por subsistema.
                    </p>
                  </button>

                  <button
                    onClick={() => onNavigateTab && onNavigateTab('distribuicao')}
                    className="p-3 rounded-xl border border-slate-200 hover:border-blue-400 hover:bg-blue-50/50 text-left transition-all group"
                  >
                    <div className="text-xs font-bold text-slate-900 group-hover:text-blue-700 flex items-center justify-between">
                      <span>2. Qualidade (PRODIST)</span>
                      <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-blue-600" />
                    </div>
                    <p className="text-[11px] text-slate-500 mt-1">
                      Conformidade DEC/FEC e cálculo de compensações financeiras.
                    </p>
                  </button>

                  <button
                    onClick={() => onNavigateTab && onNavigateTab('financeiro_proret')}
                    className="p-3 rounded-xl border border-slate-200 hover:border-blue-400 hover:bg-blue-50/50 text-left transition-all group"
                  >
                    <div className="text-xs font-bold text-slate-900 group-hover:text-blue-700 flex items-center justify-between">
                      <span>3. Simulador PRORET & DRE</span>
                      <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-blue-600" />
                    </div>
                    <p className="text-[11px] text-slate-500 mt-1">
                      Revisão tarifária com WACC e BRR + dados contábeis CVM de 8 empresas.
                    </p>
                  </button>

                  <button
                    onClick={() => onNavigateTab && onNavigateTab('sin')}
                    className="p-3 rounded-xl border border-slate-200 hover:border-blue-400 hover:bg-blue-50/50 text-left transition-all group"
                  >
                    <div className="text-xs font-bold text-slate-900 group-hover:text-blue-700 flex items-center justify-between">
                      <span>4. Operação do SIN</span>
                      <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-blue-600" />
                    </div>
                    <p className="text-[11px] text-slate-500 mt-1">
                      Hidrologia live (ONS S3): EAR, ENA, CMO e despacho térmico.
                    </p>
                  </button>

                  <button
                    onClick={() => onNavigateTab && onNavigateTab('ccee')}
                    className="p-3 rounded-xl border border-slate-200 hover:border-blue-400 hover:bg-blue-50/50 text-left transition-all group"
                  >
                    <div className="text-xs font-bold text-slate-900 group-hover:text-blue-700 flex items-center justify-between">
                      <span>5. Mercado CCEE</span>
                      <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-blue-600" />
                    </div>
                    <p className="text-[11px] text-slate-500 mt-1">
                      PLD Horário, GSF, Curtailment, ESS e Bandeiras Tarifárias.
                    </p>
                  </button>

                  <button
                    onClick={() => onNavigateTab && onNavigateTab('perdas_mmgd')}
                    className="p-3 rounded-xl border border-slate-200 hover:border-blue-400 hover:bg-blue-50/50 text-left transition-all group"
                  >
                    <div className="text-xs font-bold text-slate-900 group-hover:text-blue-700 flex items-center justify-between">
                      <span>6. Perdas & MMGD (27 UFs)</span>
                      <ExternalLink className="w-3.5 h-3.5 text-slate-400 group-hover:text-blue-600" />
                    </div>
                    <p className="text-[11px] text-slate-500 mt-1">
                      Balanço de perdas e expansão solar da Lei 14.300 em todos os estados.
                    </p>
                  </button>
                </div>

                {/* Callout da Persona */}
                {renderPersonaCallout(7)}
              </div>
            )}

            {/* SLIDE 8: ATO 9 - O LEGADO (SÍNTESE TRIDIMENSIONAL DE VALOR) */}
            {currentSlide === 8 && (
              <div className="space-y-5 animate-fadeIn">
                <div className="flex flex-col sm:flex-row sm:items-center justify-between border-b border-slate-100 pb-4 gap-2">
                  <div className="flex items-center gap-2.5">
                    <span className="w-8 h-8 rounded-lg bg-indigo-100 text-indigo-700 flex items-center justify-center font-bold text-sm">
                      09
                    </span>
                    <div>
                      <h2 className="text-xl font-black text-slate-900">
                        Ato 9: O Legado — Síntese Tridimensional de Valor
                      </h2>
                      <p className="text-xs text-slate-500">
                        O impacto consolidado para Negócio, CDO e Engenharia de Dados
                      </p>
                    </div>
                  </div>
                  <span className="text-xs font-bold px-2.5 py-1 rounded bg-indigo-100 text-indigo-800 border border-indigo-200 flex items-center gap-1">
                    <Trophy className="w-3.5 h-3.5 text-indigo-600" />
                    Valor Comprovado
                  </span>
                </div>

                {/* 3 Pilares Tridimensionais de Impacto */}
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {/* Negócio */}
                  <div className="p-4 rounded-xl border border-amber-200 bg-amber-50/50 space-y-2">
                    <div className="flex items-center gap-2 text-amber-900 font-bold text-xs uppercase tracking-wide">
                      <Briefcase className="w-4 h-4 text-amber-600" />
                      👔 Executivo de Negócio
                    </div>
                    <ul className="text-xs text-slate-700 space-y-1.5 leading-relaxed">
                      <li>• Decisões estratégicas em menos de 200 ms.</li>
                      <li>• Prevenção de multas de DEC/FEC e simulação de faturas.</li>
                      <li>• Blindagem de EBITDA nas revisões tarifárias da ANEEL.</li>
                      <li>• <strong>Capex zero:</strong> Custo de infraestrutura fixo de R$ 0,00.</li>
                    </ul>
                  </div>

                  {/* CDO */}
                  <div className="p-4 rounded-xl border border-indigo-200 bg-indigo-50/50 space-y-2">
                    <div className="flex items-center gap-2 text-indigo-900 font-bold text-xs uppercase tracking-wide">
                      <Shield className="w-4 h-4 text-indigo-600" />
                      🛡️ Chief Data Officer
                    </div>
                    <ul className="text-xs text-slate-700 space-y-1.5 leading-relaxed">
                      <li>• Eliminação definitiva de silos de dados regulatórios.</li>
                      <li>• Single Source of Truth para todas as diretorias.</li>
                      <li>• Governança e linhagem transparente no BigQuery.</li>
                      <li>• <strong>Prontidão para Agentes de Dados:</strong> Gemini Data Agents ready.</li>
                    </ul>
                  </div>

                  {/* Engenharia */}
                  <div className="p-4 rounded-xl border border-emerald-200 bg-emerald-50/50 space-y-2">
                    <div className="flex items-center gap-2 text-emerald-900 font-bold text-xs uppercase tracking-wide">
                      <Wrench className="w-4 h-4 text-emerald-600" />
                      ⚙️ Líder de Engenharia
                    </div>
                    <ul className="text-xs text-slate-700 space-y-1.5 leading-relaxed">
                      <li>• Squad 15x mais produtivo com assistência agêntica.</li>
                      <li>• 34 testes automatizados 100% aprovados.</li>
                      <li>• Arquitetura Medallion serverless Scale-to-Zero.</li>
                      <li>• <strong>Zero débito técnico:</strong> Contratos de tipos estritos.</li>
                    </ul>
                  </div>
                </div>

                {/* Banner de Encerramento com CTA */}
                <div className="p-4 rounded-xl bg-gradient-to-r from-blue-900 to-indigo-950 text-white flex flex-col sm:flex-row items-center justify-between gap-4">
                  <div className="space-y-1">
                    <div className="text-xs font-bold uppercase tracking-wider text-blue-300">
                      Conclusão da Jornada
                    </div>
                    <p className="text-xs text-slate-200 max-w-xl">
                      A aplicação comprova que a IA Agêntica moderna transforma a complexidade regulatória corporativa em{' '}
                      <strong>engenharia de software determinística, arquitetura de dados rigorosa e valor executivo real</strong>.
                    </p>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <button
                      onClick={() => onNavigateTab && onNavigateTab('executive')}
                      className="px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-xs flex items-center gap-2 shadow-sm transition-all"
                    >
                      <span>Abrir Cockpit C-Level</span>
                      <ExternalLink className="w-3.5 h-3.5" />
                    </button>
                    <button
                      onClick={handleDownloadStandaloneHtml}
                      className="px-4 py-2 rounded-xl bg-amber-400 hover:bg-amber-300 text-slate-950 font-bold text-xs flex items-center gap-2 shadow-sm transition-all"
                    >
                      <Download className="w-3.5 h-3.5" />
                      <span>Baixar HTML</span>
                    </button>
                  </div>
                </div>

                {/* Callout da Persona */}
                {renderPersonaCallout(8)}
              </div>
            )}

            {/* Rodapé do Slide: Dica de navegação por teclado */}
            <div className="pt-4 border-t border-slate-100 flex items-center justify-between text-[11px] text-slate-400">
              <span className="flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5 text-amber-500" />
                Painel desenvolvido com Antigravity+Gemini (Google DeepMind + Data Cloud Tool Kit)
              </span>
              <span className="hidden sm:inline">
                Use as teclas <kbd className="px-1.5 py-0.5 bg-slate-100 border border-slate-300 rounded text-[10px] text-slate-700">←</kbd> e <kbd className="px-1.5 py-0.5 bg-slate-100 border border-slate-300 rounded text-[10px] text-slate-700">→</kbd> para navegar
              </span>
            </div>
          </div>
        </div>
      )}

      {/* ========================================================================= */}
      {/* MODO 2: DOSSIÊ COMPLETO & LINHA DO TEMPO CONTÍNUA                          */}
      {/* ========================================================================= */}
      {viewMode === 'dossier' && (
        <div className="space-y-8 animate-fadeIn">
          {/* Seção 0: A Jornada do Herói Tridimensional */}
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-5">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
              <div>
                <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <Trophy className="w-4 h-4 text-indigo-600" />
                  A Jornada do Herói Tridimensional: Negócio, CDO e Engenharia de Dados
                </h2>
                <p className="text-xs text-slate-500">
                  Como o projeto conduziu a organização da fragmentação regulatória ao Cockpit C-Level com custo zero de infraestrutura.
                </p>
              </div>
              <span className="px-2.5 py-1 rounded-full text-[11px] font-bold bg-amber-100 text-amber-900 border border-amber-300 flex items-center gap-1">
                <Sparkles className="w-3.5 h-3.5 text-amber-600" />
                9 Atos Estruturados
              </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {/* Card 1: Executivo de Negócio */}
              <div className="p-4 rounded-xl border border-amber-200 bg-amber-50/40 space-y-2.5">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-amber-900 uppercase tracking-wide flex items-center gap-1.5">
                    <Briefcase className="w-4 h-4 text-amber-600" />
                    👔 Executivo de Negócio (CEO/CFO)
                  </span>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-amber-200 text-amber-900">
                    ROI & FinOps
                  </span>
                </div>
                <p className="text-xs text-slate-700 leading-relaxed">
                  Transformou o tempo de resposta regulatória de semanas para sub-200ms. Evita multas de DEC/FEC, simula o WACC regulatório antes de audiências da ANEEL e opera com R$ 0,00 de custo fixo de infraestrutura.
                </p>
                <div className="pt-2 border-t border-amber-200 text-[11px] font-semibold text-amber-900">
                  🎯 Elixir: Blindagem de EBITDA & Agilidade Estratégica
                </div>
              </div>

              {/* Card 2: Chief Data Officer */}
              <div className="p-4 rounded-xl border border-indigo-200 bg-indigo-50/40 space-y-2.5">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-indigo-900 uppercase tracking-wide flex items-center gap-1.5">
                    <Shield className="w-4 h-4 text-indigo-600" />
                    🛡️ Chief Data Officer (CDO)
                  </span>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-indigo-200 text-indigo-900">
                    Governança & SSOT
                  </span>
                </div>
                <p className="text-xs text-slate-700 leading-relaxed">
                  Eliminou silos entre ANEEL, ONS, CCEE, CVM e BCB. Instituiu uma Single Source of Truth no BigQuery com Dataform SQLX assertions, contratos tipados de dados e prontidão para Agentes de Dados.
                </p>
                <div className="pt-2 border-t border-indigo-200 text-[11px] font-semibold text-indigo-900">
                  🎯 Elixir: Integridade de Dados & Single Source of Truth
                </div>
              </div>

              {/* Card 3: Líder de Engenharia */}
              <div className="p-4 rounded-xl border border-emerald-200 bg-emerald-50/40 space-y-2.5">
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-emerald-900 uppercase tracking-wide flex items-center gap-1.5">
                    <Wrench className="w-4 h-4 text-emerald-600" />
                    ⚙️ Líder de Engenharia de Dados
                  </span>
                  <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-emerald-200 text-emerald-900">
                    34 Testes Pass
                  </span>
                </div>
                <p className="text-xs text-slate-700 leading-relaxed">
                  Arquitetura Medallion serverless com Scale-to-Zero e BI Engine 2 GB in-memory. Suíte automatizada com 34 testes 100% aprovados, self-healing agêntico e Docker multi-stage build.
                </p>
                <div className="pt-2 border-t border-emerald-200 text-[11px] font-semibold text-emerald-900">
                  🎯 Elixir: Produtividade 15x & Zero Débito Técnico
                </div>
              </div>
            </div>
          </div>

          {/* Seção 1: Comparativo de Impacto e Produtividade */}
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
              <div>
                <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <TrendingUp className="w-4 h-4 text-emerald-600" />
                  Impacto Mensurável: Squad Tradicional vs Antigravity+Gemini
                </h2>
                <p className="text-xs text-slate-500">
                  Comparação real entre a abordagem manual de engenharia e o desenvolvimento agêntico assistido por IA.
                </p>
              </div>
              <span className="px-2.5 py-1 rounded-full text-[11px] font-bold bg-emerald-100 text-emerald-800 border border-emerald-200">
                Economia Comprovada
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-200 text-slate-400 font-bold uppercase text-[10px]">
                    <th className="py-2.5 px-3">Dimensão do Projeto</th>
                    <th className="py-2.5 px-3">Abordagem Tradicional</th>
                    <th className="py-2.5 px-3 text-blue-700">Aceleração com Antigravity+Gemini</th>
                    <th className="py-2.5 px-3 text-right">Ganho Obtido</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {comparisonData.map((row, idx) => (
                    <tr key={idx} className={row.highlight ? 'bg-blue-50/30' : ''}>
                      <td className="py-3 px-3 font-semibold text-slate-800">{row.metric}</td>
                      <td className="py-3 px-3 text-slate-500">{row.traditional}</td>
                      <td className="py-3 px-3 font-bold text-blue-800 flex items-center gap-1.5">
                        <Sparkles className="w-3.5 h-3.5 text-amber-500 shrink-0" />
                        {row.antigravity_gemini}
                      </td>
                      <td className="py-3 px-3 text-right font-black text-emerald-700">{row.multiplier}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Seção 2: Mapa de Impacto da IA Agêntica (Jetski & Data Cloud Tool Kit) */}
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
              <div>
                <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <Cpu className="w-4 h-4 text-purple-600" />
                  Mapa de Impacto da IA Agêntica (Jetski & Data Tool Kit)
                </h2>
                <p className="text-xs text-slate-500">
                  Matriz oficial da atuação do Antigravity e do Data Cloud Tool Kit nas 7 fases fundamentais do projeto.
                </p>
              </div>
              <span className="px-2.5 py-1 rounded-full text-[11px] font-bold bg-amber-100 text-amber-900 border border-amber-300 flex items-center gap-1">
                <Sparkles className="w-3.5 h-3.5 text-amber-600" />
                7 Fases Mapeadas
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs">
                <thead>
                  <tr className="border-b border-slate-200 text-slate-400 font-bold uppercase text-[10px] bg-slate-50/70">
                    <th className="py-2.5 px-3 w-1/3">Fase do Projeto</th>
                    <th className="py-2.5 px-3 w-2/3 text-blue-700">Papel da IA (Antigravity + Data Cloud Tool Kit)</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {aiImpactMap.map((item) => {
                    const Icon = item.icon;
                    return (
                      <tr key={item.id} className="hover:bg-blue-50/20 transition-colors">
                        <td className="py-3.5 px-3 align-top">
                          <div className="flex items-center gap-2 mb-1.5">
                            <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${item.badgeColor}`}>
                              {item.badge}
                            </span>
                            <div className="w-5 h-5 rounded bg-slate-100 flex items-center justify-center text-slate-600">
                              <Icon className="w-3 h-3 text-blue-600" />
                            </div>
                          </div>
                          <div className="font-bold text-slate-900 text-xs">{item.phase}</div>
                        </td>
                        <td className="py-3.5 px-3 align-top">
                          <ul className="space-y-1.5 text-slate-700">
                            {item.bullets.map((bullet, bIdx) => (
                              <li key={bIdx} className="flex items-start gap-1.5 leading-relaxed">
                                <span className="text-blue-600 font-bold">•</span>
                                <span>{bullet}</span>
                              </li>
                            ))}
                          </ul>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* Seção 3: Diagrama Interativo de Swimlanes de Arquitetura */}
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-4">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b border-slate-100 pb-3">
              <div>
                <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <Layers className="w-4 h-4 text-blue-600" />
                  Diagrama Interativo de Swimlanes da Arquitetura
                </h2>
                <p className="text-xs text-slate-500">
                  Clique nas raias para inspecionar cada componente, fluxo e contrato de dados.
                </p>
              </div>
              <span className="text-[11px] font-mono text-slate-400">docs/architecture.drawio</span>
            </div>

            <div className="space-y-3">
              {swimlanes.map((lane) => {
                const Icon = lane.icon;
                const isSelected = activeSwimlane === lane.id;
                return (
                  <div
                    key={lane.id}
                    onClick={() => setActiveSwimlane(isSelected ? null : lane.id)}
                    className={`rounded-xl border p-4 transition-all cursor-pointer ${
                      isSelected
                        ? `${lane.color} shadow-md border-blue-400 ring-2 ring-blue-500/20`
                        : 'border-slate-200 bg-slate-50/50 hover:bg-slate-100/60'
                    }`}
                  >
                    <div className="flex items-center justify-between">
                      <div className="flex items-center gap-3">
                        <div className="w-7 h-7 rounded-lg bg-white shadow-xs border border-slate-200 flex items-center justify-center text-slate-700">
                          <Icon className="w-4 h-4 text-blue-600" />
                        </div>
                        <div>
                          <h3 className="text-xs font-bold text-slate-900">{lane.title}</h3>
                          <span className="text-[10px] text-slate-500">{lane.tag}</span>
                        </div>
                      </div>
                      <span className="text-xs font-semibold text-blue-600">
                        {isSelected ? 'Ocultar Detalhes ↑' : 'Inspecionar Nós ↓'}
                      </span>
                    </div>

                    {/* Detalhes dos nós ao clicar */}
                    {isSelected && (
                      <div className="mt-4 pt-3 border-t border-slate-200/80 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3 animate-fadeIn">
                        {lane.nodes.map((node, nodeIdx) => (
                          <div key={nodeIdx} className="bg-white p-3 rounded-lg border border-slate-200 shadow-2xs">
                            <div className="font-bold text-xs text-slate-800">{node.name}</div>
                            <div className="text-[11px] text-slate-500 mt-1 leading-relaxed">{node.desc}</div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Seção 4: Linha do Tempo Cronológica Completa das Sprints */}
          <div className="bg-white rounded-2xl border border-slate-200 shadow-sm p-6 space-y-5">
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 border-b border-slate-100 pb-3">
              <div>
                <h2 className="text-base font-bold text-slate-900 flex items-center gap-2">
                  <Workflow className="w-4 h-4 text-purple-600" />
                  Linha do Tempo Cronológica das Sprints
                </h2>
                <p className="text-xs text-slate-500">
                  Histórico verificado via commits do Git, entregáveis técnicos e atuação da IA Antigravity+Gemini.
                </p>
              </div>

              {/* Filtro por Sprint */}
              <div className="flex items-center gap-1.5 flex-wrap">
                <Filter className="w-3.5 h-3.5 text-slate-400" />
                <span className="text-xs text-slate-500 mr-1">Filtro:</span>
                {['all', 'fase-0', 'fase-1', 'sprint-1', 'sprint-2', 'sprint-3', 'fase-proret'].map((f) => (
                  <button
                    key={f}
                    onClick={() => setSelectedSprintFilter(f)}
                    className={`px-2.5 py-1 rounded-lg text-[10px] font-bold transition-all ${
                      selectedSprintFilter === f
                        ? 'bg-blue-600 text-white shadow-xs'
                        : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
                    }`}
                  >
                    {f === 'all' ? 'Todas' : f.toUpperCase()}
                  </button>
                ))}
              </div>
            </div>

            {/* Itens da Timeline */}
            <div className="space-y-4">
              {filteredSprints.map((sprint) => (
                <div
                  key={sprint.id}
                  className="p-5 rounded-xl border border-slate-200 bg-slate-50/70 hover:bg-slate-50 transition-all space-y-3"
                >
                  <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-2">
                    <div className="flex items-center gap-2.5 flex-wrap">
                      <span className={`text-[10px] font-bold px-2 py-0.5 rounded border ${sprint.badgeColor}`}>
                        {sprint.badge}
                      </span>
                      <h3 className="font-bold text-sm text-slate-900">{sprint.title}</h3>
                    </div>
                    <div className="flex items-center gap-2 text-[11px] text-slate-500">
                      <Calendar className="w-3.5 h-3.5 text-slate-400" />
                      <span>{sprint.period}</span>
                      <span className="font-mono text-[10px] bg-slate-200 px-1.5 py-0.5 rounded text-slate-700">
                        {sprint.commitHash}
                      </span>
                    </div>
                  </div>

                  <p className="text-xs text-slate-700 leading-relaxed">{sprint.description}</p>

                  {/* Entregáveis */}
                  <div className="bg-white p-3 rounded-lg border border-slate-200">
                    <div className="text-[11px] font-bold text-slate-800 uppercase tracking-wider mb-1.5">
                      Entregáveis Técnicos:
                    </div>
                    <ul className="grid grid-cols-1 sm:grid-cols-2 gap-1.5 text-xs text-slate-600">
                      {sprint.deliverables.map((item, dIdx) => (
                        <li key={dIdx} className="flex items-start gap-1.5">
                          <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600 shrink-0 mt-0.5" />
                          <span>{item}</span>
                        </li>
                      ))}
                    </ul>
                  </div>

                  {/* O Papel da IA nesta Sprint */}
                  <div className="p-3 rounded-lg bg-amber-500/10 border border-amber-500/30 flex items-start gap-2.5">
                    <Sparkles className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                    <div className="text-xs text-slate-800">
                      <strong className="text-amber-900">⚡ Atuação da IA Antigravity+Gemini:</strong> {sprint.aiRole}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProjectStory;
