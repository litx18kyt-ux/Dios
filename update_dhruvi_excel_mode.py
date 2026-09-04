import os, sys

# 1. Update memoryStore.ts
mem_code = '''export interface FwDayEntry {
  date: number;
  day: string;
  areaWorked: string;
  tpSubmitted: string;
  drsMet: string | number;
  chemistsMet: string | number;
  withManager?: boolean;
  workType?: string;
}

export interface PartyBreakdownItem {
  id: string;
  partyName: string;
  amount: number;
  note?: string;
}

export interface MonthBreakdownMap {
  [key: string]: PartyBreakdownItem[];
}

export interface DhruviProductEntry {
  sn: number;
  salesFormula: string;
  salesQty: number;
  closingFormula: string;
  closingQty: number;
}

export type DhruviValuationMode = 'PTS' | 'PTR' | 'MANUAL_PTR' | 'MANUAL_PTS';

export const DEFAULT_STOCKISTS = [
  'NAGDA DISTRIBUTORS',
  'MODI DISTRIBUTORS',
  'SHREE VARDHMAN PHARMA',
  'SUN DISTRIBUTORS',
  'R.P. AGENCIES',
  'DWARIKA MEDICALS'
];

export const memoryStore = {
  dcrDataByMonth: {} as Record<string, FwDayEntry[]>,
  currentDcrMonth: 'Aug-2026',
  effortLevelData: null as Record<string, Record<string, string>> | null,
  salesBreakdown: {} as MonthBreakdownMap,
  dhruviEntries: {} as Record<number, DhruviProductEntry>,
  dhruviManualPtrTotal: '' as string,
  dhruviManualPtsTotal: '' as string,
  dhruviValuationMode: 'PTS' as DhruviValuationMode,
  beName: 'BANWARI LAL MEENA',
  hqName: 'UDAIPUR',
  lastSyncedMonthCode: 'AUG'
};
'''
with open("/workspaces/Dios/src/data/memoryStore.ts", "w") as f:
    f.write(mem_code)
print("✓ Updated memoryStore.ts with DhruviValuationMode!")

