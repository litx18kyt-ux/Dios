import React from 'react';
import { HeartPulse } from 'lucide-react';

const CAMPAIGN_ROWS = [
  { sn: 1, brand: 'VINTEL', doctor: 'PRIYANKA MINOCHA', spec: 'MD MBBS, NEUROLOGY', date: '10TH OF EVERY MONTH', doneOn: 'na' },
  { sn: 2, brand: 'VINTEL', doctor: 'Mona dingra', spec: 'DM ENDOCRINOLOGIST', date: '10TH OF EVERY MONTH', doneOn: '10-Jul' },
  { sn: 3, brand: 'VINTEL', doctor: 'UDAY BHOMIK', spec: 'MCH NEUROSURGERY', date: '10TH OF EVERY MONTH', doneOn: '17-Jul' },
  { sn: 4, brand: 'VALROS', doctor: 'DEEPAK AAMETHA', spec: 'DM CARD.', date: '20TH OF EVERY MONTH', doneOn: '22-Jul' },
  { sn: 5, brand: 'VALROS', doctor: 'MUKESH SHARMA', spec: 'DM CARD.', date: '20TH OF EVERY MONTH', doneOn: '22-Jul' },
  { sn: 6, brand: 'VALROS', doctor: 'CPPUROHIT', spec: 'DM CARD.', date: '20TH OF EVERY MONTH', doneOn: '22-Jul' },
  { sn: 7, brand: 'VALROS', doctor: 'RAMESH PATEL', spec: 'DM CARD.', date: '20TH OF EVERY MONTH', doneOn: '22-Jul' },
  { sn: 8, brand: 'VALROS', doctor: 'Sanjay Gandhi', spec: 'MS, MCH, CARDIOLOGY', date: '20TH OF EVERY MONTH', doneOn: '' },
  { sn: 9, brand: 'VALROS', doctor: 'RAVIRAJ SINGH AHADA', spec: 'DM CARD.', date: '20TH OF EVERY MONTH', doneOn: '22-Jul' },
  { sn: 10, brand: 'VALROS', doctor: 'Dilip jain', spec: 'DM CARD.', date: '20TH OF EVERY MONTH', doneOn: '23-Jul' },
];

export const WcfyhSheet: React.FC = () => {
  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-5 shadow-xl">
      <div className="flex items-center justify-between mb-4 pb-3 border-b border-slate-800">
        <div className="flex items-center gap-2">
          <span className="p-2 bg-rose-500/20 text-rose-400 rounded-lg"><HeartPulse size={18} /></span>
          <h2 className="text-base font-bold text-white">7. WE CARE FOR YOUR HEALTH (WCFYH) CAMPAIGN</h2>
        </div>
      </div>
      <div className="overflow-x-auto">
        <table className="w-full text-left text-xs border-collapse">
          <thead>
            <tr className="bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800">
              <th className="p-2.5 w-10 text-center">S.N.</th>
              <th className="p-2.5">Brand</th>
              <th className="p-2.5">Doctor Name</th>
              <th className="p-2.5">Speciality</th>
              <th className="p-2.5">Schedule</th>
              <th className="p-2.5 text-center text-cyan-400">Done On</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {CAMPAIGN_ROWS.map(row => (
              <tr key={row.sn} className="hover:bg-slate-800/40 transition">
                <td className="p-2.5 text-center text-slate-500 font-mono">{row.sn}</td>
                <td className="p-2.5 font-bold text-cyan-400">{row.brand}</td>
                <td className="p-2.5 font-semibold text-white">{row.doctor}</td>
                <td className="p-2.5 text-slate-300">{row.spec}</td>
                <td className="p-2.5 text-slate-400">{row.date}</td>
                <td className="p-2.5 text-center font-mono font-bold text-emerald-400">{row.doneOn || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};
