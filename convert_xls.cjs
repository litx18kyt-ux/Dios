const fs = require('fs');
const XLSX = require('xlsx');

const inputFile = '/workspaces/Dios/csv_output/DCR_DateWise_Aug-2026.xls';
const outputFile = '/workspaces/Dios/csv_output/2_MONTH FW PROGRESS.csv';

if (fs.existsSync(inputFile)) {
  const buf = fs.readFileSync(inputFile);
  const wb = XLSX.read(buf, { type: 'buffer' });
  const sheet = wb.Sheets[wb.SheetNames[0]];
  const csvData = XLSX.utils.sheet_to_csv(sheet);
  
  fs.writeFileSync(outputFile, csvData, 'utf-8');
  console.log('\n========================================================');
  console.log('🎉 2_MONTH FW PROGRESS.csv CREATED SUCCESSFULLY!');
  console.log('========================================================\n');
  const lines = csvData.trim().split('\n');
  console.log('Total Rows:', lines.length);
  console.log('\n--- First 15 Rows Preview ---');
  console.log(lines.slice(0, 15).join('\n'));
} else {
  console.error('File not found:', inputFile);
}
