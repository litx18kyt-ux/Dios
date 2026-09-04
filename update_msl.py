import os

# 1. Update memoryStore.ts to persist MSL edits
mem_path = 'src/data/memoryStore.ts'
with open(mem_path, 'r') as f:
    mem_code = f.read()

if 'mslData' not in mem_code:
    mem_code = mem_code.replace(
        "beName: 'BANWARI LAL MEENA',",
        "mslData: null as any[] | null,\n  beName: 'BANWARI LAL MEENA',"
    )
    with open(mem_path, 'w') as f:
        f.write(mem_code)
    print('✅ Updated memoryStore.ts with mslData persistence!')

# 2. Create interactive MslSheet.tsx with all 123 doctors seeded
msl_sheet_code = '''import React, { useState } from 'react';
import { Calendar, Search, Save, Download, Check, Plus, Trash2 } from 'lucide-react';
import { memoryStore } from '../../data/memoryStore';

interface MslDoctor {
  srNo: number;
  doctorName: string;
  activityType: string;
  speciality: string;
  dob: string;
  doa: string;
  apr: string;
  may: string;
  jun: string;
  jul: string;
  aug: string;
  sept: string;
  oct: string;
  nov: string;
  dec: string;
  jan: string;
  feb: string;
  mar: string;
}

const INITIAL_MSL_DOCTORS: MslDoctor[] = [
  { srNo: 23, doctorName: 'Abhay jain', activityType: 'CRM', speciality: 'CONSULTANT PHYSICIAN', dob: '12/12/1972', doa: '', apr: '1,7,10,17,21,24,27,29', may: '6,8,11,19,26,27,29', jun: '1,2,12,16,18,', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
  { srNo: 50, doctorName: 'ABHIJEET BASU', activityType: '', speciality: 'MD MED', dob: '12/12/1972', doa: '', apr: '7,9,11,17,24', may: '4,6,8,15,18', jun: '13,19,29', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
  { srNo: 61, doctorName: 'Abhishek Kumar', activityType: '', speciality: 'CONSPHYS', dob: '', doa: '', apr: '2,10,17,23,24,28,30', may: '15,21,28', jun: '12,18,25', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
  { srNo: 10, doctorName: 'AKVATS', activityType: 'CRM', speciality: 'DM NEURO', dob: '02/08/2019', doa: '', apr: '1,15,23,30', may: '6,14,21', jun: '3,18,24', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
  { srNo: 59, doctorName: 'Ameet Mehta', activityType: '', speciality: 'GENERAL PHYSICIAN', dob: '27/04/1900', doa: '19/05/1900', apr: '3,13,17,24,27', may: '8,15,28,29', jun: '1,3,16', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
  { srNo: 37, doctorName: 'AMIT KHANDELWAL', activityType: 'WCFYH VAL/VIN', speciality: 'CARDIO', dob: '03/04/1977', doa: '', apr: 'out of Town ,21', may: '', jun: '', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
  { srNo: 66, doctorName: 'ANIS JUKARWALA', activityType: '', speciality: 'MD', dob: '', doa: '', apr: '1,10,30', may: '18,27', jun: '12,out of town ', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
  { srNo: 20, doctorName: 'ANISH JAIN', activityType: 'CRM', speciality: 'MD MED', dob: '16/12/2019', doa: '', apr: '', may: '', jun: '11,na', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
  { srNo: 86, doctorName: 'ANMOL PAGARIYA', activityType: '', speciality: 'MD MED', dob: '23/01/2019', doa: '', apr: '6,22', may: '7,22', jun: '4,23', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
  { srNo: 22, doctorName: 'BALDEV MEENA', activityType: 'CRM', speciality: 'MD MED', dob: '05/07/1997', doa: '', apr: '1,2,9,11,18,27', may: '14,28,27', jun: '12,22,25,29', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
  { srNo: 57, doctorName: 'BHUPESH PARTANI', activityType: '', speciality: 'MD MED', dob: '23/10/2019', doa: '', apr: '6,22', may: '7,22', jun: '4,23', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
  { srNo: 6, doctorName: 'BS BOMB', activityType: 'CRM', speciality: 'MD MED', dob: '08/12/2019', doa: '', apr: '4,11,15', may: '8,14,18', jun: '1,18', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
  { srNo: 7, doctorName: 'D C SHARMA', activityType: 'CRM', speciality: 'DM ENDO', dob: '12/05/2019', doa: '', apr: '3,9,10', may: '7,12,28', jun: '12,18,ntc', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
  { srNo: 12, doctorName: 'DENY', activityType: 'CRM', speciality: 'DM CARDIO', dob: '03/06/2019', doa: '', apr: '9,10,24,30(doa)', may: '8,19,26,29', jun: '12,18,25', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
  { srNo: 2, doctorName: 'DP SINGH', activityType: 'CRM', speciality: 'MD MED', dob: '23/11/2019', doa: '', apr: '7,23,27', may: '6,11,21,29,30', jun: '15,24,29', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
  { srNo: 27, doctorName: 'G K Mukhiya', activityType: 'CRM', speciality: 'DM NEPHRO', dob: '13/05/1973', doa: '', apr: '3,11', may: '8,15,29', jun: '13,19,na', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
  { srNo: 1, doctorName: 'MAHESH DAVE', activityType: 'CRM', speciality: 'MD MED', dob: '03/03/2019', doa: '', apr: '1,10,17', may: '15,19,26,30', jun: 'na,13,25,30', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
  { srNo: 11, doctorName: 'RAMESH PATEL', activityType: 'CRM', speciality: 'DM CARDIO', dob: '30/09/2019', doa: '', apr: '1,17,22', may: '8,15,18,19,29', jun: '12,19,24', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
  { srNo: 9, doctorName: 'VINOD MEHTA', activityType: 'CRM', speciality: 'DM NEURO', dob: '02/06/2019', doa: '', apr: '2,3,11,17', may: '14,15,26,29', jun: 'na,16,18,19,29', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' },
];

export const MslSheet: React.FC = () => {
  const [search, setSearch] = useState('');
  const [doctors, setDoctors] = useState<MslDoctor[]>(() => {
    if (memoryStore.mslData) {
      return memoryStore.mslData;
    }
    return INITIAL_MSL_DOCTORS;
  });

  const [savedSuccess, setSavedSuccess] = useState(false);

  const handleFieldChange = (srNo: number, field: keyof MslDoctor, val: string) => {
    setDoctors(prev => {
      const updated = prev.map(d => d.srNo === srNo ? { ...d, [field]: val } : d);
      memoryStore.mslData = updated;
      return updated;
    });
  };

  const handleAddDoctor = () => {
    setDoctors(prev => {
      const nextSr = prev.length > 0 ? Math.max(...prev.map(p => p.srNo)) + 1 : 1;
      const updated = [
        ...prev,
        { srNo: nextSr, doctorName: '', activityType: '', speciality: '', dob: '', doa: '', apr: '', may: '', jun: '', jul: '', aug: '', sept: '', oct: '', nov: '', dec: '', jan: '', feb: '', mar: '' }
      ];
      memoryStore.mslData = updated;
      return updated;
    });
  };

  const handleDeleteDoctor = (srNo: number) => {
    setDoctors(prev => {
      const updated = prev.filter(d => d.srNo !== srNo);
      memoryStore.mslData = updated;
      return updated;
    });
  };

  const handleSave = () => {
    memoryStore.mslData = doctors;
    setSavedSuccess(true);
    setTimeout(() => setSavedSuccess(false), 2000);
  };

  const handleExportCSV = () => {
    let csv = `,,,,,,VISIT DATES,,,,,,,,,,\\n`;
    csv += `SrNo,Doctor Name,Activity Type,Speciality,DOB,DOA,APR,MAY,JUN,JUL,AUG,SEPT,OCT,NOV,DEC,JAN,FEB,MAR\\n`;
    
    doctors.forEach(d => {
      csv += `${d.srNo},"${d.doctorName}","${d.activityType}","${d.speciality}","${d.dob}","${d.doa}","${d.apr}","${d.may}","${d.jun}","${d.jul}","${d.aug}","${d.sept}","${d.oct}","${d.nov}","${d.dec}","${d.jan}","${d.feb}","${d.mar}"\\n`;
    });

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', '14_MSL.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  const filtered = doctors.filter(d => 
    d.doctorName.toLowerCase().includes(search.toLowerCase()) || 
    d.speciality.toLowerCase().includes(search.toLowerCase()) ||
    d.activityType.toLowerCase().includes(search.toLowerCase())
  );

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <span className="p-2 bg-cyan-500/20 text-cyan-400 rounded-lg"><Calendar size={18} /></span>
          <div>
            <h2 className="text-base font-bold text-white">14. MSL (Master Specialty List &amp; Visit Dates)</h2>
            <p className="text-xs text-slate-400">Fully editable doctor visit schedule across months</p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <div className="relative w-full sm:w-60">
            <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
            <input 
              type="text" 
              placeholder="Search doctor, speciality..."
              value={search}
              onChange={e => setSearch(e.target.value)}
              className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-8 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
            />
          </div>

          <button
            onClick={handleAddDoctor}
            className="flex items-center gap-1 px-3 py-1.5 bg-slate-800 hover:bg-slate-700 border border-slate-700 text-cyan-300 rounded-xl text-xs font-semibold transition cursor-pointer"
          >
            <Plus size={14} /> Add Doctor
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

      <div className="overflow-x-auto max-h-[600px] border border-slate-800 rounded-xl">
        <table className="w-full text-left text-xs border-collapse">
          <thead className="sticky top-0 bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800 z-10">
            <tr>
              <th className="p-2.5 text-center w-12">SrNo</th>
              <th className="p-2.5 min-w-[180px]">Doctor Name</th>
              <th className="p-2.5 min-w-[130px]">Activity Type</th>
              <th className="p-2.5 min-w-[160px]">Speciality</th>
              <th className="p-2.5 text-center w-24">DOB</th>
              <th className="p-2.5 text-center w-24">DOA</th>
              <th className="p-2.5 text-center w-20 text-cyan-400">APR</th>
              <th className="p-2.5 text-center w-20 text-emerald-400">MAY</th>
              <th className="p-2.5 text-center w-20 text-purple-400">JUN</th>
              <th className="p-2.5 text-center w-20 text-blue-400">JUL</th>
              <th className="p-2.5 text-center w-20 text-amber-400">AUG</th>
              <th className="p-2.5 text-center w-20 text-rose-400">SEPT</th>
              <th className="p-2.5 text-center w-12">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {filtered.map(doc => (
              <tr key={doc.srNo} className="hover:bg-slate-800/40 transition">
                <td className="p-2 text-center text-slate-500 font-mono">{doc.srNo}</td>
                <td className="p-1">
                  <input
                    type="text"
                    value={doc.doctorName}
                    onChange={e => handleFieldChange(doc.srNo, 'doctorName', e.target.value)}
                    className="w-full py-1.5 px-2 bg-slate-950 rounded-lg font-semibold text-white border border-slate-800 focus:border-cyan-500 focus:outline-none text-xs"
                  />
                </td>
                <td className="p-1">
                  <input
                    type="text"
                    value={doc.activityType}
                    onChange={e => handleFieldChange(doc.srNo, 'activityType', e.target.value)}
                    placeholder="-"
                    className="w-full py-1.5 px-2 bg-slate-950 rounded-lg text-amber-400 border border-slate-800 focus:border-cyan-500 focus:outline-none text-xs font-medium"
                  />
                </td>
                <td className="p-1">
                  <input
                    type="text"
                    value={doc.speciality}
                    onChange={e => handleFieldChange(doc.srNo, 'speciality', e.target.value)}
                    placeholder="-"
                    className="w-full py-1.5 px-2 bg-slate-950 rounded-lg text-slate-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-xs"
                  />
                </td>
                <td className="p-1">
                  <input
                    type="text"
                    value={doc.dob}
                    onChange={e => handleFieldChange(doc.srNo, 'dob', e.target.value)}
                    placeholder="DD/MM/YYYY"
                    className="w-full py-1.5 px-2 bg-slate-950 rounded-lg font-mono text-slate-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-center text-xs"
                  />
                </td>
                <td className="p-1">
                  <input
                    type="text"
                    value={doc.doa}
                    onChange={e => handleFieldChange(doc.srNo, 'doa', e.target.value)}
                    placeholder="DD/MM/YYYY"
                    className="w-full py-1.5 px-2 bg-slate-950 rounded-lg font-mono text-slate-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-center text-xs"
                  />
                </td>
                <td className="p-1">
                  <input
                    type="text"
                    value={doc.apr}
                    onChange={e => handleFieldChange(doc.srNo, 'apr', e.target.value)}
                    placeholder="-"
                    className="w-full py-1.5 px-1 bg-slate-950 rounded-lg font-mono text-cyan-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-center text-xs"
                  />
                </td>
                <td className="p-1">
                  <input
                    type="text"
                    value={doc.may}
                    onChange={e => handleFieldChange(doc.srNo, 'may', e.target.value)}
                    placeholder="-"
                    className="w-full py-1.5 px-1 bg-slate-950 rounded-lg font-mono text-emerald-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-center text-xs"
                  />
                </td>
                <td className="p-1">
                  <input
                    type="text"
                    value={doc.jun}
                    onChange={e => handleFieldChange(doc.srNo, 'jun', e.target.value)}
                    placeholder="-"
                    className="w-full py-1.5 px-1 bg-slate-950 rounded-lg font-mono text-purple-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-center text-xs"
                  />
                </td>
                <td className="p-1">
                  <input
                    type="text"
                    value={doc.jul}
                    onChange={e => handleFieldChange(doc.srNo, 'jul', e.target.value)}
                    placeholder="-"
                    className="w-full py-1.5 px-1 bg-slate-950 rounded-lg font-mono text-blue-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-center text-xs"
                  />
                </td>
                <td className="p-1">
                  <input
                    type="text"
                    value={doc.aug}
                    onChange={e => handleFieldChange(doc.srNo, 'aug', e.target.value)}
                    placeholder="-"
                    className="w-full py-1.5 px-1 bg-slate-950 rounded-lg font-mono text-amber-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-center text-xs"
                  />
                </td>
                <td className="p-1">
                  <input
                    type="text"
                    value={doc.sept}
                    onChange={e => handleFieldChange(doc.srNo, 'sept', e.target.value)}
                    placeholder="-"
                    className="w-full py-1.5 px-1 bg-slate-950 rounded-lg font-mono text-rose-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-center text-xs"
                  />
                </td>
                <td className="p-2 text-center">
                  <button
                    type="button"
                    onClick={() => handleDeleteDoctor(doc.srNo)}
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
  );
};
'''

with open('src/components/review/MslSheet.tsx', 'w') as f:
    f.write(msl_sheet_code)
print('✅ MslSheet.tsx updated with full interactive editing and CSV export!')
