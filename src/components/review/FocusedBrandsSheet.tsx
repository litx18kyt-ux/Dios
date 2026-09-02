import React from 'react';
import { Target } from 'lucide-react';

const FOCUSED = [
  { sn: 1, dr: 'ABHIJEET BASU', product: 'CALGYM 60K', spec: 'GP' },
  { sn: 2, dr: 'AMIT MEHTA', product: 'CALGYM 60K', spec: 'GP' },
  { sn: 3, dr: 'ANISH BAHL', product: 'CALGYM 60K', spec: 'GP' },
  { sn: 4, dr: 'JAGDISH VISHNOI', product: 'CALGYM 60K', spec: 'GP' },
  { sn: 5, dr: 'LALIT SHREEMALI', product: 'CALGYM 60K', spec: 'GP' },
  { sn: 6, dr: 'KB BADOLIYA', product: 'DIOFLAM', spec: 'GP' },
  { sn: 7, dr: 'RAVI MANGALIYA', product: 'DIOFLAM', spec: 'GP' },
  { sn: 8, dr: 'YN VERMA', product: 'DIOFLAM', spec: 'GP' },
  { sn: 9, dr: 'RN LADDHA', product: 'DIOFLAM', spec: 'GP' },
  { sn: 10, dr: 'LALIT SHRIMALI', product: 'DIOFLAM', spec: 'GP' },
  { sn: 11, dr: 'POOJA GANDHI', product: 'FITJEE Q10', spec: 'PHY/GYN/GP' },
  { sn: 12, dr: 'RADHA RASTOGI', product: 'FITJEE Q10', spec: 'PHY/GYN/GP' },
  { sn: 13, dr: 'LALIT JAINANI', product: 'FITJEE Q10', spec: 'PHY/GYN/GP' },
  { sn: 14, dr: 'ANMOL PAGARIYA', product: 'FITJEE Q10', spec: 'PHY/GYN/GP' },
  { sn: 15, dr: 'BS BOMB', product: 'FITJEE Q10', spec: 'PHY/GYN/GP' }
];

export const FocusedBrandsSheet: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <span className="p-2 bg-indigo-500/20 text-indigo-400 rounded-lg"><Target size={18} /></span>
          <h2 className="text-base font-bold text-white">12. FOCUSED BRANDS (Doctor-wise Rx)</h2>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800">
              <th className="p-2.5 w-10 text-center">S.N.</th>
              <th className="p-2.5">Doctor Name</th>
              <th className="p-2.5">Product Name</th>
              <th className="p-2.5">Speciality</th>
              <th className="p-2.5 text-center">Status</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {FOCUSED.map(row => (
              <tr key={row.sn} className="hover:bg-slate-800/40 transition">
                <td className="p-2.5 text-center text-slate-500 font-mono">{row.sn}</td>
                <td className="p-2.5 font-semibold text-white">{row.dr}</td>
                <td className="p-2.5 text-cyan-400 font-bold">{row.product}</td>
                <td className="p-2.5 text-slate-300">{row.spec}</td>
                <td className="p-2.5 text-center text-emerald-400 font-semibold">Active</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
