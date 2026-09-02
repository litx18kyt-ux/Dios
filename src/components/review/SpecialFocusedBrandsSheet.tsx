import React from 'react';
import { TrendingUp } from 'lucide-react';

const PRI_BRANDS = [
  { sn: 1, name: 'VINTEL', jm: 3246, apr: 1650, may: 1498, jun: 2195, qtr: 5343, growth: '64.6%' },
  { sn: 2, name: 'VINVES', jm: 0, apr: 0, may: 0, jun: 0, qtr: 0, growth: '-' },
  { sn: 3, name: 'LINAGET', jm: 214, apr: 62, may: 84, jun: 96, qtr: 242, growth: '13.1%' },
  { sn: 4, name: 'VALROS', jm: 817, apr: 352, may: 430, jun: 445, qtr: 1227, growth: '50.2%' },
  { sn: 5, name: 'DIOSGLT', jm: 0, apr: 0, may: 65, jun: 0, qtr: 65, growth: '-' },
];

const SEC_BRANDS = [
  { sn: 1, name: 'VINTEL', jm: 4819, apr: 2023, may: 1709, jun: 1717, qtr: 5449, growth: '13.1%' },
  { sn: 2, name: 'VINVES', jm: 21, apr: 2, may: 0, jun: 0, qtr: 2, growth: '-90.5%' },
  { sn: 3, name: 'LINAGET', jm: 390, apr: 153, may: 130, jun: 186, qtr: 469, growth: '20.3%' },
  { sn: 4, name: 'VALROS', jm: 1234, apr: 509, may: 361, jun: 502, qtr: 1372, growth: '11.2%' },
  { sn: 5, name: 'DIOSGLT', jm: 71, apr: 8, may: 39, jun: 15, qtr: 62, growth: '-12.7%' },
];

export const SpecialFocusedBrandsSheet: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-6">
      <div>
        <h2 className="text-base font-bold text-white mb-3">11. SPECIAL FOCUSED BRANDS - PRIMARY (IN STRIPS)</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800">
                <th className="p-2.5 w-10 text-center">S.N.</th>
                <th className="p-2.5">Product Name</th>
                <th className="p-2.5 text-center">Jan-Mar Sale</th>
                <th className="p-2.5 text-center">APR</th>
                <th className="p-2.5 text-center">MAY</th>
                <th className="p-2.5 text-center">JUN</th>
                <th className="p-2.5 text-center text-blue-400">Qtr Sale</th>
                <th className="p-2.5 text-center text-emerald-400">% Growth</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {PRI_BRANDS.map(row => (
                <tr key={row.sn} className="hover:bg-slate-800/40 transition">
                  <td className="p-2.5 text-center text-slate-500 font-mono">{row.sn}</td>
                  <td className="p-2.5 font-semibold text-white">{row.name}</td>
                  <td className="p-2.5 text-center font-mono text-slate-400">{row.jm}</td>
                  <td className="p-2.5 text-center font-mono">{row.apr}</td>
                  <td className="p-2.5 text-center font-mono">{row.may}</td>
                  <td className="p-2.5 text-center font-mono">{row.jun}</td>
                  <td className="p-2.5 text-center font-mono font-bold text-blue-400">{row.qtr}</td>
                  <td className="p-2.5 text-center font-mono font-bold text-emerald-400">{row.growth}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      <div>
        <h2 className="text-base font-bold text-white mb-3">SPECIAL FOCUSED BRANDS - SECONDARY (IN STRIPS)</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800">
                <th className="p-2.5 w-10 text-center">S.N.</th>
                <th className="p-2.5">Product Name</th>
                <th className="p-2.5 text-center">Jan-Mar Sale</th>
                <th className="p-2.5 text-center">APR</th>
                <th className="p-2.5 text-center">MAY</th>
                <th className="p-2.5 text-center">JUN</th>
                <th className="p-2.5 text-center text-cyan-400">Qtr Sale</th>
                <th className="p-2.5 text-center text-emerald-400">% Growth</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {SEC_BRANDS.map(row => (
                <tr key={row.sn} className="hover:bg-slate-800/40 transition">
                  <td className="p-2.5 text-center text-slate-500 font-mono">{row.sn}</td>
                  <td className="p-2.5 font-semibold text-white">{row.name}</td>
                  <td className="p-2.5 text-center font-mono text-slate-400">{row.jm}</td>
                  <td className="p-2.5 text-center font-mono">{row.apr}</td>
                  <td className="p-2.5 text-center font-mono">{row.may}</td>
                  <td className="p-2.5 text-center font-mono">{row.jun}</td>
                  <td className="p-2.5 text-center font-mono font-bold text-cyan-400">{row.qtr}</td>
                  <td className="p-2.5 text-center font-mono font-bold text-emerald-400">{row.growth}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
