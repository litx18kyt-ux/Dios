import React from 'react';
import { Layers } from 'lucide-react';

const LINAGET_LIST = [
  { sn: 1, name: 'SANDEEP KANSARA', hq: 'UDAIPUR', spec: 'ENDO', status: 'DONE' },
  { sn: 2, name: 'VINOD BOKADIYA', hq: 'UDAIPUR', spec: 'ENDO', status: 'DONE' },
  { sn: 3, name: 'JAI CHORDIYA', hq: 'UDAIPUR', spec: 'ENDO', status: 'PENDING' }
];

const VINTEL_LIST = [
  { sn: 1, name: 'MANISH KULSHRESHT', hq: 'UDAIPUR', spec: 'NEURO', status: 'DONE' },
  { sn: 2, name: 'JITESH AGRAWAL', hq: 'UDAIPUR', spec: 'PHY', status: 'DONE' },
  { sn: 3, name: 'SATISH CHOUDHARY', hq: 'UDAIPUR', spec: 'PHY', status: 'DONE' }
];

export const TableTopSheet: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-6">
      <div>
        <h2 className="text-base font-bold text-white mb-3">9. TABLE TOP CAMPAIGN (LINAGET)</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800">
                <th className="p-2.5 w-10 text-center">S.N.</th>
                <th className="p-2.5">Doctor Name</th>
                <th className="p-2.5">HQ</th>
                <th className="p-2.5">Speciality</th>
                <th className="p-2.5 text-center">Activity Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {LINAGET_LIST.map(item => (
                <tr key={item.sn} className="hover:bg-slate-800/40 transition">
                  <td className="p-2.5 text-center text-slate-500 font-mono">{item.sn}</td>
                  <td className="p-2.5 font-semibold text-white">{item.name}</td>
                  <td className="p-2.5 text-slate-300">{item.hq}</td>
                  <td className="p-2.5 text-slate-300">{item.spec}</td>
                  <td className="p-2.5 text-center font-bold text-emerald-400">{item.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div>
        <h2 className="text-base font-bold text-white mb-3">TABLE TOP CAMPAIGN (VINTEL)</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800">
                <th className="p-2.5 w-10 text-center">S.N.</th>
                <th className="p-2.5">Doctor Name</th>
                <th className="p-2.5">HQ</th>
                <th className="p-2.5">Speciality</th>
                <th className="p-2.5 text-center">Activity Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {VINTEL_LIST.map(item => (
                <tr key={item.sn} className="hover:bg-slate-800/40 transition">
                  <td className="p-2.5 text-center text-slate-500 font-mono">{item.sn}</td>
                  <td className="p-2.5 font-semibold text-white">{item.name}</td>
                  <td className="p-2.5 text-slate-300">{item.hq}</td>
                  <td className="p-2.5 text-slate-300">{item.spec}</td>
                  <td className="p-2.5 text-center font-bold text-emerald-400">{item.status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
