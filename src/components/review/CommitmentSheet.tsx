import React from 'react';
import { CheckCircle2 } from 'lucide-react';

const DOCTORS_SUPPORT = [
  { sn: 1, hq: 'UDAIPUR', name: 'JIMESH PANDYA', type: 'GIFT CARDS', amount: 30000, roi: 15000 },
  { sn: 2, hq: 'UDAIPUR', name: 'VIJAY GOYAL', type: 'GIFT CARDS', amount: 10000, roi: 10000 },
  { sn: 3, hq: 'UDAIPUR', name: 'JAYESH GANDHI', type: 'SPECIAL PLAN', amount: 50000, roi: 50000 },
  { sn: 4, hq: 'UDAIPUR', name: 'AK VATS', type: 'GIFT CARDS', amount: 30000, roi: 15000 },
  { sn: 5, hq: 'UDAIPUR', name: 'SANDEEP BHATNAGAR', type: 'GIFT CARDS', amount: 30000, roi: 150000 },
  { sn: 6, hq: 'UDAIPUR', name: 'RK MALOT', type: 'GIFT CARDS', amount: 40000, roi: 20000 },
  { sn: 7, hq: 'UDAIPUR', name: 'BS BOMB', type: 'GIFT CARDS (VINTEL)', amount: 50000, roi: 30000 },
  { sn: 8, hq: 'UDAIPUR', name: 'RAHUL PANCHAL', type: 'GIFT CARDS', amount: 30000, roi: 15000 },
  { sn: 9, hq: 'UDAIPUR', name: 'KC JAIN', type: 'SPECIAL PLAN', amount: 20000, roi: 20000 },
  { sn: 10, hq: 'UDAIPUR', name: 'DP SINGH', type: 'GIFT CARDS', amount: 30000, roi: 15000 },
  { sn: 11, hq: 'UDAIPUR', name: 'JC DEVPURA', type: 'GIFT CARDS', amount: 10000, roi: 10000 },
  { sn: 12, hq: 'UDAIPUR', name: 'BALDEV MEENA', type: 'TREAD MILL', amount: 85000, roi: 50000 },
  { sn: 13, hq: 'UDAIPUR', name: 'KRIPA SHANKAR', type: 'GIFT CARDS', amount: 20000, roi: 10000 },
];

export const CommitmentSheet: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-6">
      <div>
        <div className="flex items-center gap-2 mb-3">
          <span className="p-2 bg-emerald-500/20 text-emerald-400 rounded-lg"><CheckCircle2 size={18} /></span>
          <h2 className="text-base font-bold text-white">6. COMMITMENT OF MONTH</h2>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800">
                <th className="p-2.5">H.Q. NAME</th>
                <th className="p-2.5 text-center">Prev Month Budget</th>
                <th className="p-2.5 text-center">Prev Month Ach.</th>
                <th className="p-2.5 text-center">Current Sec</th>
                <th className="p-2.5 text-center">Current Inventory</th>
                <th className="p-2.5 text-center">Current Budget</th>
                <th className="p-2.5 text-center text-emerald-400">Commitment</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b border-slate-800">
                <td className="p-2.5 font-bold text-white">UDAIPUR</td>
                <td className="p-2.5 text-center font-mono">4.83</td>
                <td className="p-2.5 text-center font-mono text-cyan-400">4.84</td>
                <td className="p-2.5 text-center font-mono">4.85</td>
                <td className="p-2.5 text-center font-mono">7.01</td>
                <td className="p-2.5 text-center font-mono">4.83</td>
                <td className="p-2.5 text-center font-mono font-bold text-emerald-400">5.50</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      <div>
        <h3 className="text-sm font-bold text-white mb-3">Doctor Support &amp; Expected ROI</h3>
        <div className="overflow-x-auto max-h-[400px]">
          <table className="w-full text-left text-xs border-collapse">
            <thead className="sticky top-0 bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800">
              <tr>
                <th className="p-2.5 w-10 text-center">S.N.</th>
                <th className="p-2.5">Doctor Name</th>
                <th className="p-2.5">Type of Support</th>
                <th className="p-2.5 text-right">Amount (₹)</th>
                <th className="p-2.5 text-right text-emerald-400">Expected ROI (₹)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {DOCTORS_SUPPORT.map(doc => (
                <tr key={doc.sn} className="hover:bg-slate-800/40 transition">
                  <td className="p-2.5 text-center text-slate-500 font-mono">{doc.sn}</td>
                  <td className="p-2.5 font-semibold text-white">{doc.name}</td>
                  <td className="p-2.5 text-slate-300">{doc.type}</td>
                  <td className="p-2.5 text-right font-mono text-slate-300">₹{doc.amount.toLocaleString()}</td>
                  <td className="p-2.5 text-right font-mono font-bold text-emerald-400">₹{doc.roi.toLocaleString()}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
