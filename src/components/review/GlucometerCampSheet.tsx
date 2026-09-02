import React from 'react';
import { Activity } from 'lucide-react';

const PATIENTS = [
  { sn: 1, name: 'OM PRAKASH RANAWAT', phone: '-', brand: 'LINAGET', strips: '-' },
  { sn: 2, name: 'GURUSIKHA SALVI', phone: '-', brand: 'LINAGET', strips: '-' },
  { sn: 3, name: 'NILESH ARCHARIA', phone: '-', brand: 'LINAGET', strips: '-' },
  { sn: 4, name: 'KANTI LAL SHARMA', phone: '-', brand: 'LINAGET', strips: '-' },
  { sn: 5, name: 'BHERU PRASAD', phone: '-', brand: 'LINAGET', strips: '-' }
];

export const GlucometerCampSheet: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <span className="p-2 bg-teal-500/20 text-teal-400 rounded-lg"><Activity size={18} /></span>
          <h2 className="text-base font-bold text-white">10. GLUCOMETER CAMPAIGN (LINAGET)</h2>
        </div>
        <div className="text-xs text-slate-400 font-mono">Dr. Mona Dhingra (Endocrinologist, Udaipur)</div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800">
              <th className="p-2.5 w-10 text-center">S.N.</th>
              <th className="p-2.5">Patient Name</th>
              <th className="p-2.5">Phone No.</th>
              <th className="p-2.5">Brand Prescribed</th>
              <th className="p-2.5 text-center">Strips Sold</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {PATIENTS.map(p => (
              <tr key={p.sn} className="hover:bg-slate-800/40 transition">
                <td className="p-2.5 text-center text-slate-500 font-mono">{p.sn}</td>
                <td className="p-2.5 font-semibold text-white">{p.name}</td>
                <td className="p-2.5 text-slate-400">{p.phone}</td>
                <td className="p-2.5 text-cyan-400 font-bold">{p.brand}</td>
                <td className="p-2.5 text-center font-mono text-slate-300">{p.strips}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
