import React, { useState } from 'react';
import { Calendar, Search } from 'lucide-react';

const MSL_DOCTORS = [
  { sn: 1, name: 'MAHESH DAVE', activity: 'CRM', spec: 'MD MED', apr: '1,10,17', may: '15,19,26,30', jun: 'na,13,25,30' },
  { sn: 2, name: 'DP SINGH', activity: 'CRM', spec: 'MD MED', apr: '7,23,27', may: '6,11,21,29,30', jun: '15,24,29' },
  { sn: 3, name: 'KAVITA BADJATIYA', activity: 'CRM', spec: 'MD MED', apr: '1,7,13,18,20', may: '4,11,21,27', jun: '9,13,15,22,29' },
  { sn: 4, name: 'NAVGEET MATHUR', activity: 'CRM', spec: 'MD MED', apr: '3,11', may: 'na out of town', jun: 'na,13,19' },
  { sn: 5, name: 'PARAS JAIN', activity: 'CRM', spec: 'MD MED', apr: '4,15,24', may: '14,26', jun: '1,24' },
  { sn: 6, name: 'BS BOMB', activity: 'CRM', spec: 'MD MED', apr: '4,11,15', may: '8,14,18', jun: '1,18' },
  { sn: 7, name: 'D C SHARMA', activity: 'CRM', spec: 'DM ENDO', apr: '3,9,10', may: '7,12,28', jun: '12,18,ntc' },
  { sn: 8, name: 'SANDEEP KANSARA', activity: 'CRM+LGT TABLE TOP', spec: 'DM ENDO', apr: '11,23', may: '14,21', jun: '2,9,24' },
  { sn: 9, name: 'VINOD MEHTA', activity: 'CRM', spec: 'DM NEURO', apr: '2,3,11,17', may: '14,15,26,29', jun: 'na,16,18,19,29' },
  { sn: 10, name: 'AKVATS', activity: 'CRM', spec: 'DM NEURO', apr: '1,15,23,30', may: '6,14,21', jun: '3,18,24' },
  { sn: 11, name: 'RAMESH PATEL', activity: 'CRM', spec: 'DM CARDIO', apr: '1,17,22', may: '8,15,18,19,29', jun: '12,19,24' },
  { sn: 12, name: 'DENY', activity: 'CRM', spec: 'DM CARDIO', apr: '9,10,24,30', may: '8,19,26,29', jun: '12,18,25' },
];

export const MslSheet: React.FC = () => {
  const [search, setSearch] = useState('');
  const filtered = MSL_DOCTORS.filter(d => d.name.toLowerCase().includes(search.toLowerCase()) || d.spec.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <span className="p-2 bg-cyan-500/20 text-cyan-400 rounded-lg"><Calendar size={18} /></span>
          <h2 className="text-base font-bold text-white">14. MSL (Master Specialty List &amp; Visit Dates)</h2>
        </div>
        <div className="relative w-full sm:w-60">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
          <input 
            type="text" 
            placeholder="Search doctor or speciality..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-8 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
          />
        </div>
      </div>
      <div className="overflow-x-auto max-h-[500px]">
        <table className="w-full text-left text-xs border-collapse">
          <thead className="sticky top-0 bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800 z-10">
            <tr>
              <th className="p-2.5 w-10 text-center">S.N.</th>
              <th className="p-2.5">Doctor Name</th>
              <th className="p-2.5">Activity</th>
              <th className="p-2.5">Speciality</th>
              <th className="p-2.5 text-center text-cyan-400">APR</th>
              <th className="p-2.5 text-center text-emerald-400">MAY</th>
              <th className="p-2.5 text-center text-purple-400">JUN</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {filtered.map(row => (
              <tr key={row.sn} className="hover:bg-slate-800/40 transition">
                <td className="p-2.5 text-center text-slate-500 font-mono">{row.sn}</td>
                <td className="p-2.5 font-semibold text-white">{row.name}</td>
                <td className="p-2.5 text-amber-400">{row.activity}</td>
                <td className="p-2.5 text-slate-300">{row.spec}</td>
                <td className="p-2.5 text-center font-mono text-slate-300">{row.apr}</td>
                <td className="p-2.5 text-center font-mono text-slate-300">{row.may}</td>
                <td className="p-2.5 text-center font-mono text-slate-300">{row.jun}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
