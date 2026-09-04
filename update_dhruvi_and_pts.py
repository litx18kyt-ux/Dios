import os, sys

# 1. Update src/data/masterProducts.ts with exact PTS rates from PriceList.csv
master_products_code = '''export interface MasterProduct {
  sn: number;
  name: string;
  pack?: string;
  pts: number;
  ptr?: number;
  mrp?: number;
  keywords: string[];
}

export const MASTER_PRODUCTS: MasterProduct[] = [
  { sn: 1, name: "CALGYM 60K CAPS", pack: "1x4", pts: 90.16, keywords: ["CALGYM 60K", "CALGYM-60K", "CALGYM 60 K", "CALGYM 60"] },
  { sn: 2, name: "CALGYM TAB", pack: "1x10", pts: 81.78, keywords: ["CALGYM TAB", "CALGYM"] },
  { sn: 3, name: "CILDIOS 10 TAB", pack: "1x10", pts: 84.79, keywords: ["CILDIOS 10", "CILDIOS-10", "CILDIOS 10 S"] },
  { sn: 4, name: "CILDIOS 20 TAB", pack: "1X10", pts: 94.29, keywords: ["CILDIOS 20", "CILDIOS-20", "CILDIOS 20 TAB"] },
  { sn: 5, name: "CITICURE 500 TAB", pack: "1x10", pts: 539.31, keywords: ["CITICURE 500", "CITICURE-500"] },
  { sn: 6, name: "CITICURE PLUS TAB", pack: "1x10", pts: 553.37, keywords: ["CITICURE PLUS"] },
  { sn: 7, name: "DIOFLAM TAB", pack: "1x10", pts: 41.72, keywords: ["DIOFLAM"] },
  { sn: 8, name: "DIOMILIN NT TABLET", pack: "1x15", pts: 152.19, keywords: ["DIOMILIN NT", "DIOMILIN-NT"] },
  { sn: 9, name: "DIOSGLT 10 TAB", pack: "5x2x15", pts: 145.84, keywords: ["DIOSGLT 10", "DIOSGLT-10", "DIOSGLT"] },
  { sn: 10, name: "DIOZAM 10 TAB", pack: "1x10", pts: 60.75, keywords: ["DIOZAM 10", "DIOZAM-10"] },
  { sn: 11, name: "DIOZAM 5 TAB", pack: "1x10", pts: 35.03, keywords: ["DIOZAM 5", "DIOZAM-5"] },
  { sn: 12, name: "ESIPRAM 10MG TAB", pack: "1x10", pts: 65.83, keywords: ["ESIPRAM 10", "ESIPRAM 10MG", "ESIPRAM 10 MG"] },
  { sn: 13, name: "ESIPRAM PLUS TAB", pack: "1x10", pts: 105.39, keywords: ["ESIPRAM PLUS"] },
  { sn: 14, name: "FITJEE CAPS", pack: "1x10", pts: 105.16, keywords: ["FITJEE CAPS", "FITJEE CAP"] },
  { sn: 15, name: "FITJEE DM TABLET", pack: "1X 10", pts: 174.98, keywords: ["FITJEE DM", "FITJEE-DM", "FITJEE CAPSULE"] },
  { sn: 16, name: "FITJEE Q10 TAB", pack: "1x10", pts: 365.46, keywords: ["FITJEE Q10", "FITJEE Q 10", "FITJEE-Q10"] },
  { sn: 17, name: "ISIRON CAPS", pack: "1x10", pts: 63.65, keywords: ["ISIRON"] },
  { sn: 18, name: "LINAGET DM TAB", pack: "5X3X10", pts: 133.65, keywords: ["LINAGET DM", "LINAGET-DM"] },
  { sn: 19, name: "LINAGET-5 TAB", pack: "1x10", pts: 66.47, keywords: ["LINAGET 5", "LINAGET-5"] },
  { sn: 20, name: "LINAGET-D TAB", pack: "5X3X10", pts: 112.44, keywords: ["LINAGET D", "LINAGET-D", "LINAGET- D"] },
  { sn: 21, name: "LINAGET-E25", pack: "10x10", pts: 77.08, keywords: ["LINAGET E 25", "LINAGET-E25", "LINAGET-E 25", "LINAGET E25", "LINAGET E", "LINAGET-E"] },
  { sn: 22, name: "LINAGET-M-OD5/1000 TAB", pack: "1x10", pts: 91.93, keywords: ["LINAGET M OD 5 1000", "LINAGET M OD 5/1000", "LINAGET-M-OD5/1000"] },
  { sn: 23, name: "LINAGET-M-OD5/500 TAB", pack: "1x10", pts: 72.64, keywords: ["LINAGET M OD 500", "LINAGET M OD 5 500", "LINAGET M OD 500 TA", "LINAGET M OD", "LINAGET-M-OD5/500", "LINAGET M-OD 5/500", "LINAGET-M-OD5/500 TABS"] },
  { sn: 24, name: "LINAGET-M1000 TAB", pack: "1x10", pts: 82.93, keywords: ["LINAGET M 1000", "LINAGET-M 1000", "LINAGET-M1000"] },
  { sn: 25, name: "LINAGET-M500 TAB", pack: "1x10", pts: 58.46, keywords: ["LINAGET M 500", "LINAGET-M 500", "LINAGET-M500"] },
  { sn: 26, name: "METDIOS25", pack: "1X 10", pts: 31.32, keywords: ["METDIOS 25", "METDIOS25"] },
  { sn: 27, name: "METDIOS50", pack: "1X 10", pts: 37.71, keywords: ["METDIOS 50", "METDIOS50"] },
  { sn: 28, name: "NEUTOCID DSR CAPS", pack: "1X 10", pts: 66.12, keywords: ["NEUTOCID DSR"] },
  { sn: 29, name: "NEUTOCID LS TAB", pack: "1x10", pts: 123.24, keywords: ["NEUTOCID LS"] },
  { sn: 30, name: "PREMYLIN M 75 TAB", pack: "1x10", pts: 121.42, keywords: ["PREMYLIN M 75", "PREMYLIN-M 75", "PREMYLIN M75", "PREMYLIN 75"] },
  { sn: 31, name: "PREMYLIN MSR TAB", pack: "1x10", pts: 116.68, keywords: ["PREMYLIN MSR", "PREMYLIN-M SR", "PREMYLIN M SR", "PREMYLIN MSR TAB"] },
  { sn: 32, name: "PROSTADO D TAB", pack: "1x10", pts: 184.46, keywords: ["PROSTADO D", "PROSTADO-D"] },
  { sn: 33, name: "PROSTADO TAB", pack: "1x10", pts: 66.25, keywords: ["PROSTADO TAB", "PROSTADO"] },
  { sn: 34, name: "SOLEM 250 TAB", pack: "1x10", pts: 39.39, keywords: ["SOLEM 250", "SOLEM-250"] },
  { sn: 35, name: "SOLEM 500 TAB", pack: "1x10", pts: 83.06, keywords: ["SOLEM 500", "SOLEM-500", "SOLEM-500 TABS"] },
  { sn: 36, name: "VALROS 10 TAB", pack: "1x10", pts: 93.17, keywords: ["VALROS 10", "VALROS-10"] },
  { sn: 37, name: "VALROS 20 TAB", pack: "1x10", pts: 139.46, keywords: ["VALROS 20", "VALROS-20"] },
  { sn: 38, name: "VALROS 40TAB", pack: "10X3X10", pts: 185.07, keywords: ["VALROS 40", "VALROS-40"] },
  { sn: 39, name: "VALROS ASP CAPS", pack: "1x10", pts: 52.11, keywords: ["VALROS ASP CAP", "VALROS ASP CAPS", "VALROS ASP"] },
  { sn: 40, name: "VALROS ASP150 CAPS", pack: "1X 10", pts: 52.68, keywords: ["VALROS ASP 150", "VALROS ASP150"] },
  { sn: 41, name: "VALROS EZ-10", pack: "10X3X10", pts: 171.36, keywords: ["VALROS EZ 10", "VALROS-EZ-10", "VALROS-EZ 10", "VALROS EZ10", "VALROS EZ"] },
  { sn: 42, name: "VALROS EZ-20", pack: "10X3X10", pts: 171.36, keywords: ["VALROS EZ 20", "VALROS-EZ-20", "VALROS-EZ 20", "VALROS EZ20"] },
  { sn: 43, name: "VALROS EZ-40", pack: "10X3X10", pts: 171.36, keywords: ["VALROS EZ 40", "VALROS-EZ-40", "VALROS-EZ 40", "VALROS EZ40"] },
  { sn: 44, name: "VALROS F TAB", pack: "1x10", pts: 115.90, keywords: ["VALROS F TAB", "VALROS-F TAB", "VALROS F"] },
  { sn: 45, name: "VALROS GOLD 10 CAPS", pack: "1x10", pts: 108.20, keywords: ["VALROS GOLD 10", "VALROS GOLD10", "VALROS GOLD CAP", "VALROS GOLD"] },
  { sn: 46, name: "VALROS GOLD 20 CAPS", pack: "1x10", pts: 118.63, keywords: ["VALROS GOLD 20", "VALROS GOLD20"] },
  { sn: 47, name: "VALROS-F20 TAB", pack: "1X 10", pts: 250.07, keywords: ["VALROS F 20", "VALROS-F 20", "VALROS-F20", "VALROS F20"] },
  { sn: 48, name: "VIDGLIT M FOTRE TAB", pack: "1x10", pts: 110.80, keywords: ["VIDGLIT M FORTE", "VIDGLIT M FOTRE", "VIDGLIT-M FORTE", "VIDGLIT FORTE", "VIDGLIT FOTRE", "VIDGLIT M FORTE TAB"] },
  { sn: 49, name: "VIDGLIT M TAB", pack: "1x10", pts: 98.82, keywords: ["VIDGLIT M TAB", "VIDGLIT-M", "VIDGLIT M"] },
  { sn: 50, name: "VIDGLIT TAB", pack: "1x10", pts: 74.35, keywords: ["VIDGLIT 20", "VIDGLIT TAB", "VIDGLIT"] },
  { sn: 51, name: "VIDMET G 80 TAB", pack: "1x10", pts: 89.83, keywords: ["VIDMET G 80", "VIDMET-G 80", "VIDMET G80"] },
  { sn: 52, name: "VIDMET SR 1000MG TAB", pack: "1x10", pts: 27.40, keywords: ["VIDMET SR 1000", "VIDMET-SR 1000", "VIDMET SR 1GM", "VIDMET SR 1GM TAB"] },
  { sn: 53, name: "VIDMET SR 500MG TAB", pack: "1x10", pts: 13.19, keywords: ["VIDMET SR 500", "VIDMET-SR 500", "VIDMET SR500"] },
  { sn: 54, name: "VINTEL 20 TAB", pack: "1X 10", pts: 26.37, keywords: ["VINTEL 20", "VINTEL-20"] },
  { sn: 55, name: "VINTEL 40 TAB NEW", pack: "1x15", pts: 73.00, keywords: ["VINTEL 40 TAB", "VINTEL-40 TAB", "VINTEL 40 TABS NEW", "VINTEL 40 TAB NEW", "VINTEL 40"] },
  { sn: 56, name: "VINTEL 40AM TAB", pack: "1x10", pts: 62.74, keywords: ["VINTEL AM 40", "VINTEL 40 AM", "VINTEL-40AM", "VINTEL AM40", "VINTEL-40 AM"] },
  { sn: 57, name: "VINTEL 80 TAB", pack: "1x10", pts: 72.35, keywords: ["VINTEL 80", "VINTEL-80"] },
  { sn: 58, name: "VINTEL AM40 TAB", pack: "1x15", pts: 103.84, keywords: ["VINTEL AM40 TAB", "VINTEL AM 40", "VINTEL AM40"] },
  { sn: 59, name: "VINTEL CD TAB", pack: "1x10", pts: 62.93, keywords: ["VINTEL CD", "VINTEL-CD"] },
  { sn: 60, name: "VINTEL CT TAB", pack: "1x10", pts: 80.90, keywords: ["VINTEL CT", "VINTEL-CT"] },
  { sn: 61, name: "VINTEL CTC 6.25 TAB", pack: "10X3X10", pts: 126.17, keywords: ["VINTEL CTC 6.25", "VINTEL-CTC 6.25", "VINTEL-CTC6.25", "VINTEL CTC 6 25"] },
  { sn: 62, name: "VINTEL CTC TAB", pack: "1x10", pts: 138.93, keywords: ["VINTEL CTC", "VINTEL-CTC"] },
  { sn: 63, name: "VINTEL H40 TAB NEW", pack: "1x15", pts: 124.07, keywords: ["VINTEL H 40", "VINTEL 40 H", "VINTEL-H-40", "VINTEL-H 40", "VINTEL 40H", "VINTEL-40H", "VINTEL H40"] },
  { sn: 64, name: "VINTEL H80 TAB", pack: "1x10", pts: 104.78, keywords: ["VINTEL H 80", "VINTEL-H80", "VINTEL H80"] },
  { sn: 65, name: "Vintel M25 TAB", pack: "1x10", pts: 69.23, keywords: ["VINTEL M 25", "VINTEL M25", "VINTEL-M25"] },
  { sn: 66, name: "Vintel M50 TAB", pack: "1x10", pts: 76.15, keywords: ["VINTEL M 50", "VINTEL M50", "VINTEL-M50"] },
  { sn: 67, name: "VINVES-100 TAB", pack: "1X14", pts: 304.72, keywords: ["VINVES 100", "VINVES-100"] },
  { sn: 68, name: "VINVES-50 TAB", pack: "1X14", pts: 178.72, keywords: ["VINVES 50", "VINVES-50", "VINVSE-50", "VINVSE 50"] },
  { sn: 69, name: "XILDA 50 TAB", pack: "5x2x15", pts: 85.99, keywords: ["XILDA 50", "XILDA-50", "XILDA TAB"] },
  { sn: 70, name: "XILDA M 1000 TAB", pack: "5x2x15", pts: 78.17, keywords: ["XILDA M 1000", "XILDA-M1000", "XILDA M 1000 TAB"] },
  { sn: 71, name: "XILDA M 500 TAB", pack: "5x2x15", pts: 85.99, keywords: ["XILDA M 500", "XILDA-M 500", "XILDA M TAB", "XILDA M"] },
  { sn: 72, name: "XILDA P TAB", pack: "1x10", pts: 82.93, keywords: ["XILDA P", "XILDA-P"] },
  { sn: 73, name: "ZIRON CAPS", pack: "1x10", pts: 18.64, keywords: ["ZIRON"] }
];
'''
with open("/workspaces/Dios/src/data/masterProducts.ts", "w") as f:
    f.write(master_products_code)