# 2. Update DhruviManualModal.tsx with Dropdown
modal_code = '''import React, { useState } from 'react';
import { Calculator, Search, X, Check, Trash2, Edit3, Settings2 } from 'lucide-react';
import { MASTER_PRODUCTS } from '../data/masterProducts';
import { PartyParseSummary } from '../parsers/common';
import { memoryStore, DhruviProductEntry, DhruviValuationMode } from '../data/memoryStore';

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

  const [manualPtrTotal, setManualPtrTotal] = useState<string>(() => {
    return memoryStore.dhruviManualPtrTotal || '';
  });

  const [manualPtsTotal, setManualPtsTotal] = useState<string>(() => {
    return memoryStore.dhruviManualPtsTotal || '';
  });

  const [valuationMode, setValuationMode] = useState<DhruviValuationMode>(() => {
    return memoryStore.dhruviValuationMode || 'PTS';
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
    memoryStore.dhruviManualPtrTotal = manualPtrTotal;
    memoryStore.dhruviManualPtsTotal = manualPtsTotal;
    memoryStore.dhruviValuationMode = valuationMode;

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
      setManualPtrTotal('');
      setManualPtsTotal('');
      setValuationMode('PTS');
      memoryStore.dhruviEntries = {};
      memoryStore.dhruviManualPtrTotal = '';
      memoryStore.dhruviManualPtsTotal = '';
      memoryStore.dhruviValuationMode = 'PTS';
      onClear();
    }
  };

  // Calculations
  let totalLiveSalesUnits = 0;
  let totalLiveClosingUnits = 0;
  let totalLiveSalesPtsVal = 0;
  let totalLiveSalesPtrVal = 0;
  let totalLiveClosingPtsVal = 0;
  let totalLiveClosingPtrVal = 0;

  MASTER_PRODUCTS.forEach(p => {
    const entry = draft[p.sn];
    if (entry) {
      const sQty = entry.salesQty || 0;
      const cQty = entry.closingQty || 0;
      totalLiveSalesUnits += sQty;
      totalLiveClosingUnits += cQty;
      totalLiveSalesPtsVal += sQty * p.pts;
      totalLiveSalesPtrVal += sQty * (p.ptr || p.pts);
      totalLiveClosingPtsVal += cQty * p.pts;
      totalLiveClosingPtrVal += cQty * (p.ptr || p.pts);
    }
  });

  const parsedManualPtr = parseFloat(manualPtrTotal.replace(/,/g, '')) || 0;
  const ptrVariance = parsedManualPtr > 0 ? (totalLiveSalesPtrVal - parsedManualPtr) : 0;

  return (
    <div className="fixed inset-0 bg-slate-950/85 backdrop-blur-md z-50 flex items-center justify-center p-2 md:p-5">
      <div className="bg-slate-900 border border-amber-500/40 rounded-3xl max-w-7xl w-full p-4 md:p-6 shadow-2xl flex flex-col max-h-[94vh]">
        
        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-800 mb-3">
          <div className="flex items-center gap-3">
            <span className="p-2.5 bg-amber-500/20 text-amber-400 rounded-xl border border-amber-500/30">
              <Calculator size={22} />
            </span>
            <div>
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                Dhruvi Manual Sheet (Formula &amp; Valuation Mode Engine)
              </h3>
              <p className="text-xs text-slate-400">
                Formula Support: <span className="text-amber-300 font-mono font-bold">+6+6 (=12)</span> or <span className="text-amber-300 font-mono font-bold">+6-2 (=4)</span>
              </p>
            </div>
          </div>

          {/* 🌟 EXCEL VALUATION MODE SELECTION DROPDOWN */}
          <div className="flex items-center gap-2 bg-slate-950 px-3 py-1.5 rounded-2xl border-2 border-amber-500/50 shadow-md">
            <span className="text-[11px] text-amber-300 font-bold uppercase flex items-center gap-1">
              <Settings2 size={13} /> Excel Value Mode:
            </span>
            <select
              value={valuationMode}
              onChange={(e) => setValuationMode(e.target.value as DhruviValuationMode)}
              className="bg-slate-900 border border-slate-700 text-amber-300 text-xs font-bold font-mono rounded-xl px-2.5 py-1 focus:outline-none focus:border-amber-400 cursor-pointer"
            >
              <option value="PTS">🔹 Calculated PTS (₹{Math.round(totalLiveSalesPtsVal).toLocaleString()})</option>
              <option value="PTR">🔸 Calculated PTR (₹{Math.round(totalLiveSalesPtrVal).toLocaleString()})</option>
              <option value="MANUAL_PTR">✏️ Manual Target PTR (₹{manualPtrTotal ? Number(manualPtrTotal).toLocaleString() : '0'})</option>
              <option value="MANUAL_PTS">✏️ Manual Target PTS (₹{manualPtsTotal ? Number(manualPtsTotal).toLocaleString() : '0'})</option>
            </select>
          </div>

          <button onClick={onClose} className="text-slate-400 hover:text-white p-1 rounded-lg cursor-pointer">
            <X size={20} />
          </button>
        </div>

        {/* Top Summary & Manual Target Boxes */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 mb-3">
          {/* Card 1: Sales Secondary Summary */}
          <div className="p-3 bg-slate-950 rounded-2xl border border-cyan-500/30 space-y-1">
            <div className="text-[10px] text-slate-400 uppercase font-semibold flex items-center justify-between">
              <span>Sales Units (SEC)</span>
              <span className="text-cyan-400 font-bold font-mono">{totalLiveSalesUnits.toLocaleString()} Units</span>
            </div>
            <div className="flex justify-between items-center text-xs font-mono">
              <span className="text-slate-400">PTS Value:</span>
              <span className="text-cyan-300 font-bold">₹ {Math.round(totalLiveSalesPtsVal).toLocaleString()}</span>
            </div>
            <div className="flex justify-between items-center text-xs font-mono">
              <span className="text-amber-400 font-semibold">PTR Value:</span>
              <span className="text-amber-300 font-bold">₹ {Math.round(totalLiveSalesPtrVal).toLocaleString()}</span>
            </div>
          </div>

          {/* Card 2: Closing Stock Summary */}
          <div className="p-3 bg-slate-950 rounded-2xl border border-emerald-500/30 space-y-1">
            <div className="text-[10px] text-slate-400 uppercase font-semibold flex items-center justify-between">
              <span>Closing Stock (CL)</span>
              <span className="text-emerald-400 font-bold font-mono">{totalLiveClosingUnits.toLocaleString()} Units</span>
            </div>
            <div className="flex justify-between items-center text-xs font-mono">
              <span className="text-slate-400">PTS Value:</span>
              <span className="text-emerald-300 font-bold">₹ {Math.round(totalLiveClosingPtsVal).toLocaleString()}</span>
            </div>
            <div className="flex justify-between items-center text-xs font-mono">
              <span className="text-amber-400 font-semibold">PTR Value:</span>
              <span className="text-amber-300 font-bold">₹ {Math.round(totalLiveClosingPtrVal).toLocaleString()}</span>
            </div>
          </div>

          {/* Card 3: User Manual Target PTR Input Box */}
          <div className="p-3 bg-slate-950 rounded-2xl border-2 border-amber-500/60 shadow-lg shadow-amber-950/30 flex flex-col justify-between">
            <div>
              <div className="text-[11px] text-amber-300 uppercase font-bold flex items-center gap-1.5">
                <Edit3 size={13} className="text-amber-400" /> Manual Target PTR (₹ Rupees)
              </div>
              <p className="text-[10px] text-slate-400 mt-0.5">Enter your target PTR value:</p>
            </div>
            <input
              type="text"
              placeholder="e.g. 50000"
              value={manualPtrTotal}
              onChange={(e) => setManualPtrTotal(e.target.value)}
              className="w-full bg-slate-900 border border-amber-500/50 text-amber-300 font-mono font-bold text-sm rounded-xl px-3 py-1.5 mt-1.5 focus:outline-none focus:border-amber-400"
            />
          </div>

          {/* Card 4: Target Variance */}
          <div className="p-3 bg-slate-950 rounded-2xl border border-purple-500/30 flex flex-col justify-between">
            <div className="text-[10px] text-slate-400 uppercase font-semibold">PTR Target Variance</div>
            <div className={`text-base font-bold font-mono ${ptrVariance === 0 ? 'text-slate-400' : ptrVariance >= 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
              {parsedManualPtr > 0 ? `${ptrVariance >= 0 ? '+' : ''}₹ ${Math.round(ptrVariance).toLocaleString()}` : 'Enter Target Above'}
            </div>
            <div className="text-[10px] text-slate-500 font-mono">
              Active Mode: <span className="text-amber-400 font-bold">{valuationMode}</span>
            </div>
          </div>
        </div>

        {/* Search */}
        <div className="relative mb-3">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            placeholder="Search in 73 products..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-8 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-amber-400"
          />
        </div>

        {/* 73 Products Table */}
        <div className="overflow-y-auto flex-1 border border-slate-800 rounded-xl pr-1">
          <table className="w-full text-left text-xs border-collapse">
            <thead className="sticky top-0 bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800 z-10">
              <tr>
                <th className="p-2 text-center w-10">S.N.</th>
                <th className="p-2 min-w-[180px]">Product Name</th>
                <th className="p-2 text-center w-16">Pack</th>
                <th className="p-2 text-right w-20 text-slate-300">PTS (₹)</th>
                <th className="p-2 text-right w-20 text-amber-300">PTR (₹)</th>
                <th className="p-2 text-center min-w-[150px] text-cyan-400 bg-cyan-950/20">
                  Sec Sales (Formula)
                </th>
                <th className="p-2 text-right min-w-[110px] text-cyan-300 bg-cyan-950/10">
                  Sales (PTS / PTR ₹)
                </th>
                <th className="p-2 text-center min-w-[150px] text-emerald-400 bg-emerald-950/20">
                  Closing (Formula)
                </th>
                <th className="p-2 text-right min-w-[110px] text-emerald-300 bg-emerald-950/10">
                  Closing (PTS / PTR ₹)
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {MASTER_PRODUCTS
                .filter(p => p.name.toLowerCase().includes(search.toLowerCase()) || String(p.sn).includes(search))
                .map(p => {
                  const entry = draft[p.sn] || { sn: p.sn, salesFormula: '', salesQty: 0, closingFormula: '', closingQty: 0 };
                  const lineSalesPts = entry.salesQty * p.pts;
                  const lineSalesPtr = entry.salesQty * (p.ptr || p.pts);
                  const lineClosingPts = entry.closingQty * p.pts;
                  const lineClosingPtr = entry.closingQty * (p.ptr || p.pts);

                  return (
                    <tr key={p.sn} className="hover:bg-slate-800/40 transition">
                      <td className="p-2 text-center text-slate-500 font-mono">{p.sn}</td>
                      <td className="p-2 font-medium text-white">{p.name}</td>
                      <td className="p-2 text-center text-slate-400 font-mono">{p.pack || '-'}</td>
                      <td className="p-2 text-right font-mono text-slate-300">{p.pts.toFixed(2)}</td>
                      <td className="p-2 text-right font-mono text-amber-300 font-bold">{p.ptr.toFixed(2)}</td>

                      {/* Sales Formula Cell */}
                      <td className="p-1 text-center bg-cyan-950/10">
                        <div className="flex items-center gap-1">
                          <input
                            type="text"
                            value={entry.salesFormula}
                            onChange={e => handleCellChange(p.sn, 'sales', e.target.value)}
                            placeholder="0"
                            className="w-full py-1 px-2 bg-slate-950 rounded-lg font-mono text-xs text-cyan-300 font-bold border border-slate-800 focus:border-cyan-400 focus:outline-none text-center"
                          />
                          {entry.salesFormula && entry.salesFormula !== String(entry.salesQty) && (
                            <span className="text-[10px] bg-cyan-500/20 text-cyan-300 px-1 py-0.5 rounded font-mono font-bold shrink-0">
                              ={entry.salesQty}
                            </span>
                          )}
                        </div>
                      </td>

                      {/* Sales Values (PTS & PTR) */}
                      <td className="p-1.5 text-right font-mono bg-cyan-950/5">
                        {entry.salesQty > 0 ? (
                          <div className="leading-tight">
                            <div className="text-cyan-300 font-bold">₹{Math.round(lineSalesPts).toLocaleString()} <span className="text-[9px] text-slate-400">PTS</span></div>
                            <div className="text-amber-300 font-semibold text-[10px]">₹{Math.round(lineSalesPtr).toLocaleString()} <span className="text-[9px] text-slate-400">PTR</span></div>
                          </div>
                        ) : '-'}
                      </td>

                      {/* Closing Formula Cell */}
                      <td className="p-1 text-center bg-emerald-950/10">
                        <div className="flex items-center gap-1">
                          <input
                            type="text"
                            value={entry.closingFormula}
                            onChange={e => handleCellChange(p.sn, 'closing', e.target.value)}
                            placeholder="0"
                            className="w-full py-1 px-2 bg-slate-950 rounded-lg font-mono text-xs text-emerald-300 font-bold border border-slate-800 focus:border-emerald-400 focus:outline-none text-center"
                          />
                          {entry.closingFormula && entry.closingFormula !== String(entry.closingQty) && (
                            <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-1 py-0.5 rounded font-mono font-bold shrink-0">
                              ={entry.closingQty}
                            </span>
                          )}
                        </div>
                      </td>

                      {/* Closing Values (PTS & PTR) */}
                      <td className="p-1.5 text-right font-mono bg-emerald-950/5">
                        {entry.closingQty > 0 ? (
                          <div className="leading-tight">
                            <div className="text-emerald-300 font-bold">₹{Math.round(lineClosingPts).toLocaleString()} <span className="text-[9px] text-slate-400">PTS</span></div>
                            <div className="text-amber-300 font-semibold text-[10px]">₹{Math.round(lineClosingPtr).toLocaleString()} <span className="text-[9px] text-slate-400">PTR</span></div>
                          </div>
                        ) : '-'}
                      </td>
                    </tr>
                  );
                })}
            </tbody>
          </table>
        </div>

        {/* Footer Summary & Action Buttons */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-3 pt-3 border-t border-slate-800 mt-2">
          <button
            type="button"
            onClick={handleReset}
            className="w-full sm:w-auto px-3.5 py-2 bg-rose-950/40 hover:bg-rose-900/60 border border-rose-800/60 text-rose-300 rounded-xl text-xs font-semibold transition cursor-pointer flex items-center justify-center gap-1.5"
          >
            <Trash2 size={13} /> Clear Dhruvi Data
          </button>

          <div className="flex items-center gap-3 w-full sm:w-auto justify-end">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 rounded-xl text-xs font-semibold transition cursor-pointer"
            >
              Cancel
            </button>

            <button
              type="button"
              onClick={handleApply}
              className="flex items-center justify-center gap-2 px-5 py-2.5 bg-gradient-to-r from-amber-500 to-amber-600 hover:from-amber-400 hover:to-amber-500 text-slate-950 font-bold text-xs rounded-xl shadow-lg shadow-amber-500/20 transition cursor-pointer"
            >
              <Check size={15} /> Save &amp; Sync With Aggregator
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
'''
with open("/workspaces/Dios/src/components/DhruviManualModal.tsx", "w") as f:
    f.write(modal_code)
