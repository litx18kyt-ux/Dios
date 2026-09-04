import os, json, csv

# 1. Parse CSV doctors
csv_path = 'csv_output/14_MSL.csv'
doctors = []
if os.path.exists(csv_path):
    with open(csv_path, mode='r', encoding='utf-8', errors='ignore') as f:
        reader = csv.reader(f)
        rows = list(reader)
        start = 0
        for i, r in enumerate(rows):
            if any('Doctor Name' in cell for cell in r):
                start = i + 1
                break
        for r in rows[start:]:
            if len(r) >= 2 and r[1].strip():
                try:
                    sr = int(r[0].strip())
                except:
                    sr = len(doctors) + 1
                pad = lambda idx: r[idx].strip() if len(r) > idx else ''
                doctors.append({
                    'srNo': sr, 'doctorName': pad(1), 'activityType': pad(2), 'speciality': pad(3),
                    'dob': pad(4), 'doa': pad(5), 'apr': pad(6), 'may': pad(7), 'jun': pad(8),
                    'jul': pad(9), 'aug': pad(10), 'sept': pad(11), 'oct': pad(12), 'nov': pad(13),
                    'dec': pad(14), 'jan': pad(15), 'feb': pad(16), 'mar': pad(17)
                })

print(f"Loaded {len(doctors)} doctors from CSV.")

