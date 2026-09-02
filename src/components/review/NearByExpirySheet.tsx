import React from 'react';
import { AlertTriangle } from 'lucide-react';

export const NearByExpirySheet: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <span className="p-2 bg-amber-500/20 text-amber-400 rounded-lg"><AlertTriangle size={18} /></span>
          <h2 className="text-base font-bold text-white">5. NEAR BY EXPIRY (&lt; 8 MONTHS)</h2>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800">
              <th className="p-2.5 text-center w-12">S.N.</th>
              <th className="p-2.5">Product</th>
              <th className="p-2.5">HQ</th>
              <th className="p-2.5">Stockist Name</th>
              <th className="p-2.5 text-center">Quantity</th>
              <th className="p-2.5 text-center">Month of Expiry</th>
              <th className="p-2.5">Plan of Liquidation</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            <tr>
              <td colSpan={7} className="p-8 text-center text-slate-500">
                No near-by expiry items recorded. (Upload stockist files to scan for expiries)
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
};
