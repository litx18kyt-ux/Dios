import React, { useState } from 'react';
import { DollarSign, Search } from 'lucide-react';

const ROI_DATA = [
  { sn: 1, dr: 'ABHAY JAIN', mobile: '7014694989', type: 'CASH', amount: '50000/120000', apr: 35000, may: 20000, jun: 10000, jul: 10000, total: 180000 },
  { sn: 2, dr: 'ABHIJEET BASU', mobile: '9352517070', type: 'GIFT CARDS', amount: '20000, 20000', apr: 5000, may: 3000, jun: 5000, jul: 3000, total: 7900 },
  { sn: 3, dr: 'AK VATS', mobile: '9829279719', type: 'GIFT CARDS', amount: '30000', apr: 8000, may: 8000, jun: 5000, jul: 5000, total: 86900 },
  { sn: 4, dr: 'AMIT MEHTA', mobile: '9879188503', type: 'DINNER', amount: '3200', apr: 4500, may: 4000, jun: 3000, jul: 1000, total: 6600 },
  { sn: 5, dr: 'BALDEV MEENA', mobile: '9549609251', type: 'IPHONE', amount: '75000', apr: 22000, may: 25000, jun: 30000, jul: 22000, total: 251500 },
  { sn: 6, dr: 'BS BOMB', mobile: '9352500310', type: 'GIFT CARDS', amount: '30000', apr: 6000, may: 9000, jun: 6000, jul: 3000, total: 94000 },
  { sn: 7, dr: 'JAYESH GANDHI', mobile: '7014111410', type: 'CASH', amount: '100000', apr: 30000, may: 30000, jun: 30000, jul: 30000, total: 592000 },
  { sn: 8, dr: 'KIRIT GANDHI', mobile: '7976280712', type: 'CASH', amount: '50000/50000', apr: 20000, may: 15000, jun: 15000, jul: 15000, total: 319000 },
  { sn: 9, dr: 'SUMIT SIROYA', mobile: '8529490073', type: 'GIFT CARDS', amount: '40000', apr: 25000, may: 25000, jun: 30000, jul: 30000, total: 355000 },
  { sn: 10, dr: 'VINOD K RAI', mobile: '9460401750', type: 'HARRISON BOOK', amount: '11000', apr: 30000, may: 30000, jun: 40000, jul: 40000, total: 331500 }
];

export const RoiSheet: React.FC = () => {
  const [search, setSearch] = useState('');
  const filtered = ROI_DATA.filter(r => r.dr.toLowerCase().includes(search.toLowerCase()) || r.mobile.includes(search));

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <span className="p-2 bg-emerald-500/20 text-emerald-400 rounded-lg"><DollarSign size={18} /></span>
          <h2 className="text-base font-bold text-white">13. INVESTMENT AND COVERAGE ANALYSIS (ROI)</h2>
        </div>
        <div className="relative w-full sm:w-60">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
          <input 
            type="text" 
            placeholder="Search doctor or mobile..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-8 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-emerald-500"
          />
        </div>
      </div>
      <div className="overflow-x-auto max-h-[500px]">
        <table className="w-full text-left text-xs border-collapse">
          <thead className="sticky top-0 bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800 z-10">
            <tr>
              <th className="p-2.5 w-10 text-center">S.N.</th>
              <th className="p-2.5">Doctor Name</th>
              <th className="p-2.5">Mobile</th>
              <th className="p-2.5">Activity Type</th>
              <th className="p-2.5 text-right">Activity Amt (₹)</th>
              <th className="p-2.5 text-right">APR</th>
              <th className="p-2.5 text-right">MAY</th>
              <th className="p-2.5 text-right">JUN</th>
              <th className="p-2.5 text-right">JUL</th>
              <th className="p-2.5 text-right text-emerald-400">Total Return (₹)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {filtered.map(row => (
              <tr key={row.sn} className="hover:bg-slate-800/40 transition">
                <td className="p-2.5 text-center text-slate-500 font-mono">{row.sn}</td>
                <td className="p-2.5 font-semibold text-white">{row.dr}</td>
                <td className="p-2.5 text-slate-400 font-mono">{row.mobile}</td>
                <td className="p-2.5 text-slate-300">{row.type}</td>
                <td className="p-2.5 text-right font-mono text-slate-400">{row.amount}</td>
                <td className="p-2.5 text-right font-mono text-slate-300">₹{row.apr.toLocaleString()}</td>
                <td className="p-2.5 text-right font-mono text-slate-300">₹{row.may.toLocaleString()}</td>
                <td className="p-2.5 text-right font-mono text-slate-300">₹{row.jun.toLocaleString()}</td>
                <td className="p-2.5 text-right font-mono text-slate-300">₹{row.jul.toLocaleString()}</td>
                <td className="p-2.5 text-right font-mono font-bold text-emerald-400">₹{row.total.toLocaleString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
