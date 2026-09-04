import os

commitment_code = '''import React, { useState } from 'react';
import { CheckCircle2, Save, Download, Check, RefreshCw, Plus, Trash2, Calendar } from 'lucide-react';
import { memoryStore } from '../../data/memoryStore';

const MONTHS_DATA = [
  { code: 'APR', label: 'APRIL' },
  { code: 'MAY', label: 'MAY' },
  { code: 'JUN', label: 'JUNE' },
  { code: 'JUL', label: 'JULY' },
  { code: 'AUG', label: 'AUGUST' },
  { code: 'SEP', label: 'SEPTEMBER' },
  { code: 'OCT', label: 'OCTOBER' },
  { code: 'NOV', label: 'NOVEMBER' },
  { code: 'DEC', label: 'DECEMBER' },
  { code: 'JAN', label: 'JANUARY' },
  { code: 'FEB', label: 'FEBRUARY' },
  { code: 'MAR', label: 'MARCH' }
];

interface SupportRow {
  sn: number;
  hq: string;
  drName: string;
  typeOfSupport: string;
  amount: string;
  expectedRoi: string;
}

export const CommitmentSheet: React.FC = () => {
  // 12-Month Commitment & Achievement State
  const [monthlyCA, setMonthlyCA] = useState<Record<string, { commitment: string; achievement: string }>>(() => {
    if (memoryStore.commitmentMonthlyCA) {
      return memoryStore.commitmentMonthlyCA;
    }
    const initial: Record<string, { commitment: string; achievement: string }> = {};
    MONTHS_DATA.forEach(m => {
      initial[m.code] = { commitment: '', achievement: '' };
    });
    return initial;
  });

  // Support Requirement Table State (Blank by default)
  const [doctorsRows, setDoctorsRows] = useState<SupportRow[]>(() => {
    return memoryStore.commitmentDoctors || [];
  });

  const [savedSuccess, setSavedSuccess] = useState(false);

  // Auto-Sync 12M Commitment (Budget) & Achievement (Primary) from Sales Performance
  const handleAutoSyncCA = () => {
    const sp = memoryStore.salesPerformanceData;
    if (!sp) {
      alert('Pehle "3. Sales Performance" section me data save karein!');
      return;
    }

    const updated: Record<string, { commitment: string; achievement: string }> = {};
    MONTHS_DATA.forEach(m => {
      const budgetVal = sp.budget?.[m.code] || '';
      const primaryVal = sp.primary_curr?.[m.code] || '';
      updated[m.code] = {
        commitment: budgetVal,
        achievement: primaryVal
      };
    });

    setMonthlyCA(updated);
    memoryStore.commitmentMonthlyCA = updated;
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 2000);
  };

  const handleCAMonthChange = (code: string, field: 'commitment' | 'achievement', val: string) => {
    setMonthlyCA(prev => {
      const updated = {
        ...prev,
        [code]: {
          ...prev[code],
          [field]: val
        }
      };
      memoryStore.commitmentMonthlyCA = updated;
      return updated;
    });
  };

  const handleDoctorFieldChange = (sn: number, field: keyof SupportRow, val: string) => {
    setDoctorsRows(prev => {
      const updated = prev.map(d => d.sn === sn ? { ...d, [field]: val } : d);
      memoryStore.commitmentDoctors = updated;
      return updated;
    });
  };

  const handleAddDoctor = () => {
    setDoctorsRows(prev => {
      const newSn = prev.length > 0 ? Math.max(...prev.map(p => p.sn)) + 1 : 1;
      const updated = [
        ...prev,
        { sn: newSn, hq: 'UDAIPUR', drName: '', typeOfSupport: '', amount: '', expectedRoi: '' }
      ];
      memoryStore.commitmentDoctors = updated;
      return updated;
    });
  };

  const handleDeleteDoctor = (sn: number) => {
    setDoctorsRows(prev => {
      const updated = prev.filter(d => d.sn !== sn);
      memoryStore.commitmentDoctors = updated;
      return updated;
    });
  };

  const handleSave = () => {
    memoryStore.commitmentMonthlyCA = monthlyCA;
    memoryStore.commitmentDoctors = doctorsRows;
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 2000);
  };

  const handleExportCSV = () => {
    let csv = `12-MONTH COMMITMENT & ACHIEVEMENT\\n`;
    csv += `MONTH,COMMITMENT,ACHIEVEMENT\\n`;
    MONTHS_DATA.forEach(m => {
      const item = monthlyCA[m.code] || { commitment: '', achievement: '' };
      csv += `${m.label},${item.commitment},${item.achievement}\\n`;
    });
    csv += `\\nSUPPORT REQUIREMENT\\n`;
    csv += `S.N.,H.Q.NAME,DR.NAME,TYPE OF SUPPORT,AMOUNT,EXPECTED ROI\\n`;
    doctorsRows.forEach(d => {
      csv += `${d.sn},${d.hq},"${d.drName}","${d.typeOfSupport}",${d.amount},${d.expectedRoi}\\n`;
    });

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', '6_COMMITMENT.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-6">
      
      {/* HEADER & AUTO-SYNC CONTROLS */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <span className="p-2 bg-emerald-500/20 text-emerald-400 rounded-lg"><CheckCircle2 size={18} /></span>
          <div>
            <h2 className="text-base font-bold text-white">6. COMMITMENT &amp; ACHIEVEMENT (12-MONTH GRID)</h2>
            <p className="text-xs text-slate-400">Monthly budget commitment vs primary achievement tracking</p>
          </div>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleAutoSyncCA}
            className="flex items-center gap-1.5 px-3.5 py-2 bg-cyan-600 hover:bg-cyan-500 text-white text-xs font-bold rounded-xl shadow transition cursor-pointer"
          >
            <RefreshCw size={14} className="text-yellow-300" /> Auto-Sync from Performance
          </button>

          <button
            onClick={handleSave}
            className="flex items-center gap-1.5 px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-xl text-xs font-semibold transition cursor-pointer"
          >
            {savedSuccess ? <Check size={14} className="text-emerald-400" /> : <Save size={14} />}
            {savedSuccess ? 'Saved' : 'Save'}
          </button>

          <button
            onClick={handleExportCSV}
            className="flex items-center gap-1.5 px-3.5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold transition cursor-pointer"
          >
            <Download size={14} /> Export CSV
          </button>
        </div>
      </div>

      {/* 12-MONTH COMMITMENT & ACHIEVEMENT BOXES (EXACTLY AS REQUESTED) */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
        {MONTHS_DATA.map(m => {
          const dataItem = monthlyCA[m.code] || { commitment: '', achievement: '' };
          return (
            <div key={m.code} className="bg-slate-950 rounded-2xl border border-slate-800 overflow-hidden shadow-lg flex flex-col justify-between">
              {/* Month Yellow/Cyan Header Banner */}
              <div className="bg-slate-900 border-b border-slate-800 py-2 px-3 text-center">
                <span className="text-xs font-black tracking-wider text-amber-300">{m.label}</span>
              </div>

              {/* Sub-table for Commitment & Achievement */}
              <div className="grid grid-cols-2 text-center divide-x divide-slate-800 border-b border-slate-800 text-[10px] text-slate-400 font-bold uppercase bg-slate-900/40">
                <div className="py-1 px-1">Commitment</div>
                <div className="py-1 px-1">Achievement</div>
              </div>

              <div className="grid grid-cols-2 divide-x divide-slate-800 p-2 gap-2 bg-slate-950">
                <div>
                  <input
                    type="text"
                    value={dataItem.commitment}
                    onChange={e => handleCAMonthChange(m.code, 'commitment', e.target.value)}
                    placeholder="-"
                    className="w-full py-1.5 px-1 bg-slate-900 rounded-lg text-center font-mono font-bold text-cyan-400 text-xs border border-slate-800 focus:border-cyan-500 focus:outline-none"
                  />
                </div>
                <div>
                  <input
                    type="text"
                    value={dataItem.achievement}
                    onChange={e => handleCAMonthChange(m.code, 'achievement', e.target.value)}
                    placeholder="-"
                    className="w-full py-1.5 px-1 bg-slate-900 rounded-lg text-center font-mono font-bold text-emerald-400 text-xs border border-slate-800 focus:border-cyan-500 focus:outline-none"
                  />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      {/* SUPPORT REQUIREMENT TABLE (SEPARATE SECTION AT BOTTOM) */}
      <div className="space-y-4 pt-4 border-t border-slate-800">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-2">
          <div>
            <h3 className="text-sm font-bold text-white uppercase tracking-wider">Support Requirement (Doctor-wise Investment Analysis)</h3>
            <p className="text-xs text-slate-400">Separate support table (independent of monthly C/A blocks)</p>
          </div>
          
          <button
            onClick={handleAddDoctor}
            className="flex items-center gap-1.5 px-3.5 py-2 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-cyan-300 rounded-xl text-xs font-semibold transition cursor-pointer"
          >
            <Plus size={14} /> Add Support Row
          </button>
        </div>

        <div className="overflow-x-auto max-h-[400px] border border-slate-800 rounded-xl">
          <table className="w-full text-left text-xs border-collapse">
            <thead className="sticky top-0 bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800 z-10">
              <tr>
                <th className="p-2.5 text-center w-12">S.N.</th>
                <th className="p-2.5 min-w-[200px]">Doctor Name</th>
                <th className="p-2.5 min-w-[180px]">Type of Support</th>
                <th className="p-2.5 text-right w-32">Amount (₹)</th>
                <th className="p-2.5 text-right w-32 text-emerald-400">Expected ROI (₹)</th>
                <th className="p-2.5 text-center w-16">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {doctorsRows.length === 0 ? (
                <tr>
                  <td colSpan={6} className="p-8 text-center text-slate-500">
                    No support rows added yet. Click <b>"Add Support Row"</b> above to add doctor support.
                  </td>
                </tr>
              ) : (
                doctorsRows.map(doc => (
                  <tr key={doc.sn} className="hover:bg-slate-800/40 transition">
                    <td className="p-2 text-center text-slate-500 font-mono">{doc.sn}</td>
                    <td className="p-1">
                      <input
                        type="text"
                        value={doc.drName}
                        onChange={e => handleDoctorFieldChange(doc.sn, 'drName', e.target.value)}
                        placeholder="Doctor Name"
                        className="w-full py-1.5 px-2 bg-slate-950 rounded-lg font-semibold text-white border border-slate-800 focus:border-cyan-500 focus:outline-none text-xs"
                      />
                    </td>
                    <td className="p-1">
                      <input
                        type="text"
                        value={doc.typeOfSupport}
                        onChange={e => handleDoctorFieldChange(doc.sn, 'typeOfSupport', e.target.value)}
                        placeholder="e.g. Gift Cards / Dinner"
                        className="w-full py-1.5 px-2 bg-slate-950 rounded-lg text-slate-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-xs"
                      />
                    </td>
                    <td className="p-1">
                      <input
                        type="text"
                        value={doc.amount}
                        onChange={e => handleDoctorFieldChange(doc.sn, 'amount', e.target.value)}
                        placeholder="0"
                        className="w-full py-1.5 px-2 bg-slate-950 rounded-lg font-mono text-right text-slate-200 border border-slate-800 focus:border-cyan-500 focus:outline-none text-xs"
                      />
                    </td>
                    <td className="p-1">
                      <input
                        type="text"
                        value={doc.expectedRoi}
                        onChange={e => handleDoctorFieldChange(doc.sn, 'expectedRoi', e.target.value)}
                        placeholder="0"
                        className="w-full py-1.5 px-2 bg-slate-950 rounded-lg font-mono font-bold text-right text-emerald-400 border border-slate-800 focus:border-cyan-500 focus:outline-none text-xs"
                      />
                    </td>
                    <td className="p-2 text-center">
                      <button
                        type="button"
                        onClick={() => handleDeleteDoctor(doc.sn)}
                        className="p-1.5 text-slate-500 hover:text-rose-400 rounded-lg transition cursor-pointer"
                      >
                        <Trash2 size={15} />
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
};
'''

with open('src/components/review/CommitmentSheet.tsx', 'w') as f:
    f.write(commitment_code)
print('✅ CommitmentSheet.tsx updated with separate 12-Month C/A boxes and clean Support table!')