print("✓ Updated DhruviManualModal.tsx with Mode Dropdown!")

# 3. Update excelExporter.ts to apply Dhruvi's selected Valuation Mode in Sheet 1 & Sheet 2
exporter_code = '''import * as XLSX from 'xlsx-js-style';
import { AggregatedProduct } from '../parsers/common';
import { memoryStore } from '../data/memoryStore';
import { MASTER_PRODUCTS } from '../data/masterProducts';

const MONTHS = ['APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER', 'JANUARY', 'FEBRUARY', 'MARCH'];

// Styling Presets
const borderThin = {
  top: { style: 'thin', color: { rgb: 'D1D5DB' } },
  bottom: { style: 'thin', color: { rgb: 'D1D5DB' } },
  left: { style: 'thin', color: { rgb: 'D1D5DB' } },
  right: { style: 'thin', color: { rgb: 'D1D5DB' } }
};

const borderDoubleBottom = {
  top: { style: 'thin', color: { rgb: '000000' } },
  bottom: { style: 'double', color: { rgb: '000000' } },
  left: { style: 'thin', color: { rgb: '000000' } },
  right: { style: 'thin', color: { rgb: '000000' } }
};

const styleTitle = {
  font: { name: 'Calibri', sz: 16, bold: true, color: { rgb: 'FFFFFF' } },
  fill: { fgColor: { rgb: '0F172A' } },
  alignment: { horizontal: 'center', vertical: 'center' }
};

const styleSubTitle = {
  font: { name: 'Calibri', sz: 12, bold: true, color: { rgb: '38BDF8' } },
  fill: { fgColor: { rgb: '1E293B' } },
  alignment: { horizontal: 'center', vertical: 'center' }
};

const stylePartyHeader = {
  font: { name: 'Calibri', sz: 11, bold: true, color: { rgb: 'FFFFFF' } },
  fill: { fgColor: { rgb: '0369A1' } },
  alignment: { horizontal: 'center', vertical: 'center' },
  border: borderThin
};

const styleSubColHeader = {
  font: { name: 'Calibri', sz: 10, bold: true, color: { rgb: '0F172A' } },
  fill: { fgColor: { rgb: 'E2E8F0' } },
  alignment: { horizontal: 'center', vertical: 'center' },
  border: borderThin
};

const styleCellLeft = {
  font: { name: 'Calibri', sz: 10, color: { rgb: '000000' } },
  alignment: { horizontal: 'left', vertical: 'center' },
  border: borderThin
};

const styleCellCenter = {
  font: { name: 'Calibri', sz: 10, color: { rgb: '000000' } },
  alignment: { horizontal: 'center', vertical: 'center' },
  border: borderThin
};

const styleCellRight = {
  font: { name: 'Calibri', sz: 10, color: { rgb: '000000' } },
  alignment: { horizontal: 'right', vertical: 'center' },
  border: borderThin
};

const styleCellHighlight = {
  font: { name: 'Calibri', sz: 10, bold: true, color: { rgb: '0369A1' } },
  fill: { fgColor: { rgb: 'F0F9FF' } },
  alignment: { horizontal: 'center', vertical: 'center' },
  border: borderThin
};

const styleCellHighlightPri = {
  font: { name: 'Calibri', sz: 10, bold: true, color: { rgb: '1D4ED8' } },
  fill: { fgColor: { rgb: 'EFF6FF' } },
  alignment: { horizontal: 'center', vertical: 'center' },
  border: borderThin
};

const styleTotalRow = {
  font: { name: 'Calibri', sz: 11, bold: true, color: { rgb: '0F172A' } },
  fill: { fgColor: { rgb: 'FEF08A' } },
  alignment: { horizontal: 'center', vertical: 'center' },
  border: borderDoubleBottom
};

export function exportToExcel(
  products: (AggregatedProduct & { netPri?: number; priValue?: number })[],
  selectedMonth: string,
  activeParties: string[],
  summary: { totalSalesUnits: number; totalClosingUnits: number; totalSalesValue: number; totalClosingValue: number; totalPriUnits?: number; totalPriValue?: number }
) {
  const mode = memoryStore.dhruviValuationMode || 'PTS';
  const prodMap = new Map(MASTER_PRODUCTS.map(p => [p.sn, p]));

  // Calculate Party Wise Values with Dhruvi Mode Support
  const partySalesValues: Record<string, number> = {};
  const partyClosingValues: Record<string, number> = {};

  activeParties.forEach(party => {
    const isDhruvi = party.toLowerCase().includes('dhruvi');
    let sVal = 0;
    let cVal = 0;

    if (isDhruvi) {
      if (mode === 'MANUAL_PTR' && parseFloat(memoryStore.dhruviManualPtrTotal)) {
        sVal = parseFloat(memoryStore.dhruviManualPtrTotal.replace(/,/g, '')) || 0;
        cVal = products.reduce((acc, p) => {
          const mp = prodMap.get(p.sn);
          return acc + ((p.partyBreakdown[party]?.closing || 0) * (mp?.ptr || p.pts));
        }, 0);
      } else if (mode === 'MANUAL_PTS' && parseFloat(memoryStore.dhruviManualPtsTotal)) {
        sVal = parseFloat(memoryStore.dhruviManualPtsTotal.replace(/,/g, '')) || 0;
        cVal = products.reduce((acc, p) => acc + ((p.partyBreakdown[party]?.closing || 0) * p.pts), 0);
      } else if (mode === 'PTR') {
        sVal = products.reduce((acc, p) => {
          const mp = prodMap.get(p.sn);
          return acc + ((p.partyBreakdown[party]?.sales || 0) * (mp?.ptr || p.pts));
        }, 0);
        cVal = products.reduce((acc, p) => {
          const mp = prodMap.get(p.sn);
          return acc + ((p.partyBreakdown[party]?.closing || 0) * (mp?.ptr || p.pts));
        }, 0);
      } else {
        sVal = products.reduce((acc, p) => acc + ((p.partyBreakdown[party]?.sales || 0) * p.pts), 0);
        cVal = products.reduce((acc, p) => acc + ((p.partyBreakdown[party]?.closing || 0) * p.pts), 0);
      }
    } else {
      sVal = products.reduce((acc, p) => acc + ((p.partyBreakdown[party]?.sales || 0) * p.pts), 0);
      cVal = products.reduce((acc, p) => acc + ((p.partyBreakdown[party]?.closing || 0) * p.pts), 0);
    }

    partySalesValues[party] = sVal;
    partyClosingValues[party] = cVal;
  });

  const finalTotalSalesValue = Object.values(partySalesValues).reduce((a, b) => a + b, 0);
  const finalTotalClosingValue = Object.values(partyClosingValues).reduce((a, b) => a + b, 0);

  // =============================================================
  // SHEET 1: UN.SALES PROG (HQ TOTAL 12 MONTHS)
  // =============================================================
  const totalCols = 3 + MONTHS.length * 3;
  const wsData: any[][] = [];

  const row1 = new Array(totalCols).fill({ v: '', s: styleTitle });
  row1[0] = { v: 'DIOS LIFESCIENCES PVT. LTD.', s: styleTitle };
  wsData.push(row1);

  const row2 = new Array(totalCols).fill({ v: '', s: styleSubTitle });
  row2[0] = { v: 'UNIT SALES PROGRESSION (HQ TOTAL) - 2026-27', s: styleSubTitle };
  wsData.push(row2);

  const row3: any[] = [
    { v: '', s: stylePartyHeader },
    { v: '', s: stylePartyHeader },
    { v: '', s: stylePartyHeader }
  ];
  MONTHS.forEach(m => {
    row3.push(
      { v: `${m} 2026`, s: stylePartyHeader },
      { v: '', s: stylePartyHeader },
      { v: '', s: stylePartyHeader }
    );
  });
  wsData.push(row3);

  const row4: any[] = [
    { v: 'S.N.', s: styleSubColHeader },
    { v: 'PRODUCT NAME', s: styleSubColHeader },
    { v: 'PTS (₹)', s: styleSubColHeader }
  ];
  MONTHS.forEach(() => {
    row4.push(
      { v: 'NET PRI', s: styleSubColHeader },
      { v: 'NET SEC', s: styleSubColHeader },
      { v: 'CLOSING', s: styleSubColHeader }
    );
  });
  wsData.push(row4);

  // Data rows
  products.forEach(p => {
    const row: any[] = [
      { v: p.sn, s: styleCellCenter },
      { v: p.name, s: styleCellLeft },
      { v: p.pts.toFixed(2), s: styleCellRight }
    ];

    MONTHS.forEach(m => {
      if (m.toUpperCase() === selectedMonth.toUpperCase()) {
        const priVal = p.netPri !== undefined && p.netPri !== 0 ? p.netPri : 0;
        row.push(
          { v: priVal, s: priVal !== 0 ? styleCellHighlightPri : styleCellCenter },
          { v: p.netSec > 0 ? p.netSec : 0, s: p.netSec > 0 ? styleCellHighlight : styleCellCenter },
          { v: p.closing > 0 ? p.closing : 0, s: p.closing > 0 ? styleCellHighlight : styleCellCenter }
        );
      } else {
        row.push(
          { v: '', s: styleCellCenter },
          { v: '', s: styleCellCenter },
          { v: '', s: styleCellCenter }
        );
      }
    });

    wsData.push(row);
  });

  // Grand Total Units
  const totPriUnits = summary.totalPriUnits !== undefined 
    ? summary.totalPriUnits 
    : products.reduce((acc, p) => acc + (p.netPri || 0), 0);

  const rowTotal: any[] = [
    { v: 'Σ', s: styleTotalRow },
    { v: 'GRAND TOTAL (UNITS)', s: { ...styleTotalRow, alignment: { horizontal: 'left', vertical: 'center' } } },
    { v: '-', s: styleTotalRow }
  ];
  MONTHS.forEach(m => {
    if (m.toUpperCase() === selectedMonth.toUpperCase()) {
      rowTotal.push(
        { v: totPriUnits, s: { ...styleTotalRow, font: { bold: true, color: { rgb: '1D4ED8' } } } },
        { v: summary.totalSalesUnits, s: styleTotalRow },
        { v: summary.totalClosingUnits, s: styleTotalRow }
      );
    } else {
      rowTotal.push(
        { v: '', s: styleTotalRow },
        { v: '', s: styleTotalRow },
        { v: '', s: styleTotalRow }
      );
    }
  });
  wsData.push(rowTotal);

  // Total Value in Rupees
  const totPriVal = summary.totalPriValue !== undefined 
    ? summary.totalPriValue 
    : products.reduce((acc, p) => acc + (p.priValue || ((p.netPri || 0) * p.pts)), 0);

  const rowValue: any[] = [
    { v: '₹', s: styleTotalRow },
    { v: 'TOTAL VALUE (RUPEES)', s: { ...styleTotalRow, alignment: { horizontal: 'left', vertical: 'center' } } },
    { v: '-', s: styleTotalRow }
  ];
  MONTHS.forEach(m => {
    if (m.toUpperCase() === selectedMonth.toUpperCase()) {
      rowValue.push(
        { v: `₹ ${Math.round(totPriVal).toLocaleString()}`, s: { ...styleTotalRow, font: { bold: true, color: { rgb: '1D4ED8' } } } },
        { v: `₹ ${Math.round(finalTotalSalesValue).toLocaleString()}`, s: styleTotalRow },
        { v: `₹ ${Math.round(finalTotalClosingValue).toLocaleString()}`, s: styleTotalRow }
      );
    } else {
      rowValue.push(
        { v: '', s: styleTotalRow },
        { v: '', s: styleTotalRow },
        { v: '', s: styleTotalRow }
      );
    }
  });
  wsData.push(rowValue);

  const ws = XLSX.utils.aoa_to_sheet(wsData);
  ws['!merges'] = [
    { s: { r: 0, c: 0 }, e: { r: 0, c: totalCols - 1 } },
    { s: { r: 1, c: 0 }, e: { r: 1, c: totalCols - 1 } },
  ];
  MONTHS.forEach((_, idx) => {
    const startCol = 3 + idx * 3;
    ws['!merges']!.push({
      s: { r: 2, c: startCol },
      e: { r: 2, c: startCol + 2 }
    });
  });

  const colWidths: any[] = [{ wch: 6 }, { wch: 35 }, { wch: 12 }];
  MONTHS.forEach(() => {
    colWidths.push({ wch: 11 }, { wch: 11 }, { wch: 12 });
  });
  ws['!cols'] = colWidths;
  ws['!rows'] = [{ hpt: 30 }, { hpt: 22 }, { hpt: 22 }, { hpt: 20 }];

  // =============================================================
  // SHEET 2: 2-TIER PARTY BREAKDOWN (WITH DHRUVI VALUATION MODE)
  // =============================================================
  const bData: any[][] = [];
  const bRow1: any[] = [
    { v: 'S.N.', s: styleSubColHeader },
    { v: 'PRODUCT NAME', s: styleSubColHeader },
    { v: 'PTS (₹)', s: styleSubColHeader }
  ];
  activeParties.forEach(p => {
    const isDhruvi = p.toLowerCase().includes('dhruvi');
    const headerTitle = isDhruvi ? `DHRUVI (${mode})` : p.toUpperCase();
    bRow1.push(
      { v: headerTitle, s: stylePartyHeader },
      { v: '', s: stylePartyHeader }
    );
  });
  bRow1.push(
    { v: 'TOTAL ALL PARTIES', s: { ...stylePartyHeader, fill: { fgColor: { rgb: '0F172A' } } } },
    { v: '', s: stylePartyHeader }
  );
  bData.push(bRow1);

  const bRow2: any[] = [
    { v: '', s: styleSubColHeader },
    { v: '', s: styleSubColHeader },
    { v: '', s: styleSubColHeader }
  ];
  activeParties.forEach(() => {
    bRow2.push(
      { v: 'SEC', s: styleSubColHeader },
      { v: 'CLOSING', s: styleSubColHeader }
    );
  });
  bRow2.push(
    { v: 'TOTAL SEC', s: { ...styleSubColHeader, font: { bold: true, color: { rgb: '0369A1' } } } },
    { v: 'TOTAL CLOSING', s: { ...styleSubColHeader, font: { bold: true, color: { rgb: '0369A1' } } } }
  );
  bData.push(bRow2);

  products.forEach(p => {
    const row: any[] = [
      { v: p.sn, s: styleCellCenter },
      { v: p.name, s: styleCellLeft },
      { v: p.pts.toFixed(2), s: styleCellRight }
    ];

    activeParties.forEach(party => {
      const partySales = p.partyBreakdown[party]?.sales || 0;
      const partyClosing = p.partyBreakdown[party]?.closing || 0;
      row.push(
        { v: partySales, s: partySales > 0 ? styleCellHighlight : styleCellCenter },
        { v: partyClosing, s: partyClosing > 0 ? styleCellHighlight : styleCellCenter }
      );
    });

    row.push(
      { v: p.netSec, s: { ...styleCellHighlight, fill: { fgColor: { rgb: 'E0F2FE' } } } },
      { v: p.closing, s: { ...styleCellHighlight, fill: { fgColor: { rgb: 'E0F2FE' } } } }
    );

    bData.push(row);
  });

  // Grand Total Row (Units)
  const bRowTotal: any[] = [
    { v: 'Σ', s: styleTotalRow },
    { v: 'GRAND TOTAL (UNITS)', s: { ...styleTotalRow, alignment: { horizontal: 'left', vertical: 'center' } } },
    { v: '-', s: styleTotalRow }
  ];
  activeParties.forEach(party => {
    const partyTotalSales = products.reduce((acc, p) => acc + (p.partyBreakdown[party]?.sales || 0), 0);
    const partyTotalClosing = products.reduce((acc, p) => acc + (p.partyBreakdown[party]?.closing || 0), 0);
    bRowTotal.push(
      { v: partyTotalSales, s: styleTotalRow },
      { v: partyTotalClosing, s: styleTotalRow }
    );
  });
  bRowTotal.push(
    { v: summary.totalSalesUnits, s: { ...styleTotalRow, font: { bold: true, sz: 12 } } },
    { v: summary.totalClosingUnits, s: { ...styleTotalRow, font: { bold: true, sz: 12 } } }
  );
  bData.push(bRowTotal);

  // Grand Total Row (Value in ₹) - Applies Mode
  const bRowValue: any[] = [
    { v: '₹', s: styleTotalRow },
    { v: 'TOTAL VALUE (RUPEES)', s: { ...styleTotalRow, alignment: { horizontal: 'left', vertical: 'center' } } },
    { v: '-', s: styleTotalRow }
  ];
  activeParties.forEach(party => {
    const sVal = partySalesValues[party] || 0;
    const cVal = partyClosingValues[party] || 0;
    bRowValue.push(
      { v: `₹ ${Math.round(sVal).toLocaleString()}`, s: styleTotalRow },
      { v: `₹ ${Math.round(cVal).toLocaleString()}`, s: styleTotalRow }
    );
  });
  bRowValue.push(
    { v: `₹ ${Math.round(finalTotalSalesValue).toLocaleString()}`, s: { ...styleTotalRow, font: { bold: true, sz: 11 } } },
    { v: `₹ ${Math.round(finalTotalClosingValue).toLocaleString()}`, s: { ...styleTotalRow, font: { bold: true, sz: 11 } } }
  );
  bData.push(bRowValue);

  const wsBreakdown = XLSX.utils.aoa_to_sheet(bData);
  wsBreakdown['!merges'] = [
    { s: { r: 0, c: 0 }, e: { r: 1, c: 0 } },
    { s: { r: 0, c: 1 }, e: { r: 1, c: 1 } },
    { s: { r: 0, c: 2 }, e: { r: 1, c: 2 } },
  ];

  activeParties.forEach((_, idx) => {
    const startCol = 3 + idx * 2;
    wsBreakdown['!merges']!.push({
      s: { r: 0, c: startCol },
      e: { r: 0, c: startCol + 1 }
    });
  });

  const totStartCol = 3 + activeParties.length * 2;
  wsBreakdown['!merges']!.push({
    s: { r: 0, c: totStartCol },
    e: { r: 0, c: totStartCol + 1 }
  });

  const bCols: any[] = [{ wch: 6 }, { wch: 35 }, { wch: 12 }];
  activeParties.forEach(() => {
    bCols.push({ wch: 14 }, { wch: 14 });
  });
  bCols.push({ wch: 15 }, { wch: 16 });
  wsBreakdown['!cols'] = bCols;

  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'UN.SALES PROG');
  XLSX.utils.book_append_sheet(wb, wsBreakdown, 'PARTY BREAKDOWN');

  const fileName = `Dios_Master_Statement_${selectedMonth}_2026.xlsx`;
  XLSX.writeFile(wb, fileName);
}
'''
with open("/workspaces/Dios/src/utils/excelExporter.ts", "w") as f:
    f.write(exporter_code)
print("✓ Updated excelExporter.ts with dynamic Dhruvi valuation export!")
