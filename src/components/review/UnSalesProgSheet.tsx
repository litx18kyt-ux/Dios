import React, { useState } from 'react';
import { Table2, Search } from 'lucide-react';
import { MASTER_PRODUCTS } from '../../data/masterProducts';

export const UnSalesProgSheet: React.FC = () => {
  const [search, setSearch] = useState('');
  const filtered = MASTER_PRODUCTS.filter(p => p.name.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-4 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <span className="p-2 bg-cyan-500/20 text-cyan-400 rounded-lg"><Table2 size={18} /></span>
          <h2 className="text-base font-bold text-white">4. UNIT SALES PROGRESSION (HQ TOTAL)</h2>
        </div>
        <div className="relative w-full sm:w-60">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
          <input 
            type="text" 
            placeholder="Search in 73 products..."
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
              <th className="p-2.5 text-center w-12">S.N.</th>
              <th className="p-2.5 min-w-[200px]">Product Name</th>
              <th className="p-2.5 text-right">PTS (₹)</th>
              <th className="p-2.5 text-center text-blue-400">APR (Pri / Sec / Cl)</th>
              <th className="p-2.5 text-center text-cyan-400">MAY (Pri / Sec / Cl)</th>
              <th className="p-2.5 text-center text-emerald-400">JUN (Pri / Sec / Cl)</th>
              <th className="p-2.5 text-center text-purple-400">JUL (Pri / Sec / Cl)</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {filtered.map(p => (
              <tr key={p.sn} className="hover:bg-slate-800/40 transition">
                <td className="p-2.5 text-center text-slate-500 font-mono">{p.sn}</td>
                <td className="p-2.5 font-medium text-white">{p.name}</td>
                <td className="p-2.5 text-right text-slate-400 font-mono">{p.pts.toFixed(2)}</td>
                <td className="p-2.5 text-center text-slate-400 font-mono">- / - / -</td>
                <td className="p-2.5 text-center text-slate-400 font-mono">- / - / -</td>
                <td className="p-2.5 text-center text-slate-400 font-mono">- / - / -</td>
                <td className="p-2.5 text-center text-slate-400 font-mono">- / - / -</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