print("✓ Updated masterProducts.ts with PriceList.csv PTS Rates!")

# 2. Update memoryStore.ts to hold manual PTS total override
mem_store_code = '''export interface FwDayEntry {
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
  dhruviManualPtsTotal: '' as string,
  beName: 'BANWARI LAL MEENA',
  hqName: 'UDAIPUR',
  lastSyncedMonthCode: 'AUG'
};
'''
with open("/workspaces/Dios/src/data/memoryStore.ts", "w") as f:
    f.write(mem_store_code)
print("✓ Updated memoryStore.ts with dhruviManualPtsTotal!")

# 3. Update DhruviManualModal.tsx with live PTS value counter and manual override box
modal_code = '''import React, { useState } from 'react';
import { Calculator, Search, X, Check, Trash2, Edit3, DollarSign, Layers } from 'lucide-react';
import { MASTER_PRODUCTS } from '../data/masterProducts';
import { PartyParseSummary } from '../parsers/common';
import { memoryStore, DhruviProductEntry } from '../data/memoryStore';

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

  const [manualPtsTotal, setManualPtsTotal] = useState<string>(() => {
    return memoryStore.dhruviManualPtsTotal || '';
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
    memoryStore.dhruviManualPtsTotal = manualPtsTotal;

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
      setManualPtsTotal('');
      memoryStore.dhruviEntries = {};
      memoryStore.dhruviManualPtsTotal = '';
      onClear();
    }
  };

  // Calculations
  let totalLiveSalesUnits = 0;
  let totalLiveClosingUnits = 0;
  let totalLiveSalesPtsVal = 0;
  let totalLiveClosingPtsVal = 0;

  MASTER_PRODUCTS.forEach(p => {
    const entry = draft[p.sn];
    if (entry) {
      totalLiveSalesUnits += entry.salesQty || 0;
      totalLiveClosingUnits += entry.closingQty || 0;
      totalLiveSalesPtsVal += (entry.salesQty || 0) * p.pts;
      totalLiveClosingPtsVal += (entry.closingQty || 0) * p.pts;
    }
  });

  const parsedManualVal = parseFloat(manualPtsTotal.replace(/,/g, '')) || 0;
  const variance = parsedManualVal > 0 ? (totalLiveSalesPtsVal - parsedManualVal) : 0;

  return (
    <div className="fixed inset-0 bg-slate-950/85 backdrop-blur-md z-50 flex items-center justify-center p-3 md:p-6">
      <div className="bg-slate-900 border border-amber-500/40 rounded-3xl max-w-6xl w-full p-5 md:p-6 shadow-2xl flex flex-col max-h-[92vh]">
        
        {/* Header */}
        <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-3">
          <div className="flex items-center gap-3">
            <span className="p-2.5 bg-amber-500/20 text-amber-400 rounded-xl border border-amber-500/30">
              <Calculator size={22} />
            </span>
            <div>
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                Dhruvi Manual Sheet (Excel In-Cell Formula &amp; Live PTS Value Engine)
              </h3>
              <p className="text-xs text-slate-400">
                Formula examples: <span className="text-amber-300 font-mono font-bold">+6+6 (=12)</span> or <span className="text-amber-300 font-mono font-bold">+6-2 (=4)</span>
              </p>
            </div>
          </div>
          <button onClick={onClose} className="text-slate-400 hover:text-white p-1 rounded-lg cursor-pointer">
            <X size={20} />
          </button>
        </div>

        {/* Live Top Stats Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-2.5 mb-3">
          <div className="p-2.5 bg-slate-950 rounded-xl border border-cyan-500/30">
            <div className="text-[10px] text-slate-400 uppercase font-semibold">Sales Units (SEC)</div>
            <div className="text-sm font-bold text-cyan-400 font-mono">{totalLiveSalesUnits.toLocaleString()} Units</div>
            <div className="text-[11px] text-cyan-300 font-mono font-semibold">₹ {Math.round(totalLiveSalesPtsVal).toLocaleString()}</div>
          </div>

          <div className="p-2.5 bg-slate-950 rounded-xl border border-emerald-500/30">
            <div className="text-[10px] text-slate-400 uppercase font-semibold">Closing Stock (CL)</div>
            <div className="text-sm font-bold text-emerald-400 font-mono">{totalLiveClosingUnits.toLocaleString()} Units</div>
            <div className="text-[11px] text-emerald-300 font-mono font-semibold">₹ {Math.round(totalLiveClosingPtsVal).toLocaleString()}</div>
          </div>

          <div className="p-2.5 bg-slate-950 rounded-xl border border-amber-500/40">
            <div className="text-[10px] text-amber-300 uppercase font-semibold flex items-center gap-1">
              <Edit3 size={11} /> Manual PTS Total (₹)
            </div>
            <input
              type="text"
              placeholder="e.g. 45000"
              value={manualPtsTotal}
              onChange={(e) => setManualPtsTotal(e.target.value)}
              className="w-full bg-slate-900 border border-amber-500/40 text-amber-300 font-mono font-bold text-xs rounded-lg px-2 py-1 mt-0.5 focus:outline-none focus:border-amber-400"
            />
          </div>

          <div className="p-2.5 bg-slate-950 rounded-xl border border-purple-500/30">
            <div className="text-[10px] text-slate-400 uppercase font-semibold">PTS Target Variance</div>
            <div className={`text-sm font-bold font-mono ${variance === 0 ? 'text-slate-400' : variance > 0 ? 'text-emerald-400' : 'text-rose-400'}`}>
              {parsedManualVal > 0 ? `${variance >= 0 ? '+' : ''}₹ ${Math.round(variance).toLocaleString()}` : 'No Target Set'}
            </div>
            <div className="text-[10px] text-slate-500 font-mono">Calc vs Manual</div>
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
                <th className="p-2 min-w-[200px]">Product Name</th>
                <th className="p-2 text-center w-20">Pack</th>
                <th className="p-2 text-right w-20">PTS (₹)</th>
                <th className="p-2 text-center min-w-[170px] text-cyan-400 bg-cyan-950/20">
                  Secondary Sales (Formula)
                </th>
                <th className="p-2 text-right w-24 text-cyan-300 bg-cyan-950/10">
                  Sales Val (₹)
                </th>
                <th className="p-2 text-center min-w-[170px] text-emerald-400 bg-emerald-950/20">
                  Closing Stock (Formula)
                </th>
                <th className="p-2 text-right w-24 text-emerald-300 bg-emerald-950/10">
                  Closing Val (₹)
                </th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {MASTER_PRODUCTS
                .filter(p => p.name.toLowerCase().includes(search.toLowerCase()) || String(p.sn).includes(search))
                .map(p => {
                  const entry = draft[p.sn] || { sn: p.sn, salesFormula: '', salesQty: 0, closingFormula: '', closingQty: 0 };
                  const lineSalesVal = entry.salesQty * p.pts;
                  const lineClosingVal = entry.closingQty * p.pts;

                  return (
                    <tr key={p.sn} className="hover:bg-slate-800/40 transition">
                      <td className="p-2 text-center text-slate-500 font-mono">{p.sn}</td>
                      <td className="p-2 font-medium text-white">{p.name}</td>
                      <td className="p-2 text-center text-slate-400 font-mono">{p.pack || '-'}</td>
                      <td className="p-2 text-right font-mono text-amber-300 font-semibold">{p.pts.toFixed(2)}</td>

                      {/* Sales Cell */}
                      <td className="p-1 text-center bg-cyan-950/10">
                        <div className="flex items-center gap-1.5">
                          <input
                            type="text"
                            value={entry.salesFormula}
                            onChange={e => handleCellChange(p.sn, 'sales', e.target.value)}
                            placeholder="0"
                            className="w-full py-1 px-2 bg-slate-950 rounded-lg font-mono text-xs text-cyan-300 font-bold border border-slate-800 focus:border-cyan-400 focus:outline-none text-center"
                          />
                          {entry.salesFormula && entry.salesFormula !== String(entry.salesQty) && (
                            <span className="text-[10px] bg-cyan-500/20 text-cyan-300 px-1 py-0.5 rounded font-mono font-bold shrink-0">
                              = {entry.salesQty}
                            </span>
                          )}
                        </div>
                      </td>

                      <td className="p-1.5 text-right font-mono text-cyan-300 font-bold bg-cyan-950/5">
                        {lineSalesVal > 0 ? `₹${Math.round(lineSalesVal).toLocaleString()}` : '-'}
                      </td>

                      {/* Closing Cell */}
                      <td className="p-1 text-center bg-emerald-950/10">
                        <div className="flex items-center gap-1.5">
                          <input
                            type="text"
                            value={entry.closingFormula}
                            onChange={e => handleCellChange(p.sn, 'closing', e.target.value)}
                            placeholder="0"
                            className="w-full py-1 px-2 bg-slate-950 rounded-lg font-mono text-xs text-emerald-300 font-bold border border-slate-800 focus:border-emerald-400 focus:outline-none text-center"
                          />
                          {entry.closingFormula && entry.closingFormula !== String(entry.closingQty) && (
                            <span className="text-[10px] bg-emerald-500/20 text-emerald-300 px-1 py-0.5 rounded font-mono font-bold shrink-0">
                              = {entry.closingQty}
                            </span>
                          )}
                        </div>
                      </td>

                      <td className="p-1.5 text-right font-mono text-emerald-300 font-bold bg-emerald-950/5">
                        {lineClosingVal > 0 ? `₹${Math.round(lineClosingVal).toLocaleString()}` : '-'}
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
print("✓ Updated DhruviManualModal.tsx with live PTS value counters and manual target input box!")
