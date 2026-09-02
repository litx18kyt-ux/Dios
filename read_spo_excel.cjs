const fs = require('fs');
const XLSX = require('xlsx');

const xlsPath = '/workspaces/Dios/csv_output/SPO_StockistWise_Aug-2026.xls';
const outTxt = '/workspaces/Dios/spo_excel_columns.txt';

if (fs.existsSync(xlsPath)) {
  const buf = fs.readFileSync(xlsPath);
  const wb = XLSX.read(buf, { type: 'buffer' });
  const sheet = wb.Sheets[wb.SheetNames[0]];
  const csv = XLSX.utils.sheet_to_csv(sheet);
  
  fs.writeFileSync(outTxt, csv, 'utf-8');
  console.log('✅ Converted to txt: ' + outTxt);
  
  const lines = csv.split('\n').filter(l => l.trim().length > 0);
  console.log('Total Rows in File:', lines.length);
  console.log('\n--- First 10 Rows ---');
  console.log(lines.slice(0, 10).join('\n'));
} else {
  console.error('File not found:', xlsPath);
}
