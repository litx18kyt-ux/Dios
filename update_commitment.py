import os

commitment_code = '''import React, { useState } from 'react';
import { CheckCircle2, Save, Download, Check, RefreshCw, Plus, Trash2 } from 'lucide-react';
import { memoryStore } from '../../data/memoryStore';

const MONTH_CODES = ['APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC', 'JAN', 'FEB', 'MAR'];
const MONTH_FULL = ['Apr-2026', 'May-2026', 'Jun-2026', 'Jul-2026', 'Aug-2026', 'Sep-2026', 'Oct-2026', 'Nov-2026', 'Dec-2026', 'Jan-2027', 'Feb-2027', 'Mar-2027'];

interface SupportRow {
  sn: number;
  hq: string;
  drName: string;
  typeOfSupport: string;
  amount: number | string;
  expectedRoi: number | string;
  commitments: Record<string, string>;
  achievements: Record<string, string>;
}

const INITIAL_DOCTORS_SUPPORT: SupportRow[] = [
  { sn: 1, hq: 'UDAIPUR', drName: 'JIMESH PANDYA', typeOfSupport: 'GIFT CARDS', amount: 30000, expectedRoi: 15000, commitments: { APR: '4.34', MAY: '4.55' }, achievements: { APR: '4.34', MAY: '4.74' } },
  { sn: 2, hq: 'UDAIPUR', drName: 'VIJAY GOYAL', typeOfSupport: 'GIFT CARDS', amount: 10000, expectedRoi: 10000, commitments: {}, achievements: {} },
  { sn: 3, hq: 'UDAIPUR', drName: 'JAYESH GANDHI', typeOfSupport: 'SPECIAL PLAN', amount: 50000, expectedRoi: 50000, commitments: {}, achievements: {} },
  { sn: 4, hq: 'UDAIPUR', drName: 'AK VATS', typeOfSupport: 'GIFT CARDS', amount: 30000, expectedRoi: 15000, commitments: {}, achievements: {} },
  { sn: 5, hq: 'UDAIPUR', drName: 'SANDEEP BHATNAGAR', typeOfSupport: 'GIFT CARDS', amount: 30000, expectedRoi: 150000, commitments: {}, achievements: {} },
  { sn: 6, hq: 'UDAIPUR', drName: 'RK MALOT', typeOfSupport: 'GIFT CARDS', amount: '40000', expectedRoi: 20000, commitments: {}, achievements: {} },
  { sn: 7, hq: 'UDAIPUR', drName: 'BS BOMB', typeOfSupport: 'GIFT CARDS (VINTEL)', amount: '30000+20000', expectedRoi: 30000, commitments: {}, achievements: {} },
  { sn: 8, hq: 'UDAIPUR', drName: 'RAHUL PANCHAL', typeOfSupport: 'GIFT CARDS', amount: 30000, expectedRoi: 15000, commitments: {}, achievements: {} },
  { sn: 9, hq: 'UDAIPUR', drName: 'KC JAIN', typeOfSupport: 'SPECIAL PLAN', amount: 20000, expectedRoi: 20000, commitments: {}, achievements: {} },
  { sn: 10, hq: 'UDAIPUR', drName: 'DP SINGH', typeOfSupport: 'GIFT CARDS', amount: 30000, expectedRoi: 15000, commitments: {}, achievements: {} },
  { sn: 11, hq: 'UDAIPUR', drName: 'JC DEVPURA', typeOfSupport: 'GIFT CARDS', amount: 10000, expectedRoi: 10000, commitments: {}, achievements: {} },
  { sn: 12, hq: 'UDAIPUR', drName: 'BALDEV MEENA', typeOfSupport: 'TREAD MILL', amount: 85000, expectedRoi: 50000, commitments: {}, achievements: {} },
  { sn: 13, hq: 'UDAIPUR', drName: 'KRIPA SHANKAR', typeOfSupport: 'GIFT CARDS', amount: 20000, expectedRoi: 10000, commitments: {}, achievements: {} },
];

export const CommitmentSheet: React.FC = () => {
  const [selectedPrevIdx, setSelectedPrevIdx] = useState<number>(3); // Default July (Index 3 -> APR=0, MAY=1, JUN=2, JUL=3)
  
  // Commitment of Month top box state
  const [commitmentData, setCommitmentData] = useState({
    prevBudget: '4.83',
    prevAch: '4.84',
    currSec: '4.85',
    currInventory: '7.01',
    currBudget: '4.83',
    commitmentVal: '5.50'
  });

  const [doctorsRows, setDoctorsRows] = useState<SupportRow[]>(() => {
    return memoryStore.commitmentDoctors || INITIAL_DOCTORS_SUPPORT;
  });

  const [savedSuccess, setSavedSuccess] = useState(false);

  // Auto-fill from Sales Performance data based on selected Previous Month Index
  const handleAutoFillFromPerformance = () => {
    const sp = memoryStore.salesPerformanceData;
    if (!sp) {
      alert('Pehle "3. Sales Performance" section me data save karein!');
      return;
    }

    const prevCode = MONTH_CODES[selectedPrevIdx];
    const currCode = MONTH_CODES[(selectedPrevIdx + 1) % 12];

    const prevBud = sp.budget?.[prevCode] || '4.83';
    const prevAc = sp.primary_curr?.[prevCode] || '4.84';
    const sec = sp.sec_curr?.[currCode] || '4.85';
    const inv = sp.closing_stock?.[currCode] || '7.01';
    const curBud = sp.budget?.[currCode] || '4.83';
    
    const comm = (parseFloat(curBud) * 1.2).toFixed(2);

    setCommitmentData({
      prevBudget: prevBud,
      prevAch: prevAc,
      currSec: sec,
      currInventory: inv,
      currBudget: curBud,
      commitmentVal: comm
    });

    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 2000);
  };

  const handleDoctorFieldChange = (sn: number, field: keyof SupportRow, val: any) => {
    setDoctorsRows(prev => {
      const updated = prev.map(d => d.sn === sn ? { ...d, [field]: val } : d);
      memoryStore.commitmentDoctors = updated;
      return updated;
    });
  };

  const handleDoctorNestedChange = (sn: number, type: 'commitments' | 'achievements', monthCode: string, val: string) => {
    setDoctorsRows(prev => {
      const updated = prev.map(d => {
        if (d.sn === sn) {
          return {
            ...d,
            [type]: { ...d[type], [monthCode]: val }
          };
        }
        return d;
      });
      memoryStore.commitmentDoctors = updated;
      return updated;
    });
  };

  const handleAddDoctor = () => {
    setDoctorsRows(prev => {
      const newSn = prev.length > 0 ? Math.max(...prev.map(p => p.sn)) + 1 : 1;
      const updated = [
        ...prev,
        { sn: newSn, hq: 'UDAIPUR', drName: 'NEW DOCTOR', typeOfSupport: 'GIFT CARDS', amount: 10000, expectedRoi: 10000, commitments: {}, achievements: {} }
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
    memoryStore.commitmentDoctors = doctorsRows;
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 2000);
  };

  const handleExportCSV = () => {
    let csv = `COMMITMENT OF MONTH\\n`;
    csv += `H.Q. NAME,PREVIOUS MONTH BUDGET,PREVIOUS MONTH ACH.,CURRENT SECONDARY,CURRENT INVENTORY,CURRENT MONTH BUDGET,COMMITMENT\\n`;
    csv += `UDAIPUR,${commitmentData.prevBudget},${commitmentData.prevAch},${commitmentData.currSec},${commitmentData.currInventory},${commitmentData.currBudget},${commitmentData.commitmentVal}\\n\\n`;
    
    csv += `SUPPORT REQUIREMENT\\n`;
    csv += `S.N.,H.Q.NAME,DR.NAME,TYPE OF SUPPORT,AMOUNT,EXPECTED ROI,` + MONTH_CODE_HEADERS(MONTH_CODES) + `\\n`;

    doctorsRows.forEach(d => {
      const cCells = MONTH_CODES.map(m => `C:${d.commitments[m] || ''} A:${d.achievements[m] || ''}`).join(',');
      csv += `${d.sn},${d.hq},"${d.drName}","${d.typeOfSupport}",${d.amount},${d.expectedRoi},${cCells}\\n`;
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

  function MONTH_CODE_HEADERS(codes: string[]) {
    return codes.map(m => `${m} COMMITMENT,${m} ACHIEVEMENT`).join(',');
  }

  const prevMonthLabel = MONTH_FULL[selectedPrevIdx];
  const currMonthLabel = MONTH_FULL[(selectedPrevIdx + 1) % 12];

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-6">
      
      {/* SECTION 1: COMMITMENT OF MONTH */}
      <div className="space-y-4 bg-slate-950 p-4 rounded-2xl border border-slate-800">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-800">
          <div className="flex items-center gap-2">
            <span className="p-2 bg-emerald-500/20 text-emerald-400 rounded-lg"><CheckCircle2 size={18} /></span>
            <div>
              <h2 className="text-base font-bold text-white">6. COMMITMENT OF MONTH</h2>
              <p className="text-xs text-slate-400">Select previous month to auto-calculate current commitment</p>
            </div>
          </div>

          <div className="flex items-center gap-2">
            <div className="flex items-center bg-slate-900 px-3 py-1.5 rounded-xl border border-cyan-500/40">
              <span className="text-xs text-slate-400 mr-2 font-medium">Prev Month:</span>
              <select
                value={selectedPrevIdx}
                onChange={e => setSelectedPrevIdx(parseInt(e.target.value))}
                className="bg-transparent text-xs font-bold text-cyan-400 focus:outline-none cursor-pointer"
              >
                {MONTH_FULL.map((mFull, idx) => (
                  <option key={mFull} value={idx} className="bg-slate-900 text-white">{mFull}</option>
                ))}
              </select>
            </div>

            <button
              onClick={handleAutoFillFromPerformance}
              className="flex items-center gap-1.5 px-3.5 py-2 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white text-xs font-bold rounded-xl shadow transition cursor-pointer"
            >
              <RefreshCw size={14} className="text-yellow-300" /> Auto-Fill Data
            </button>
          </div>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs border-collapse">
            <thead>
              <tr className="bg-slate-900 text-slate-400 font-bold uppercase border-b border-slate-800">
                <th className="p-2.5">H.Q. NAME</th>
                <th className="p-2.5 text-center">Prev Month Budget ({prevMonthLabel})</th>
                <th className="p-2.5 text-center">Prev Month Ach. (Primary)</th>
                <th className="p-2.5 text-center">Current Secondary ({currMonthLabel})</th>
                <th className="p-2.5 text-center">Current Inventory (Closing)</th>
                <th className="p-2.5 text-center">Current Month Budget</th>
                <th className="p-2.5 text-center text-emerald-400">Commitment (120%)</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b border-slate-800 hover:bg-slate-900/40">
                <td className="p-2.5 font-bold text-white">UDAIPUR</td>
                <td className="p-1 text-center">
                  <input
                    type="text"
                    value={commitmentData.prevBudget}
                    onChange={e => setCommitmentData({ ...commitmentData, prevBudget: e.target.value })}
                    className="w-20 bg-slate-900 border border-slate-700 text-center font-mono text-xs text-white rounded-lg py-1 focus:border-cyan-500 focus:outline-none"
                  />
                </td>
                <td className="p-1 text-center">
                  <input
                    type="text"
                    value={commitmentData.prevAch}
                    onChange={e => setCommitmentData({ ...commitmentData, prevAch: e.target.value })}
                    className="w-20 bg-slate-900 border border-slate-700 text-center font-mono text-xs text-cyan-400 rounded-lg py-1 focus:border-cyan-500 focus:outline-none font-bold"
                  />
                </td>
                <td className="p-1 text-center">
                  <input
                    type="text"
                    value={commitmentData.currSec}
                    onChange={e => setCommitmentData({ ...commitmentData, currSec: e.target.value })}
                    className="w-20 bg-slate-900 border border-slate-700 text-center font-mono text-xs text-white rounded-lg py-1 focus:border-cyan-500 focus:outline-none"
                  />
                </td>
                <td className="p-1 text-center">
                  <input
                    type="text"
                    value={commitmentData.currInventory}
                    onChange={e => setCommitmentData({ ...commitmentData, currInventory: e.target.value })}
                    className="w-20 bg-slate-900 border border-slate-700 text-center font-mono text-xs text-white rounded-lg py-1 focus:border-cyan-500 focus:outline-none"
                  />
                </td>
                <td className="p-1 text-center">
                  <input
                    type="text"
                    value={commitmentData.currBudget}
                    onChange={e => setCommitmentData({ ...commitmentData, currBudget: e.target.value })}
                    className="w-20 bg-slate-900 border border-slate-700 text-center font-mono text-xs text-white rounded-lg py-1 focus:border-cyan-500 focus:outline-none"
                  />
                </td>
                <td className="p-1 text-center">
                  <input
                    type="text"
                    value={commitmentData.commitmentVal}
                    onChange={e => setCommitmentData({ ...commitmentData, commitmentVal: e.target.value })}
                    className="w-24 bg-slate-900 border border-emerald-500/60 text-center font-mono font-bold text-xs text-emerald-400 rounded-lg py-1 focus:outline-none shadow-sm shadow-emerald-950"
                  />
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* SECTION 2: DOCTOR SUPPORT & MONTHLY COMMITMENT/ACHIEVEMENT */}
      <div className="space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-2">
          <h3 className="text-sm font-bold text-white">Support Requirement &amp; Doctor-wise Monthly Commitments</h3>
          
          <div className="flex items-center gap-2">
            <button
              onClick={handleAddDoctor}
              className="flex items-center gap-1 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-cyan-300 rounded-xl text-xs font-semibold transition cursor-pointer"
            >
              <Plus size={14} /> Add Doctor Support
            </button>
            <button
              onClick={handleSave}
              className="flex items-center gap-1.5 px-3.5 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-xl text-xs font-semibold transition cursor-pointer"
            >
              {savedSuccess ? <Check size={14} className="text-emerald-400" /> : <Save size={14} />}
              {savedSuccess ? 'Saved' : 'Save'}
            </button>
            <button
              onClick={handleExportCSV}
              className="flex items-center gap-1.5 px-3.5 py-1.5 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold transition cursor-pointer"
            >
              <Download size={14} /> Export CSV
            </button>
          </div>
        </div>

        <div className="overflow-x-auto max-h-[500px] border border-slate-800 rounded-xl">
          <table className="w-full text-left text-xs border-collapse">
            <thead className="sticky top-0 bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800 z-20">
              <tr>
                <th className="p-2.5 text-center w-10">S.N.</th>
                <th className="p-2.5 min-w-[180px]">Doctor Name</th>
                <th className="p-2.5 min-w-[150px]">Type of Support</th>
                <th className="p-2.5 text-right w-24">Amount (₹)</th>
                <th className="p-2.5 text-right w-24 text-emerald-400">Expected ROI</th>
                {MONTH_CODES.map(m => (
                  <th key={m} colSpan={2} className="p-2 text-center border-r border-slate-800 bg-slate-900">
                    {m} (C / A)
                  </th>
                ))}
                <th className="p-2.5 text-center w-12">Action</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {doctorsRows.map(doc => (
                <tr key={doc.sn} className="hover:bg-slate-800/40 transition">
                  <td className="p-2 text-center text-slate-500 font-mono">{doc.sn}</td>
                  <td className="p-1">
                    <input
                      type="text"
                      value={doc.drName}
                      onChange={e => handleDoctorFieldChange(doc.sn, 'drName', e.target.value)}
                      className="w-full py-1.5 px-2 bg-slate-950 rounded-lg font-semibold text-white border border-slate-800 focus:border-cyan-500 focus:outline-none text-xs"
                    />
                  </td>
                  <td className="p-1">
                    <input
                      type="text"
                      value={doc.typeOfSupport}
                      onChange={e => handleDoctorFieldChange(doc.sn, 'typeOfSupport', e.target.value)}
                      className="w-full py-1.5 px-2 bg-slate-950 rounded-lg text-slate-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-xs"
                    />
                  </td>
                  <td className="p-1">
                    <input
                      type="text"
                      value={doc.amount}
                      onChange={e => handleDoctorFieldChange(doc.sn, 'amount', e.target.value)}
                      className="w-full py-1.5 px-2 bg-slate-950 rounded-lg font-mono text-right text-slate-200 border border-slate-800 focus:border-cyan-500 focus:outline-none text-xs"
                    />
                  </td>
                  <td className="p-1">
                    <input
                      type="text"
                      value={doc.expectedRoi}
                      onChange={e => handleDoctorFieldChange(doc.sn, 'expectedRoi', e.target.value)}
                      className="w-full py-1.5 px-2 bg-slate-950 rounded-lg font-mono font-bold text-right text-emerald-400 border border-slate-800 focus:border-cyan-500 focus:outline-none text-xs"
                    />
                  </td>

                  {MONTH_CODES.map(m => (
                    <React.Fragment key={m}>
                      {/* Commitment */}
                      <td className="p-0.5 text-center bg-blue-950/20">
                        <input
                          type="text"
                          value={doc.commitments[m] || ''}
                          onChange={e => handleDoctorNestedChange(doc.sn, 'commitments', m, e.target.value)}
                          placeholder="C"
                          className="w-12 py-1 px-1 bg-transparent text-center font-mono text-[11px] text-blue-300 focus:bg-slate-950 focus:outline-none"
                        />
                      </td>
                      {/* Achievement */}
                      <td className="p-0.5 text-center border-r border-slate-800/60 bg-emerald-950/20">
                        <input
                          type="text"
                          value={doc.achievements[m] || ''}
                          onChange={e => handleDoctorNestedChange(doc.sn, 'achievements', m, e.target.value)}
                          placeholder="A"
                          className="w-12 py-1 px-1 bg-transparent text-center font-mono text-[11px] text-emerald-300 font-bold focus:bg-slate-950 focus:outline-none"
                        />
                      </td>
                    </React.Fragment>
                  ))}

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
              ))}
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
print('✅ CommitmentSheet.tsx updated with dynamic month dropdown, auto-fill from Sales Performance, and doctor support tables!')
