const fs = require('fs');
const XLSX = require('xlsx');

const xlsPath = '/workspaces/Dios/csv_output/DCR_DateWise_Aug-2026.xls';
const csvPath = '/workspaces/Dios/csv_output/DCR_DateWise_Aug-2026.csv';
const txtPath = '/workspaces/Dios/csv_output/dcr_august_full.txt';

if (fs.existsSync(xlsPath)) {
  const buf = fs.readFileSync(xlsPath);
  const wb = XLSX.read(buf, { type: 'buffer' });
  const sheet = wb.Sheets[wb.SheetNames[0]];
  
  // 1. Full raw CSV
  const rawCsv = XLSX.utils.sheet_to_csv(sheet);
  fs.writeFileSync(csvPath, rawCsv, 'utf-8');
  fs.writeFileSync(txtPath, rawCsv, 'utf-8');

  console.log('========================================================');
  console.log('🎉 SUCCESS! CSV & TXT CREATED:');
  console.log('📁 ' + csvPath);
  console.log('📁 ' + txtPath);
  console.log('========================================================\n');

  // Print all rows cleanly
  const lines = rawCsv.split('\n').filter(l => l.trim().length > 0);
  console.log(`Total Rows: ${lines.length}\n`);
  lines.forEach((line, idx) => {
    console.log(`[Row ${idx + 1}] ${line}`);
  });
} else {
  console.error('File not found:', xlsPath);
}
