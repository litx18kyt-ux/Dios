import React, { useState } from 'react';
import { Search, FolderGit2, ChevronRight, Activity, ShieldCheck } from 'lucide-react';

interface Props {
  onOpenProject: (projectId: string) => void;
}

export const MainHub: React.FC<Props> = ({ onOpenProject }) => {
  const [hubSearch, setHubSearch] = useState('');

  const projects = [
    {
      id: 'dios',
      name: 'dios',
      description: 'Unit Sales Progression (HQ Total) aggregator for Nagda, Dwarika, Sun, RP, Modi & Vardhman.',
      category: 'Pharma Analytics',
      status: 'Live (v26.0 2-Tier Breakdown)'
    }
  ];

  const filteredProjects = projects.filter(p =>
    p.name.toLowerCase().includes(hubSearch.toLowerCase()) ||
    p.description.toLowerCase().includes(hubSearch.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 md:p-12 max-w-6xl mx-auto">
      {/* 🚀 LIVE V26.0 BANNER */}
      <div className="mb-6 p-4 rounded-2xl bg-gradient-to-r from-cyan-950 via-slate-900 to-emerald-950 border border-cyan-500/40 shadow-xl flex items-center justify-between">
        <div className="flex items-center gap-3">
          <span className="p-2.5 bg-emerald-500/20 text-emerald-400 rounded-xl border border-emerald-500/30">
            <Activity size={22} className="animate-pulse" />
          </span>
          <div>
            <div className="text-xs font-black tracking-wide text-emerald-400 uppercase flex items-center gap-2">
              <span>● SYSTEM V26.0 LIVE</span>
              <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-2.5 py-0.5 rounded-full border border-emerald-500/30">2-TIER PARTY BREAKDOWN ACTIVE</span>
            </div>
            <p className="text-xs text-slate-300 mt-0.5">
              Party Name Banner • SEC & CLOSING Sub-Headers • Side-by-Side Stock & Sales Excel
            </p>
          </div>
        </div>
        <div className="hidden sm:flex items-center gap-2 text-xs text-slate-400">
          <ShieldCheck size={16} className="text-cyan-400" /> Cloudflare Production
        </div>
      </div>

      <header className="flex flex-col md:flex-row md:items-center justify-between gap-4 mb-8 pb-6 border-b border-slate-800">
        <div>
          <h1 className="text-3xl font-extrabold text-white flex items-center gap-3">
            <FolderGit2 className="text-cyan-400" size={32} />
            Dev Workspace Hub
          </h1>
          <p className="text-slate-400 text-sm mt-1">iPad Codespace Managed Multi-Project Platform</p>
        </div>
      </header>

      <div className="relative mb-8">
        <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400" size={20} />
        <input
          type="text"
          placeholder="Search projects (e.g. dios)..."
          value={hubSearch}
          onChange={(e) => setHubSearch(e.target.value)}
          className="w-full bg-slate-900 border border-slate-800 rounded-xl pl-12 pr-4 py-3 text-slate-100 placeholder-slate-500 focus:outline-none focus:border-cyan-500"
        />
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {filteredProjects.map((project) => (
          <div
            key={project.id}
            onClick={() => onOpenProject(project.id)}
            className="group bg-slate-900/80 border border-slate-800 hover:border-cyan-500 hover:bg-slate-900 rounded-2xl p-6 transition duration-200 cursor-pointer shadow-lg hover:shadow-cyan-500/10 flex flex-col justify-between"
          >
            <div>
              <div className="flex items-center justify-between mb-4">
                <span className="text-xs font-semibold px-2.5 py-1 rounded-md bg-cyan-500/20 text-cyan-400 border border-cyan-500/30">
                  Pharma Analytics
                </span>
                <ChevronRight size={18} className="text-slate-500 group-hover:text-cyan-400 group-hover:translate-x-1 transition" />
              </div>
              <h2 className="text-2xl font-bold text-white group-hover:text-cyan-400 transition mb-2">
                {project.name}
              </h2>
              <p className="text-slate-400 text-sm leading-relaxed">
                {project.description}
              </p>
            </div>

            <div className="mt-6 pt-4 border-t border-slate-800 flex items-center justify-between text-xs">
              <span className="text-emerald-400 font-medium">{project.status}</span>
              <span className="text-cyan-400 font-bold group-hover:translate-x-1 transition">Open Workspace &rarr;</span>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
