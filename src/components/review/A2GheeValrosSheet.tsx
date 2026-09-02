import React from 'react';
import { Layers } from 'lucide-react';

const A2_ROWS = [
  { sn: 1, name: 'SANJAY GANDHI', hq: 'UDAIPUR', spec: 'CARDIOLOGIST', date: '13-Jun', status: 'NON' },
  { sn: 2, name: 'SK KAUSHIQ', hq: 'UDAIPUR', spec: 'CARD', date: '13-Jun', status: 'NON' }
];

export const A2GheeValrosSheet: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <span className="p-2 bg-yellow-500/20 text-yellow-400 rounded-lg"><Layers size={18} /></span>
          <h2 className="text-base font-bold text-white">8. A2 GHEE VALROS CAMPAIGN</h2>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800">
              <th className="p-2.5 w-10 text-center">S.N.</th>
              <th className="p-2.5">Doctor Name</th>
              <th className="p-2.5">HQ</th>
              <th className="p-2.5">Speciality</th>
              <th className="p-2.5 text-center">Date of Activity</th>
              <th className="p-2.5 text-center">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {A2_ROWS.map(row => (
              <tr key={row.sn} className="hover:bg-slate-800/40 transition">
                <td className="p-2.5 text-center text-slate-500 font-mono">{row.sn}</td>
                <td className="p-2.5 font-semibold text-white">{row.name}</td>
                <td className="p-2.5 text-slate-300">{row.hq}</td>
                <td className="p-2.5 text-slate-300">{row.spec}</td>
                <td className="p-2.5 text-center font-mono text-cyan-400">{row.date}</td>
                <td className="p-2.5 text-center font-semibold text-amber-400">{row.status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
