import React, { useState } from 'react';
import { MainHub } from './components/MainHub';
import { DiosWorkspace } from './components/DiosWorkspace';

export default function App() {
  const [activeProject, setActiveProject] = useState<string | null>(null);

  if (activeProject === 'dios') {
    return <DiosWorkspace onBack={() => setActiveProject(null)} />;
  }

  return <MainHub onOpenProject={(id) => setActiveProject(id)} />;
}
