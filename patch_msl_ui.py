import os

path = 'src/components/review/MslSheet.tsx'
with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

split_marker = '  return ('
if split_marker in text:
    header_part = text.split(split_marker)[0]
else:
    print("Error: Could not find return statement in MslSheet.tsx")
    exit(1)

new_jsx = '''  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl space-y-4">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <span className="p-2 bg-cyan-500/20 text-cyan-400 rounded-lg"><Calendar size={18} /></span>
          <div>
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              14. MSL (Master Specialty List &amp; Visit Dates)
              <span className="text-[10px] bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 px-2 py-0.5 rounded-full font-mono font-bold">
                Frozen Till DOA
              </span>
            </h2>
            <p className="text-xs text-slate-400">DOA Tak Columns Frozen • Extended Month Inputs (155px)</p>
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

      {/* TABLE WITH FROZEN PANES UP TO DOA */}
      <div className="overflow-x-auto max-h-[620px] border border-slate-800 rounded-2xl relative shadow-2xl">
        <table className="w-full text-left text-xs border-collapse">
          <thead className="sticky top-0 bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800 z-30">
            <tr>
              <th className="p-2.5 text-center w-[48px] min-w-[48px] bg-slate-950 border-r border-slate-800 sticky left-0 z-40">
                SrNo
              </th>
              <th className="p-2.5 w-[190px] min-w-[190px] bg-slate-950 border-r border-slate-800 sticky left-[48px] z-40">
                Doctor Name
              </th>
              <th className="p-2.5 w-[130px] min-w-[130px] bg-slate-950 border-r border-slate-800 sticky left-[238px] z-40">
                Activity Type
              </th>
              <th className="p-2.5 w-[160px] min-w-[160px] bg-slate-950 border-r border-slate-800 sticky left-[368px] z-40">
                Speciality
              </th>
              <th className="p-2.5 text-center w-[90px] min-w-[90px] bg-slate-950 border-r border-slate-800 sticky left-[528px] z-40">
                DOB
              </th>
              <th className="p-2.5 text-center w-[90px] min-w-[90px] bg-slate-950 border-r-2 border-cyan-500/70 shadow-lg shadow-cyan-950/50 sticky left-[618px] z-40">
                DOA
              </th>

              <th className="p-2.5 text-center min-w-[155px] text-cyan-400 bg-slate-950 border-r border-slate-800/60">APR</th>
              <th className="p-2.5 text-center min-w-[155px] text-emerald-400 bg-slate-950 border-r border-slate-800/60">MAY</th>
              <th className="p-2.5 text-center min-w-[155px] text-purple-400 bg-slate-950 border-r border-slate-800/60">JUN</th>
              <th className="p-2.5 text-center min-w-[155px] text-blue-400 bg-slate-950 border-r border-slate-800/60">JUL</th>
              <th className="p-2.5 text-center min-w-[155px] text-amber-400 bg-slate-950 border-r border-slate-800/60">AUG</th>
              <th className="p-2.5 text-center min-w-[155px] text-rose-400 bg-slate-950 border-r border-slate-800/60">SEPT</th>
              <th className="p-2.5 text-center min-w-[155px] text-cyan-300 bg-slate-950 border-r border-slate-800/60">OCT</th>
              <th className="p-2.5 text-center min-w-[155px] text-emerald-300 bg-slate-950 border-r border-slate-800/60">NOV</th>
              <th className="p-2.5 text-center min-w-[155px] text-purple-300 bg-slate-950 border-r border-slate-800/60">DEC</th>
              <th className="p-2.5 text-center min-w-[155px] text-blue-300 bg-slate-950 border-r border-slate-800/60">JAN</th>
              <th className="p-2.5 text-center min-w-[155px] text-amber-300 bg-slate-950 border-r border-slate-800/60">FEB</th>
              <th className="p-2.5 text-center min-w-[155px] text-rose-300 bg-slate-950 border-r border-slate-800/60">MAR</th>
              <th className="p-2.5 text-center w-14 bg-slate-950">Action</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {filtered.map(doc => (
              <tr key={doc.srNo} className="hover:bg-slate-800/40 transition">
                <td className="p-2 text-center text-slate-500 font-mono border-r border-slate-800/60 sticky left-0 bg-slate-900 z-20 w-[48px] min-w-[48px]">
                  {doc.srNo}
                </td>

                <td className="p-1 border-r border-slate-800/60 sticky left-[48px] bg-slate-900 z-20 w-[190px] min-w-[190px]">
                  <input
                    type="text"
                    value={doc.doctorName}
                    onChange={e => handleFieldChange(doc.srNo, 'doctorName', e.target.value)}
                    className="w-full py-1.5 px-2 bg-slate-950 rounded-lg font-semibold text-white border border-slate-800 focus:border-cyan-500 focus:outline-none text-xs"
                  />
                </td>

                <td className="p-1 border-r border-slate-800/60 sticky left-[238px] bg-slate-900 z-20 w-[130px] min-w-[130px]">
                  <input
                    type="text"
                    value={doc.activityType}
                    onChange={e => handleFieldChange(doc.srNo, 'activityType', e.target.value)}
                    placeholder="-"
                    className="w-full py-1.5 px-2 bg-slate-950 rounded-lg text-amber-400 border border-slate-800 focus:border-cyan-500 focus:outline-none text-xs font-medium"
                  />
                </td>

                <td className="p-1 border-r border-slate-800/60 sticky left-[368px] bg-slate-900 z-20 w-[160px] min-w-[160px]">
                  <input
                    type="text"
                    value={doc.speciality}
                    onChange={e => handleFieldChange(doc.srNo, 'speciality', e.target.value)}
                    placeholder="-"
                    className="w-full py-1.5 px-2 bg-slate-950 rounded-lg text-slate-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-xs"
                  />
                </td>

                <td className="p-1 border-r border-slate-800/60 sticky left-[528px] bg-slate-900 z-20 w-[90px] min-w-[90px]">
                  <input
                    type="text"
                    value={doc.dob}
                    onChange={e => handleFieldChange(doc.srNo, 'dob', e.target.value)}
                    placeholder="DD/MM/YYYY"
                    className="w-full py-1.5 px-1 bg-slate-950 rounded-lg font-mono text-slate-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-center text-xs"
                  />
                </td>

                <td className="p-1 border-r-2 border-cyan-500/70 shadow-lg shadow-cyan-950/50 sticky left-[618px] bg-slate-900 z-20 w-[90px] min-w-[90px]">
                  <input
                    type="text"
                    value={doc.doa}
                    onChange={e => handleFieldChange(doc.srNo, 'doa', e.target.value)}
                    placeholder="DD/MM/YYYY"
                    className="w-full py-1.5 px-1 bg-slate-950 rounded-lg font-mono text-slate-300 border border-slate-800 focus:border-cyan-500 focus:outline-none text-center text-xs"
                  />
                </td>

                {['apr', 'may', 'jun', 'jul', 'aug', 'sept', 'oct', 'nov', 'dec', 'jan', 'feb', 'mar'].map(monthKey => (
                  <td key={monthKey} className="p-1.5 min-w-[155px] border-r border-slate-800/40">
                    <input
                      type="text"
                      value={(doc as any)[monthKey]}
                      onChange={e => handleFieldChange(doc.srNo, monthKey as any, e.target.value)}
                      placeholder="-"
                      className="w-full py-1.5 px-2 bg-slate-950 rounded-lg font-mono text-slate-100 border border-slate-800 focus:border-cyan-400 focus:bg-slate-900 focus:outline-none text-center text-xs font-semibold"
                    />
                  </td>
                ))}

                <td className="p-2 text-center w-14">
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

with open(path, 'w', encoding='utf-8') as f:
    f.write(header_part + new_jsx)

print("🎉 Successfully patched MslSheet.tsx!")
