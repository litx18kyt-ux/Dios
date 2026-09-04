import React, { useState, useEffect } from 'react';
import { Table2, Search, Zap, Save, Download, RefreshCw, Check, Info } from 'lucide-react';
import { MASTER_PRODUCTS } from '../../data/masterProducts';
import { unProgressionStore, MONTH_CODES } from '../../data/unProgressionStore';

export const UnSalesProgSheet: React.FC = () => {
  const [search, setSearch] = useState('');
  const [targetMonth, setTargetMonth] = useState('AUG');
  const [gridData, setGridData] = useState(() => unProgressionStore.getData());
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  const filtered = MASTER_PRODUCTS.filter(p => 
    p.name.toLowerCase().includes(search.toLowerCase()) || String(p.sn).includes(search)
  );

  const handleCellChange = (month: string, sn: number, field: 'netPri' | 'netSec' | 'closing', valStr: string) => {
    const val = parseFloat(valStr) || 0;
    unProgressionStore.updateCell(month, sn, field, val);
    setGridData({ ...unProgressionStore.getData() });
  };

  const handleAutoSyncFromMemory = () => {
    setGridData({ ...unProgressionStore.getData() });
    setStatusMsg(`🎉 Synced '${targetMonth}' from Statement Aggregator!`);
    setTimeout(() => setStatusMsg(null), 3500);
  };

  const handleSave = () => {
    setStatusMsg('✅ Data saved successfully to persistent memory!');
    setTimeout(() => setStatusMsg(null), 2500);
  };

  const handleExportCSV = () => {
    let csv = `UNIT SALES PROGRESSION (HQ TOTAL)
`;
    csv += `S.N.,PRODUCT NAME,PTS,` + MONTH_CODES.map(m => `${m} PRI,${m} SEC,${m} CL`).join(',') + `,CUMM PRI,CUMM SEC,CUMM CL,TOTAL SEC VAL (Rs)
`;
    
    MASTER_PRODUCTS.forEach(p => {
      let cummPri = 0;
      let cummSec = 0;
      let cummCl = 0;
      
      const mCells: string[] = [];
      MONTH_CODES.forEach(m => {
        const item = gridData[m]?.[p.sn] || { netPri: 0, netSec: 0, closing: 0 };
        cummPri += item.netPri || 0;
        cummSec += item.netSec || 0;
        cummCl += item.closing || 0;
        mCells.push(`${item.netPri || ''},${item.netSec || ''},${item.closing || ''}`);
      });

      const totalVal = cummSec * p.pts;
      csv += `${p.sn},"${p.name}",${p.pts.toFixed(2)},${mCells.join(',')},${cummPri},${cummSec},${cummCl},${Math.round(totalVal)}
`;
    });

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `4_UN_SALES_PROG_HQ_TOTAL.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 md:p-6 shadow-xl space-y-4">
      {/* Top Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <span className="p-2.5 bg-cyan-500/20 text-cyan-400 rounded-xl border border-cyan-500/30">
            <Table2 size={22} />
          </span>
          <div>
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              4. UNIT SALES PROGRESSION (HQ TOTAL)
              <span className="text-[10px] bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 px-2 py-0.5 rounded-full font-mono font-bold">
                12-Month Live Engine
              </span>
            </h2>
            <p className="text-xs text-slate-400">Pre-seeded APR-JUL • Auto-Sync with Statement Aggregator</p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex flex-wrap items-center gap-2.5">
          {/* Target Month Select */}
          <div className="flex items-center gap-2 bg-slate-950 px-3 py-1.5 rounded-xl border border-cyan-500/40">
            <span className="text-xs text-slate-400 font-semibold">Month:</span>
            <select
              value={targetMonth}
              onChange={(e) => setTargetMonth(e.target.value)}
              className="bg-transparent text-xs font-bold text-cyan-400 focus:outline-none cursor-pointer"
            >
              {MONTH_CODES.map(m => (
                <option key={m} value={m} className="bg-slate-900 text-white">{m} 2026</option>
              ))}
            </select>

            <button
              onClick={handleAutoSyncFromMemory}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white rounded-lg text-xs font-bold shadow-md shadow-cyan-600/20 transition cursor-pointer"
            >
              <Zap size={14} className="text-yellow-300" /> Auto-Sync {targetMonth}
            </button>
          </div>

          <button
            onClick={handleSave}
            className="flex items-center gap-1.5 px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-xl text-xs font-semibold transition cursor-pointer"
          >
            <Save size={14} /> Save
          </button>

          <button
            onClick={handleExportCSV}
            className="flex items-center gap-1.5 px-3.5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold shadow-md shadow-emerald-600/20 transition cursor-pointer"
          >
            <Download size={14} /> Export CSV
          </button>
        </div>
      </div>

      {statusMsg && (
        <div className="p-3 bg-emerald-950/70 border border-emerald-500/50 text-emerald-300 rounded-xl text-xs flex items-center gap-2">
          <Check size={16} className="text-emerald-400 shrink-0" />
          <span>{statusMsg}</span>
        </div>
      )}

      {/* Search Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
        <div className="relative w-full sm:w-80">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            placeholder="Search in 73 products..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-8 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
          />
        </div>
        <div className="text-xs text-slate-400 flex items-center gap-2">
          <Info size={14} className="text-cyan-400" />
          <span>Statement Aggregator me <b>"Sync to Data Hub"</b> karne par yahan live refresh ho jata hai.</span>
        </div>
      </div>

      {/* Main 12-Month Table */}
      <div className="overflow-x-auto max-h-[620px] border border-slate-800 rounded-xl">
        <table className="w-full text-left text-xs border-collapse">
          <thead className="sticky top-0 bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800 z-20">
            <tr>
              <th rowSpan={2} className="p-2.5 text-center w-10 bg-slate-950 border-r border-slate-800">S.N.</th>
              <th rowSpan={2} className="p-2.5 min-w-[200px] bg-slate-950 border-r border-slate-800">Product Name</th>
              <th rowSpan={2} className="p-2.5 text-right w-20 bg-slate-950 border-r border-slate-800">PTS (₹)</th>
              {MONTH_CODES.map(m => (
                <th
                  key={m}
                  colSpan={3}
                  className={`p-2 text-center border-r border-slate-800 ${m === targetMonth ? 'bg-cyan-950/60 text-cyan-300 font-extrabold border-b-2 border-cyan-400' : 'bg-slate-950'}`}
                >
                  {m} 2026
                </th>
              ))}
              <th colSpan={3} className="p-2 text-center bg-purple-950/40 text-purple-300 border-r border-slate-800">CUMM UNITS</th>
              <th rowSpan={2} className="p-2.5 text-right min-w-[110px] bg-emerald-950/40 text-emerald-300 font-bold">TOTAL SEC (₹)</th>
            </tr>
            <tr className="border-b border-slate-800 text-[10px]">
              {MONTH_CODES.map(m => (
                <React.Fragment key={m}>
                  <th className="p-1 text-center text-blue-400 bg-slate-950/80 w-14">PRI</th>
                  <th className="p-1 text-center text-cyan-400 bg-slate-950/80 w-14">SEC</th>
                  <th className="p-1 text-center text-emerald-400 bg-slate-950/80 w-14 border-r border-slate-800">CL</th>
                </React.Fragment>
              ))}
              <th className="p-1 text-center text-blue-300 bg-purple-950/30 w-14">PRI</th>
              <th className="p-1 text-center text-cyan-300 bg-purple-950/30 w-14">SEC</th>
              <th className="p-1 text-center text-emerald-300 bg-purple-950/30 w-14 border-r border-slate-800">CL</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {filtered.map(p => {
              let cummPri = 0;
              let cummSec = 0;
              let cummCl = 0;

              return (
                <tr key={p.sn} className="hover:bg-slate-800/40 transition">
                  <td className="p-2 text-center text-slate-500 font-mono border-r border-slate-800/60">{p.sn}</td>
                  <td className="p-2 font-medium text-white border-r border-slate-800/60">{p.name}</td>
                  <td className="p-2 text-right font-mono text-amber-300 border-r border-slate-800/60">{p.pts.toFixed(2)}</td>

                  {MONTH_CODES.map(m => {
                    const item = gridData[m]?.[p.sn] || { netPri: 0, netSec: 0, closing: 0 };
                    cummPri += item.netPri || 0;
                    cummSec += item.netSec || 0;
                    cummCl += item.closing || 0;
                    const isTarget = m === targetMonth;

                    return (
                      <React.Fragment key={m}>
                        {/* NET PRI */}
                        <td className={`p-0.5 text-center ${isTarget ? 'bg-blue-950/20' : ''}`}>
                          <input
                            type="text"
                            value={item.netPri !== 0 ? item.netPri : ''}
                            onChange={e => handleCellChange(m, p.sn, 'netPri', e.target.value)}
                            placeholder="-"
                            className="w-full py-1 px-1 bg-transparent text-center font-mono text-xs text-blue-300 focus:bg-slate-950 focus:outline-none"
                          />
                        </td>
                        {/* NET SEC */}
                        <td className={`p-0.5 text-center ${isTarget ? 'bg-cyan-950/20' : ''}`}>
                          <input
                            type="text"
                            value={item.netSec !== 0 ? item.netSec : ''}
                            onChange={e => handleCellChange(m, p.sn, 'netSec', e.target.value)}
                            placeholder="-"
                            className="w-full py-1 px-1 bg-transparent text-center font-mono text-xs text-cyan-300 font-bold focus:bg-slate-950 focus:outline-none"
                          />
                        </td>
                        {/* CLOSING */}
                        <td className={`p-0.5 text-center border-r border-slate-800/60 ${isTarget ? 'bg-emerald-950/20' : ''}`}>
                          <input
                            type="text"
                            value={item.closing !== 0 ? item.closing : ''}
                            onChange={e => handleCellChange(m, p.sn, 'closing', e.target.value)}
                            placeholder="-"
                            className="w-full py-1 px-1 bg-transparent text-center font-mono text-xs text-emerald-300 font-bold focus:bg-slate-950 focus:outline-none"
                          />
                        </td>
                      </React.Fragment>
                    );
                  })}

                  {/* CUMM UNITS */}
                  <td className="p-2 text-center font-mono text-blue-300 bg-purple-950/10">{cummPri || '-'}</td>
                  <td className="p-2 text-center font-mono text-cyan-300 font-bold bg-purple-950/10">{cummSec || '-'}</td>
                  <td className="p-2 text-center font-mono text-emerald-300 font-bold bg-purple-950/10 border-r border-slate-800/60">{cummCl || '-'}</td>

                  {/* TOTAL SEC VAL */}
                  <td className="p-2 text-right font-mono text-emerald-400 font-bold bg-emerald-950/10">
                    {cummSec > 0 ? `₹${Math.round(cummSec * p.pts).toLocaleString()}` : '-'}
                  </td>
                </tr>
              );
            })}
          </tbody>

          {/* Grand Total Footer */}
          <tfoot className="sticky bottom-0 bg-slate-950 border-t-2 border-cyan-500/40 font-bold z-20 shadow-2xl text-[11px]">
            {/* ROW 1: TOTAL UNITS */}
            <tr>
              <td className="p-2.5 text-center text-cyan-400 font-mono border-r border-slate-800">Σ</td>
              <td className="p-2.5 text-white border-r border-slate-800">GRAND TOTAL (UNITS)</td>
              <td className="p-2.5 text-right font-mono text-slate-500 border-r border-slate-800">-</td>
              {MONTH_CODES.map(m => {
                let priSum = 0, secSum = 0, clSum = 0;
                MASTER_PRODUCTS.forEach(p => {
                  const it = gridData[m]?.[p.sn];
                  if (it) {
                    priSum += it.netPri || 0;
                    secSum += it.netSec || 0;
                    clSum += it.closing || 0;
                  }
                });
                return (
                  <React.Fragment key={m}>
                    <td className="p-2 text-center font-mono text-blue-300 bg-blue-950/40">{priSum || '-'}</td>
                    <td className="p-2 text-center font-mono text-cyan-300 bg-cyan-950/40">{secSum || '-'}</td>
                    <td className="p-2 text-center font-mono text-emerald-300 bg-emerald-950/40 border-r border-slate-800">{clSum || '-'}</td>
                  </React.Fragment>
                );
              })}
              <td colSpan={3} className="p-2 text-center text-purple-300 font-mono bg-purple-950/40 border-r border-slate-800">12M Summary</td>
              <td className="p-2 text-right font-mono text-emerald-300 bg-emerald-950/40">-</td>
            </tr>

            {/* ROW 2: TOTAL RUPEES VALUE */}
            <tr>
              <td className="p-2.5 text-center text-emerald-400 font-mono border-r border-slate-800">₹</td>
              <td className="p-2.5 text-white border-r border-slate-800">TOTAL VALUE (RUPEES)</td>
              <td className="p-2.5 text-right font-mono text-slate-500 border-r border-slate-800">-</td>
              {MONTH_CODES.map(m => {
                let secValSum = 0;
                MASTER_PRODUCTS.forEach(p => {
                  const it = gridData[m]?.[p.sn];
                  if (it) {
                    secValSum += (it.netSec || 0) * p.pts;
                  }
                });
                return (
                  <td key={m} colSpan={3} className="p-2 text-center font-mono text-cyan-300 bg-slate-900 border-r border-slate-800">
                    {secValSum > 0 ? `₹${(secValSum / 100000).toFixed(2)}L` : '-'}
                  </td>
                );
              })}
              <td colSpan={4} className="p-2 text-center text-emerald-300 font-mono bg-slate-900">Total HQ Value</td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  );
};