# 2. Generate MslSheet.tsx with iPad-perfect sticky columns & 160px wide months
msl_content = '''import React, { useState } from 'react';
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

const FULL_123_MSL_DOCTORS: MslDoctor[] = ''' + json.dumps(doctors, indent=2) + ''';

export const MslSheet: React.FC = () => {
  const [search, setSearch] = useState('');
  const [doctors, setDoctors] = useState<MslDoctor[]>(() => {
    if (memoryStore.mslData) {
      return memoryStore.mslData;
    }
    return FULL_123_MSL_DOCTORS;
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
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              14. MSL (Master Specialty List &amp; Visit Dates)
              <span className="text-[10px] bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 px-2 py-0.5 rounded-full font-mono font-bold">
                SYSTEM V55.0 • DOA FROZEN
              </span>
            </h2>
            <p className="text-xs text-slate-400">Total {doctors.length} Doctors • DOA Tak Columns Frozen • 160px Wide Month Inputs</p>
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

      {/* TABLE WITH SAFARI/IPAD STICKY FROZEN PANES UP TO DOA */}
      <div className="overflow-x-auto max-h-[640px] border border-slate-800 rounded-2xl relative shadow-2xl">
        <table className="w-full text-left text-xs border-separate border-spacing-0">
          <thead className="sticky top-0 z-40 bg-slate-950">
            <tr>
              <th className="p-2.5 text-center w-[50px] min-w-[50px] bg-slate-950 border-b border-r border-slate-800 sticky left-0 z-50 text-slate-400 font-bold uppercase">
                SrNo
              </th>
              <th className="p-2.5 w-[200px] min-w-[200px] bg-slate-950 border-b border-r border-slate-800 sticky left-[50px] z-50 text-slate-400 font-bold uppercase">
                Doctor Name
              </th>
              <th className="p-2.5 w-[140px] min-w-[140px] bg-slate-950 border-b border-r border-slate-800 sticky left-[250px] z-50 text-slate-400 font-bold uppercase">
                Activity Type
              </th>
              <th className="p-2.5 w-[180px] min-w-[180px] bg-slate-950 border-b border-r border-slate-800 sticky left-[390px] z-50 text-slate-400 font-bold uppercase">
                Speciality
              </th>
              <th className="p-2.5 text-center w-[100px] min-w-[100px] bg-slate-950 border-b border-r border-slate-800 sticky left-[570px] z-50 text-slate-400 font-bold uppercase">
                DOB
              </th>
              <th className="p-2.5 text-center w-[100px] min-w-[100px] bg-slate-950 border-b border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)] sticky left-[670px] z-50 text-slate-400 font-bold uppercase">
                DOA
              </th>

              {/* Expanded Month Columns (160px width) */}
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-cyan-400 font-bold uppercase">APR</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-emerald-400 font-bold uppercase">MAY</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-purple-400 font-bold uppercase">JUN</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-blue-400 font-bold uppercase">JUL</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-amber-400 font-bold uppercase">AUG</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-rose-400 font-bold uppercase">SEPT</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-cyan-300 font-bold uppercase">OCT</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-emerald-300 font-bold uppercase">NOV</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-purple-300 font-bold uppercase">DEC</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-blue-300 font-bold uppercase">JAN</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-amber-300 font-bold uppercase">FEB</th>
              <th className="p-2.5 text-center w-[160px] min-w-[160px] bg-slate-950 border-b border-r border-slate-800 text-rose-300 font-bold uppercase">MAR</th>
              <th className="p-2.5 text-center w-[60px] min-w-[60px] bg-slate-950 border-b border-slate-800 text-slate-400 font-bold uppercase">Action</th>
            </tr>
          </thead>
          <tbody className="bg-slate-900">
            {filtered.map(doc => (
              <tr key={doc.srNo} className="hover:bg-slate-800/60 transition group">
                {/* 1. SrNo (Frozen) */}
                <td className="p-2 text-center text-slate-400 font-mono border-b border-r border-slate-800/80 sticky left-0 bg-slate-900 group-hover:bg-slate-800 z-20 w-[50px] min-w-[50px]">
                  {doc.srNo}
                </td>

                {/* 2. Doctor Name (Frozen) */}
                <td className="p-1 border-b border-r border-slate-800/80 sticky left-[50px] bg-slate-900 group-hover:bg-slate-800 z-20 w-[200px] min-w-[200px]">
                  <input
                    type="text"
                    value={doc.doctorName}
                    onChange={e => handleFieldChange(doc.srNo, 'doctorName', e.target.value)}
                    className="w-full py-1.5 px-2 bg-slate-950 rounded-lg font-bold text-white border border-slate-800 focus:border-cyan-500 focus:outline-none text-xs"
                  />
                </td>

                {/* 3. Activity Type (Frozen) */}
                <td className="p-1 border-b border-r border-slate-800/80 sticky left-[250px] bg-slate-900 group-hover:bg-slate-800 z-20 w-[140px] min-w-[140px]">
                  <input
                    type="text"
                    value={doc.activityType}
                    onChange={e => handleFieldChange(doc.srNo, 'activityType', e.target.value)}
                    placeholder="-"
                    className="w-full py-1.5 px-2 bg-slate-950 rounded-lg text-amber-400 border border-slate-800 focus:border-cyan-500 focus:outline-none text-xs font-semibold"
                  />
                </td>

                {/* 4. Speciality (Frozen) */}
                <td className="p-1 border-b border-r border-slate-800/80 sticky left-[390px] bg-slate-900 group-hover:bg-slate-800 z-20 w-[180px] min-w-[180px]">
                  <input
                    type="text"
                    value={doc.speciality}
                    onChange={e => handleFieldChange(doc.srNo, 'speciality', e.target.value)}
                    placeholder="-"
                    className="w-full py-1.5 px-2 bg-slate-950 rounded-lg text-slate-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-xs font-medium"
                  />
                </td>

                {/* 5. DOB (Frozen) */}
                <td className="p-1 border-b border-r border-slate-800/80 sticky left-[570px] bg-slate-900 group-hover:bg-slate-800 z-20 w-[100px] min-w-[100px]">
                  <input
                    type="text"
                    value={doc.dob}
                    onChange={e => handleFieldChange(doc.srNo, 'dob', e.target.value)}
                    placeholder="DD/MM/YYYY"
                    className="w-full py-1.5 px-1 bg-slate-950 rounded-lg font-mono text-slate-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-center text-xs"
                  />
                </td>

                {/* 6. DOA (Frozen with Cyan Divider) */}
                <td className="p-1 border-b border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)] sticky left-[670px] bg-slate-900 group-hover:bg-slate-800 z-20 w-[100px] min-w-[100px]">
                  <input
                    type="text"
                    value={doc.doa}
                    onChange={e => handleFieldChange(doc.srNo, 'doa', e.target.value)}
                    placeholder="DD/MM/YYYY"
                    className="w-full py-1.5 px-1 bg-slate-950 rounded-lg font-mono text-slate-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-center text-xs font-bold"
                  />
                </td>

                {/* 12 Months (Wide inputs) */}
                {['apr', 'may', 'jun', 'jul', 'aug', 'sept', 'oct', 'nov', 'dec', 'jan', 'feb', 'mar'].map(monthKey => (
                  <td key={monthKey} className="p-1.5 w-[160px] min-w-[160px] border-b border-r border-slate-800/50">
                    <input
                      type="text"
                      value={(doc as any)[monthKey]}
                      onChange={e => handleFieldChange(doc.srNo, monthKey as any, e.target.value)}
                      placeholder="-"
                      className="w-full py-1.5 px-2 bg-slate-950 rounded-lg font-mono text-slate-100 border border-slate-800 focus:border-cyan-400 focus:bg-slate-900 focus:outline-none text-center text-xs font-semibold"
                    />
                  </td>
                ))}

                {/* Action */}
                <td className="p-2 text-center border-b border-slate-800/80 w-[60px] min-w-[60px]">
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
with open('src/components/review/MslSheet.tsx', 'w', encoding='utf-8') as f:
    f.write(msl_content)
print("Updated MslSheet.tsx!")

# 3. Update MainHub.tsx version banner to SYSTEM V55.0 LIVE
hub_path = 'src/components/MainHub.tsx'
with open(hub_path, 'r', encoding='utf-8') as f:
    hub_text = f.read()

hub_text = hub_text.replace("SYSTEM V52.0 LIVE", "SYSTEM V55.0 LIVE (MSL FREEZE & EXTENDED INPUTS)")
with open(hub_path, 'w', encoding='utf-8') as f:
    f.write(hub_text)
print("Updated MainHub.tsx to V55.0!")

# 4. Update ReviewFormatWorkspace.tsx banner to V55.0
rf_path = 'src/components/ReviewFormatWorkspace.tsx'
with open(rf_path, 'r', encoding='utf-8') as f:
    rf_text = f.read()

rf_text = rf_text.replace("DIOS REVIEW HUB (14 MODULAR SHEETS)", "DIOS V55.0 REVIEW HUB (MSL FREEZE ACTIVE)")
with open(rf_path, 'w', encoding='utf-8') as f:
    f.write(rf_text)
print("Updated ReviewFormatWorkspace.tsx to V55.0!")

print("🎉 ALL FILES SUCCESSFULLY UPDATED TO V55.0!")
