import React, { useState } from 'react';
import { Calculator, Search, X, Check, Trash2 } from 'lucide-react';
import { MASTER_PRODUCTS } from '../data/masterProducts';
import { PartyParseSummary } from '../parsers/common';
import { memoryStore, DhruviProductEntry } from '../data/memoryStore';

// 🧮 1000 IQ In-Cell Math Evaluator (+6+6 -> 12, +6-2 -> 4)
export function evalExcelFormula(input: string): number {
  if (!input) return 0;
  let expr = String(input).trim();
  if (expr.startsWith('+')) expr = expr.substring(1).trim();
  if (!expr) return 0;

  if (!/^[\d\s+\-*/.]+$/.test(expr)) {
    const num = parseFloat(expr);
    return isNaN(num) ? 0 : num;
  }

  try {
    const res = new Function(`return (${expr})`)();
    const val = Number(res);
    return isNaN(val) ? 0 : Math.round(val * 100) / 100;
  } catch {
    const num = parseFloat(expr);
    return isNaN(num) ? 0 : num;
  }
}

interface Props {
  isOpen: boolean;
  onClose: () => void;
  onSave: (summary: PartyParseSummary) => void;
  onClear: () => void;
}

export const DhruviManualModal: React.FC<Props> = ({ isOpen, onClose, onSave, onClear }) => {
  const [search, setSearch] = useState('');
  const [draft, setDraft] = useState<Record<number, DhruviProductEntry>>(() => {
    return memoryStore.dhruviEntries || {};
  });

  if (!isOpen) return null;

  const handleCellChange = (sn: number, field: 'sales' | 'closing', textVal: string) => {
    setDraft(prev => {
      const current = prev[sn] || { sn, salesFormula: '', salesQty: 0, closingFormula: '', closingQty: 0 };
      const evaluated = evalExcelFormula(textVal);

      return {
        ...prev,
        [sn]: {
          ...current,
          ...(field === 'sales'
            ? { salesFormula: textVal, salesQty: evaluated }
            : { closingFormula: textVal, closingQty: evaluated })
        }
      };
    });
  };

  const handleApply = () => {
    memoryStore.dhruviEntries = draft;

    const itemsMap: Record<number, { sales: number; closing: number }> = {};
    let totalSales = 0;
    let totalClosing = 0;
    let count = 0;

    MASTER_PRODUCTS.forEach(p => {
      const entry = draft[p.sn];
      if (entry && (entry.salesQty !== 0 || entry.closingQty !== 0)) {
        itemsMap[p.sn] = { sales: entry.salesQty, closing: entry.closingQty };
        totalSales += entry.salesQty;
        totalClosing += entry.closingQty;
        count++;
      }
    });

    const summary: PartyParseSummary = {
      partyName: 'Dhruvi',
      fileName: 'Manual Formula Entry',
      itemCount: count,
      totalSales,
      totalClosing,
      items: itemsMap
    };

    onSave(summary);
  };

  const handleReset = () => {
    if (window.confirm("Dhruvi ka saara data clear karna hai?")) {
      setDraft({});
      memoryStore.dhruviEntries = {};
      onClear();
    }
  };

  const totalLiveSales = Object.values(draft).reduce((s, it) => s + (it.salesQty || 0), 0);
  const totalLiveClosing = Object.values(draft).reduce((s, it) => s + (it.closingQty || 0), 0);

  return (
    <div className="fixed inset-0 bg-slate-950/85 backdrop-blur-md z-50 flex items-center justify-center p-3 md:p-6">
      <div className="bg-slate-900 border border-amber-500/40 rounded-3xl max-w-5xl w-full p-5 md:p-6 shadow-2xl flex flex-col max-h-[90vh]">
        
        {/* Header */}
        <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-4">
          <div className="flex items-center gap-3">
            <span className="p-2.5 bg-amber-500/20 text-amber-400 rounded-xl border border-amber-500/30">
              <Calculator size={22} />
            </span>
            <div>
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                Dhruvi Manual Sheet (Excel In-Cell Formula Engine)
              </h3>
              <p className="text-xs text-slate-400">
                Formula examples: <span className="text-amber-300 font-mono font-bold">+6+6 (=12)</span> or <span className="text-amber-300 font-mono font-bold">+6-2 (=4)</span> or <span className="text-amber-300 font-mono font-bold">10+5</span>
              </p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white p-1 rounded-lg cursor-pointer">
            <X size={20} />
          </button>
        </div>

        {/* Search & Real-time Math Summary */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 mb-4">
          <div className="relative w-full sm:w-72">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <input
              type="text"
              placeholder="Search in 73 products..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-8 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-amber-400"
            />
          </div>

          <div className="flex items-center gap-3 text-xs bg-slate-950 px-3 py-1.5 rounded-xl border border-slate-800 font-mono">
            <span className="text-slate-400">Dhruvi Sales: <b className="text-cyan-400">{totalLiveSales} Units</b></span>
            <span className="text-slate-600">|</span>
            <span className="text-slate-400">Closing: <b className="text-emerald-400">{totalLiveClosing} Units</b></span>
          </div>
        </div>

        {/* 73 Master Products Grid */}
        <div className="overflow-y-auto flex-1 border border-slate-800 rounded-xl pr-1">
          <table className="w-full text-left text-xs border-collapse">
            <thead className="sticky top-0 bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800 z-10">
              <tr>
                <th className="p-2.5 text-center w-12">S.N.</th>
                <th className="p-2.5 min-w-[220px]">Product Name</th>
                <th className="p-2.5 text-right w-24">PTS (₹)</th>
                <th className="p-2.5 text-center min-w-[160px] text-cyan-400 bg-cyan-950/20">
                  Secondary Sales (Formula: +6+6)
                </th>
                <th className="p-2.5 text-center min-w-[160px] text-emerald-400 bg-emerald-950/20">
                  Closing Stock (Formula: +6-2)
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {MASTER_PRODUCTS
                .filter(p => p.name.toLowerCase().includes(search.toLowerCase()) || String(p.sn).includes(search))
                .map(p => {
                  const entry = draft[p.sn] || { sn: p.sn, salesFormula: '', salesQty: 0, closingFormula: '', closingQty: 0 };
                  return (
                    <tr key={p.sn} className="hover:bg-slate-800/40 transition">
                      <td className="p-2 text-center text-slate-500 font-mono">{p.sn}</td>
                      <td className="p-2 font-medium text-white">{p.name}</td>
                      <td className="p-2 text-right font-mono text-slate-400">{p.pts.toFixed(2)}</td>

                      {/* Sales Cell */}
                      <td className="p-1.5 text-center bg-cyan-950/10">
                        <div className="flex items-center gap-1.5">
                          <input
                            type="text"
                            value={entry.salesFormula}
                            onChange={e => handleCellChange(p.sn, 'sales', e.target.value)}
                            placeholder="0"
                            className="w-full py-1.5 px-2 bg-slate-950 rounded-lg font-mono text-xs text-cyan-300 font-bold border border-slate-800 focus:border-cyan-400 focus:outline-none text-center"
                          />
                          {entry.salesFormula && entry.salesFormula !== String(entry.salesQty) && (
                            <span className="text-[10px] bg-cyan-500/20 text-cyan-300 px-1.5 py-0.5 rounded font-mono font-bold shrink-0" title="Calculated Result">
                              = {entry.salesQty}
                            </span>
                          )}
                        </div>
                      </td>

                      {/* Closing Cell */}
                      <td className="p-1.5 text-center bg-emerald-950/10">
                        <div className="flex items-center gap-1.5">
                          <input
                            type="text"
                            value={entry.closingFormula}
                            onChange={e => handleCellChange(p.sn, 'closing', e.target.value)}
                            placeholder="0"
                            className="w-full py-1.5 px-2 bg-slate-950 rounded-lg font-mono text-xs text-emerald-300 font-bold border border-slate-800 focus:border-emerald-400 focus:outline-none text-center"
                          />
                          {entry.closingFormula && entry.closingFormula !== String(entry.closingQty) && (
                            <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-1.5 py-0.5 rounded font-mono font-bold shrink-0" title="Calculated Result">
                              = {entry.closingQty}
                            </span>
                          )}
                        </div>
                      </td>
                    </tr>
                  );
                })}
            </tbody>
          </table>
        </div>

        {/* Footer Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-4 border-t border-slate-800">
          <button
            type="button"
            onClick={handleReset}
            className="w-full sm:w-auto px-4 py-2 bg-rose-950/40 hover:bg-rose-900/60 border border-rose-800/60 text-rose-300 rounded-xl text-xs font-semibold transition cursor-pointer flex items-center gap-1.5"
          >
            <Trash2 size={13} /> Clear Dhruvi Data
          </button>

          <div className="flex items-center gap-2.5 w-full sm:w-auto">
            <button
              type="button"
              onClick={onClose}
              className="w-full sm:w-auto px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold transition cursor-pointer"
            >
              Cancel
            </button>

            <button
              type="button"
              onClick={handleApply}
              className="w-full sm:w-auto flex items-center justify-center gap-2 px-5 py-2.5 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-xs rounded-xl shadow-lg shadow-amber-500/20 transition cursor-pointer"
            >
              <Check size={15} /> Save &amp; Sync With Aggregator
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
