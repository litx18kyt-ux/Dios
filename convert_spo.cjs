const fs = require('fs');
const XLSX = require('xlsx');

const inputFile = '/workspaces/Dios/csv_output/SPO_StockistWise_Aug-2026.xls';

if (fs.existsSync(inputFile)) {
  const buf = fs.readFileSync(inputFile);
  const wb = XLSX.read(buf, { type: 'buffer' });
  const sheet = wb.Sheets[wb.SheetNames[0]];
  const csvData = XLSX.utils.sheet_to_csv(sheet);
  
  console.log('\n========================================================');
  console.log('🎉 SPO STOCKIST WISE EXCEL READ SUCCESSFULLY!');
  console.log('========================================================\n');
  const lines = csvData.trim().split('\n');
  lines.forEach((line, idx) => {
    if (line.includes('Total') || idx < 10) {
      console.log(`[Line ${idx + 1}] ${line}`);
    }
  });
}
