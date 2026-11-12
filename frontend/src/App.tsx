import { useState } from 'react';
import { Sidebar } from './components/layout/Sidebar';
import type { TabKey } from './components/layout/Sidebar';
import { Header } from './components/layout/Header';
import type { SubsystemId } from './types';
import { ExecutiveOverview } from './pages/ExecutiveOverview';
import { SinOperation } from './pages/SinOperation';
import { CceeMarket } from './pages/CceeMarket';
import { Transmission } from './pages/Transmission';
import { DistributionQuality } from './pages/DistributionQuality';
import { LossesMmgd } from './pages/LossesMmgd';
import { CustomerService } from './pages/CustomerService';
import { FinancialProret } from './pages/FinancialProret';
import { AlertsCenter } from './pages/AlertsCenter';
import { ProjectStory } from './pages/ProjectStory';

export function App() {
  const [activeTab, setActiveTab] = useState<TabKey>('executive');
  const [selectedSubsystem, setSelectedSubsystem] = useState<SubsystemId>('SIN');
  const [isRefreshing, setIsRefreshing] = useState(false);
  const [refreshKey, setRefreshKey] = useState(0);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => {
      setRefreshKey(prev => prev + 1);
      setIsRefreshing(false);
    }, 600);
  };

  return (
    <div className="flex h-screen bg-slate-50 font-sans overflow-hidden">
      {/* Sidebar */}
      <Sidebar
        activeTab={activeTab}
        onSelectTab={setActiveTab}
        alertCount={5}
      />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 overflow-y-auto">
        <Header
          selectedSubsystem={selectedSubsystem}
          onSelectSubsystem={setSelectedSubsystem}
          onRefresh={handleRefresh}
          isRefreshing={isRefreshing}
        />

        <main className="flex-1 p-6 max-w-7xl w-full mx-auto" key={refreshKey}>
          {activeTab === 'executive' && (
            <ExecutiveOverview
              selectedSubsystem={selectedSubsystem}
              onSelectSubsystem={setSelectedSubsystem}
              onNavigateTab={setActiveTab}
            />
          )}
          {activeTab === 'sin' && <SinOperation selectedSubsystem={selectedSubsystem} />}
          {activeTab === 'ccee' && <CceeMarket selectedSubsystem={selectedSubsystem} />}
          {activeTab === 'transmissao' && <Transmission />}
          {activeTab === 'distribuicao' && <DistributionQuality selectedSubsystem={selectedSubsystem} />}
          {activeTab === 'perdas_mmgd' && <LossesMmgd selectedSubsystem={selectedSubsystem} />}
          {activeTab === 'atendimento' && <CustomerService />}
          {activeTab === 'financeiro_proret' && <FinancialProret />}
          {activeTab === 'alerts' && <AlertsCenter />}
          {activeTab === 'project_story' && <ProjectStory onNavigateTab={setActiveTab} />}
        </main>
      </div>
    </div>
  );
}

export default App;
