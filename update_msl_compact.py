import os, json, csv

# 1. Load CSV Doctors
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

print(f"Loaded {len(doctors)} doctors.")

# 2. Generate MslSheet.tsx with dynamic column toggles and compact dimensions
msl_code = '''import React, { useState } from 'react';
import { Calendar, Search, Save, Download, Check, Plus, Trash2, Eye, EyeOff, Sparkles, Filter } from 'lucide-react';
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

  // Column Visibility Toggles (Can be hidden to save space)
  const [showActivity, setShowActivity] = useState(true);
  const [showSpeciality, setShowSpeciality] = useState(true);
  const [showDob, setShowDob] = useState(true);
  const [showDoa, setShowDoa] = useState(true);

  const [savedSuccess, setSavedSuccess] = useState(false);

  // Compact Column Widths (in pixels)
  const W_SR = 38;
  const W_DOC = 145;
  const W_ACT = 90;
  const W_SPEC = 110;
  const W_DOB = 75;
  const W_DOA = 75;

  // Calculate Dynamic Sticky Offsets
  let currentOffset = W_SR + W_DOC;
  const offsetAct = currentOffset;
  if (showActivity) currentOffset += W_ACT;
  const offsetSpec = currentOffset;
  if (showSpeciality) currentOffset += W_SPEC;
  const offsetDob = currentOffset;
  if (showDob) currentOffset += W_DOB;
  const offsetDoa = currentOffset;

  // Determine which column is the last visible left column (gets the cyan divider)
  let lastLeftCol = 'doa';
  if (!showDoa) {
    if (showDob) lastLeftCol = 'dob';
    else if (showSpeciality) lastLeftCol = 'speciality';
    else if (showActivity) lastLeftCol = 'activity';
    else lastLeftCol = 'doctor';
  }

  const isAllHidden = !showActivity && !showSpeciality && !showDob && !showDoa;

  const toggleFocusMode = () => {
    if (isAllHidden) {
      setShowActivity(true);
      setShowSpeciality(true);
      setShowDob(true);
      setShowDoa(true);
    } else {
      setShowActivity(false);
      setShowSpeciality(false);
      setShowDob(false);
      setShowDoa(false);
    }
  };

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
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 md:p-5 shadow-xl space-y-4">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <span className="p-2 bg-cyan-500/20 text-cyan-400 rounded-lg"><Calendar size={18} /></span>
          <div>
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              14. MSL (Master Specialty List &amp; Visit Dates)
              <span className="text-[10px] bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 px-2 py-0.5 rounded-full font-mono font-bold">
                SYSTEM V56.0 • COMPACT &amp; HIDE TOGGLES
              </span>
            </h2>
            <p className="text-xs text-slate-400">Total {doctors.length} Doctors • Compact Left Columns with Custom Column Hiding</p>
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <div className="relative w-full sm:w-52">
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

      {/* COLUMN HIDE / SHOW CONTROLS BAR (IPAD FRIENDLY) */}
      <div className="flex flex-wrap items-center justify-between gap-2 p-2.5 bg-slate-950 rounded-xl border border-slate-800 text-xs">
        <div className="flex flex-wrap items-center gap-1.5">
          <span className="text-[11px] font-bold text-slate-400 uppercase mr-1 flex items-center gap-1">
            <Filter size={13} className="text-cyan-400" /> Show/Hide Columns:
          </span>

          <button
            onClick={() => setShowActivity(!showActivity)}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold border transition cursor-pointer flex items-center gap-1 ${
              showActivity 
                ? 'bg-amber-500/20 text-amber-300 border-amber-500/40' 
                : 'bg-slate-900 text-slate-500 border-slate-800 hover:text-slate-300'
            }`}
          >
            {showActivity ? <Eye size={12} /> : <EyeOff size={12} />} Activity
          </button>

          <button
            onClick={() => setShowSpeciality(!showSpeciality)}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold border transition cursor-pointer flex items-center gap-1 ${
              showSpeciality 
                ? 'bg-blue-500/20 text-blue-300 border-blue-500/40' 
                : 'bg-slate-900 text-slate-500 border-slate-800 hover:text-slate-300'
            }`}
          >
            {showSpeciality ? <Eye size={12} /> : <EyeOff size={12} />} Speciality
          </button>

          <button
            onClick={() => setShowDob(!showDob)}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold border transition cursor-pointer flex items-center gap-1 ${
              showDob 
                ? 'bg-purple-500/20 text-purple-300 border-purple-500/40' 
                : 'bg-slate-900 text-slate-500 border-slate-800 hover:text-slate-300'
            }`}
          >
            {showDob ? <Eye size={12} /> : <EyeOff size={12} />} DOB
          </button>

          <button
            onClick={() => setShowDoa(!showDoa)}
            className={`px-2.5 py-1 rounded-lg text-xs font-semibold border transition cursor-pointer flex items-center gap-1 ${
              showDoa 
                ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40' 
                : 'bg-slate-900 text-slate-500 border-slate-800 hover:text-slate-300'
            }`}
          >
            {showDoa ? <Eye size={12} /> : <EyeOff size={12} />} DOA
          </button>
        </div>

        {/* ⚡ Focus Mode Toggle (Hide all extra details at once) */}
        <button
          onClick={toggleFocusMode}
          className={`px-3 py-1 rounded-lg text-xs font-bold border transition cursor-pointer flex items-center gap-1.5 shadow-sm ${
            isAllHidden 
              ? 'bg-gradient-to-r from-cyan-600 to-blue-600 text-white border-cyan-400 shadow-cyan-950' 
              : 'bg-slate-900 text-amber-300 border-amber-500/40 hover:bg-amber-950/40'
          }`}
        >
          <Sparkles size={13} className="text-yellow-300" />
          {isAllHidden ? 'Show All Columns' : '⚡ Focus Mode (Doctor + Months Only)'}
        </button>
      </div>

      {/* TABLE WITH DYNAMIC STICKY FROZEN PANES */}
      <div className="overflow-x-auto max-h-[640px] border border-slate-800 rounded-2xl relative shadow-2xl">
        <table className="w-full text-left text-xs border-separate border-spacing-0">
          <thead className="sticky top-0 z-40 bg-slate-950">
            <tr>
              {/* 1. SrNo */}
              <th 
                style={{ width: `${W_SR}px`, minWidth: `${W_SR}px`, left: 0 }}
                className="p-2 text-center bg-slate-950 border-b border-r border-slate-800 sticky z-50 text-slate-400 font-bold uppercase"
              >
                #
              </th>

              {/* 2. Doctor Name */}
              <th 
                style={{ width: `${W_DOC}px`, minWidth: `${W_DOC}px`, left: `${W_SR}px` }}
                className={`p-2 bg-slate-950 border-b border-slate-800 sticky z-50 text-slate-400 font-bold uppercase ${
                  lastLeftCol === 'doctor' ? 'border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)]' : 'border-r'
                }`}
              >
                Doctor Name
              </th>

              {/* 3. Activity Type (Toggleable) */}
              {showActivity && (
                <th 
                  style={{ width: `${W_ACT}px`, minWidth: `${W_ACT}px`, left: `${offsetAct}px` }}
                  className={`p-2 bg-slate-950 border-b border-slate-800 sticky z-50 text-amber-400 font-bold uppercase ${
                    lastLeftCol === 'activity' ? 'border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)]' : 'border-r'
                  }`}
                >
                  Activity
                </th>
              )}

              {/* 4. Speciality (Toggleable) */}
              {showSpeciality && (
                <th 
                  style={{ width: `${W_SPEC}px`, minWidth: `${W_SPEC}px`, left: `${offsetSpec}px` }}
                  className={`p-2 bg-slate-950 border-b border-slate-800 sticky z-50 text-blue-300 font-bold uppercase ${
                    lastLeftCol === 'speciality' ? 'border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)]' : 'border-r'
                  }`}
                >
                  Speciality
                </th>
              )}

              {/* 5. DOB (Toggleable) */}
              {showDob && (
                <th 
                  style={{ width: `${W_DOB}px`, minWidth: `${W_DOB}px`, left: `${offsetDob}px` }}
                  className={`p-2 text-center bg-slate-950 border-b border-slate-800 sticky z-50 text-purple-300 font-bold uppercase ${
                    lastLeftCol === 'dob' ? 'border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)]' : 'border-r'
                  }`}
                >
                  DOB
                </th>
              )}

              {/* 6. DOA (Toggleable with Divider) */}
              {showDoa && (
                <th 
                  style={{ width: `${W_DOA}px`, minWidth: `${W_DOA}px`, left: `${offsetDoa}px` }}
                  className="p-2 text-center bg-slate-950 border-b border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)] sticky z-50 text-emerald-400 font-bold uppercase"
                >
                  DOA
                </th>
              )}

              {/* 12 Expanded Month Columns (160px) */}
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
              <th className="p-2.5 text-center w-[50px] min-w-[50px] bg-slate-950 border-b border-slate-800 text-slate-400 font-bold uppercase">Action</th>
            </tr>
          </thead>
          <tbody className="bg-slate-900">
            {filtered.map(doc => (
              <tr key={doc.srNo} className="hover:bg-slate-800/60 transition group">
                {/* 1. SrNo */}
                <td 
                  style={{ width: `${W_SR}px`, minWidth: `${W_SR}px`, left: 0 }}
                  className="p-1.5 text-center text-slate-400 font-mono border-b border-r border-slate-800/80 sticky bg-slate-900 group-hover:bg-slate-800 z-20 text-xs"
                >
                  {doc.srNo}
                </td>

                {/* 2. Doctor Name */}
                <td 
                  style={{ width: `${W_DOC}px`, minWidth: `${W_DOC}px`, left: `${W_SR}px` }}
                  className={`p-1 border-b border-slate-800/80 sticky bg-slate-900 group-hover:bg-slate-800 z-20 ${
                    lastLeftCol === 'doctor' ? 'border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)]' : 'border-r'
                  }`}
                >
                  <input
                    type="text"
                    value={doc.doctorName}
                    onChange={e => handleFieldChange(doc.srNo, 'doctorName', e.target.value)}
                    className="w-full py-1 px-1.5 bg-slate-950 rounded-md font-bold text-white border border-slate-800 focus:border-cyan-500 focus:outline-none text-[11px]"
                  />
                </td>

                {/* 3. Activity Type (Toggleable) */}
                {showActivity && (
                  <td 
                    style={{ width: `${W_ACT}px`, minWidth: `${W_ACT}px`, left: `${offsetAct}px` }}
                    className={`p-1 border-b border-slate-800/80 sticky bg-slate-900 group-hover:bg-slate-800 z-20 ${
                      lastLeftCol === 'activity' ? 'border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)]' : 'border-r'
                    }`}
                  >
                    <input
                      type="text"
                      value={doc.activityType}
                      onChange={e => handleFieldChange(doc.srNo, 'activityType', e.target.value)}
                      placeholder="-"
                      className="w-full py-1 px-1.5 bg-slate-950 rounded-md text-amber-400 border border-slate-800 focus:border-cyan-500 focus:outline-none text-[10px] font-semibold"
                    />
                  </td>
                )}

                {/* 4. Speciality (Toggleable) */}
                {showSpeciality && (
                  <td 
                    style={{ width: `${W_SPEC}px`, minWidth: `${W_SPEC}px`, left: `${offsetSpec}px` }}
                    className={`p-1 border-b border-slate-800/80 sticky bg-slate-900 group-hover:bg-slate-800 z-20 ${
                      lastLeftCol === 'speciality' ? 'border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)]' : 'border-r'
                    }`}
                  >
                    <input
                      type="text"
                      value={doc.speciality}
                      onChange={e => handleFieldChange(doc.srNo, 'speciality', e.target.value)}
                      placeholder="-"
                      className="w-full py-1 px-1.5 bg-slate-950 rounded-md text-slate-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-[10px]"
                    />
                  </td>
                )}

                {/* 5. DOB (Toggleable) */}
                {showDob && (
                  <td 
                    style={{ width: `${W_DOB}px`, minWidth: `${W_DOB}px`, left: `${offsetDob}px` }}
                    className={`p-1 border-b border-slate-800/80 sticky bg-slate-900 group-hover:bg-slate-800 z-20 ${
                      lastLeftCol === 'dob' ? 'border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)]' : 'border-r'
                    }`}
                  >
                    <input
                      type="text"
                      value={doc.dob}
                      onChange={e => handleFieldChange(doc.srNo, 'dob', e.target.value)}
                      placeholder="DD/MM/YYYY"
                      className="w-full py-1 px-1 bg-slate-950 rounded-md font-mono text-slate-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-center text-[10px]"
                    />
                  </td>
                )}

                {/* 6. DOA (Toggleable with Divider) */}
                {showDoa && (
                  <td 
                    style={{ width: `${W_DOA}px`, minWidth: `${W_DOA}px`, left: `${offsetDoa}px` }}
                    className="p-1 border-b border-r-4 border-cyan-500 shadow-[4px_0_12px_rgba(0,0,0,0.6)] sticky bg-slate-900 group-hover:bg-slate-800 z-20"
                  >
                    <input
                      type="text"
                      value={doc.doa}
                      onChange={e => handleFieldChange(doc.srNo, 'doa', e.target.value)}
                      placeholder="DD/MM/YYYY"
                      className="w-full py-1 px-1 bg-slate-950 rounded-md font-mono text-slate-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-center text-[10px] font-bold"
                    />
                  </td>
                )}

                {/* 12 Months (160px Wide Inputs) */}
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
                <td className="p-1 text-center border-b border-slate-800/80 w-[50px] min-w-[50px]">
                  <button
                    type="button"
                    onClick={() => handleDeleteDoctor(doc.srNo)}
                    className="p-1.5 text-slate-500 hover:text-rose-400 rounded-lg transition cursor-pointer"
                  >
                    <Trash2 size={14} />
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
    f.write(msl_code)
print("Updated MslSheet.tsx with Compact Dimensions & Column Toggles!")

# 3. Update MainHub.tsx version banner to SYSTEM V56.0 LIVE
hub_path = 'src/components/MainHub.tsx'
with open(hub_path, 'r', encoding='utf-8') as f:
    hub_text = f.read()

hub_text = hub_text.replace("SYSTEM V55.0 LIVE (MSL FREEZE & EXTENDED INPUTS)", "SYSTEM V56.0 LIVE (COMPACT & COLUMN TOGGLES)")
hub_text = hub_text.replace("SYSTEM V52.0 LIVE", "SYSTEM V56.0 LIVE (COMPACT & COLUMN TOGGLES)")
with open(hub_path, 'w', encoding='utf-8') as f:
    f.write(hub_text)
print("Updated MainHub.tsx to V56.0!")

print("🎉 ALL FILES SUCCESSFULLY UPDATED TO V56.0!")
