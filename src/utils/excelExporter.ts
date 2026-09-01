import * as XLSX from 'xlsx-js-style';
import { AggregatedProduct } from '../parsers/common';

const MONTHS = ['APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NOVEMBER', 'DECEMBER', 'JANUARY', 'FEBRUARY', 'MARCH'];

// Styling Presets
const borderThin = {
  top: { style: 'thin', color: { rgb: 'D1D5DB' } },
  bottom: { style: 'thin', color: { rgb: 'D1D5DB' } },
  left: { style: 'thin', color: { rgb: 'D1D5DB' } },
  right: { style: 'thin', color: { rgb: 'D1D5DB' } }
};

const borderDoubleBottom = {
  top: { style: 'thin', color: { rgb: '000000' } },
  bottom: { style: 'double', color: { rgb: '000000' } },
  left: { style: 'thin', color: { rgb: '000000' } },
  right: { style: 'thin', color: { rgb: '000000' } }
};

const styleTitle = {
  font: { name: 'Calibri', sz: 16, bold: true, color: { rgb: 'FFFFFF' } },
  fill: { fgColor: { rgb: '0F172A' } }, // Dark Slate/Navy
  alignment: { horizontal: 'center', vertical: 'center' }
};

const styleSubTitle = {
  font: { name: 'Calibri', sz: 12, bold: true, color: { rgb: '38BDF8' } },
  fill: { fgColor: { rgb: '1E293B' } },
  alignment: { horizontal: 'center', vertical: 'center' }
};

const stylePartyHeader = {
  font: { name: 'Calibri', sz: 11, bold: true, color: { rgb: 'FFFFFF' } },
  fill: { fgColor: { rgb: '0369A1' } }, // Sky Blue Accent
  alignment: { horizontal: 'center', vertical: 'center' },
  border: borderThin
};

const styleSubColHeader = {
  font: { name: 'Calibri', sz: 10, bold: true, color: { rgb: '0F172A' } },
  fill: { fgColor: { rgb: 'E2E8F0' } }, // Soft Gray
  alignment: { horizontal: 'center', vertical: 'center' },
  border: borderThin
};

const styleCellLeft = {
  font: { name: 'Calibri', sz: 10, color: { rgb: '000000' } },
  alignment: { horizontal: 'left', vertical: 'center' },
  border: borderThin
};

const styleCellCenter = {
  font: { name: 'Calibri', sz: 10, color: { rgb: '000000' } },
  alignment: { horizontal: 'center', vertical: 'center' },
  border: borderThin
};

const styleCellRight = {
  font: { name: 'Calibri', sz: 10, color: { rgb: '000000' } },
  alignment: { horizontal: 'right', vertical: 'center' },
  border: borderThin
};

const styleCellHighlight = {
  font: { name: 'Calibri', sz: 10, bold: true, color: { rgb: '0369A1' } },
  fill: { fgColor: { rgb: 'F0F9FF' } },
  alignment: { horizontal: 'center', vertical: 'center' },
  border: borderThin
};

const styleTotalRow = {
  font: { name: 'Calibri', sz: 11, bold: true, color: { rgb: '0F172A' } },
  fill: { fgColor: { rgb: 'FEF08A' } }, // Soft Yellow Highlight
  alignment: { horizontal: 'center', vertical: 'center' },
  border: borderDoubleBottom
};

export function exportToExcel(
  products: AggregatedProduct[],
  selectedMonth: string,
  activeParties: string[],
  summary: { totalSalesUnits: number; totalClosingUnits: number; totalSalesValue: number; totalClosingValue: number }
) {
  // =============================================================
  // SHEET 1: UN.SALES PROG (HQ TOTAL 12 MONTHS)
  // =============================================================
  const totalCols = 3 + MONTHS.length * 3;
  const wsData: any[][] = [];

  const row1 = new Array(totalCols).fill({ v: '', s: styleTitle });
  row1[0] = { v: 'DIOS LIFESCIENCES PVT. LTD.', s: styleTitle };
  wsData.push(row1);

  const row2 = new Array(totalCols).fill({ v: '', s: styleSubTitle });
  row2[0] = { v: 'UNIT SALES PROGRESSION (HQ TOTAL) - 2026-27', s: styleSubTitle };
  wsData.push(row2);

  const row3: any[] = [
    { v: '', s: stylePartyHeader },
    { v: '', s: stylePartyHeader },
    { v: '', s: stylePartyHeader }
  ];
  MONTHS.forEach(m => {
    row3.push(
      { v: `${m} 2026`, s: stylePartyHeader },
      { v: '', s: stylePartyHeader },
      { v: '', s: stylePartyHeader }
    );
  });
  wsData.push(row3);

  const row4: any[] = [
    { v: 'S.N.', s: styleSubColHeader },
    { v: 'PRODUCT NAME', s: styleSubColHeader },
    { v: 'PTS (₹)', s: styleSubColHeader }
  ];
  MONTHS.forEach(() => {
    row4.push(
      { v: 'NET PRI', s: styleSubColHeader },
      { v: 'NET SEC', s: styleSubColHeader },
      { v: 'CLOSING', s: styleSubColHeader }
    );
  });
  wsData.push(row4);

  products.forEach(p => {
    const row: any[] = [
      { v: p.sn, s: styleCellCenter },
      { v: p.name, s: styleCellLeft },
      { v: p.pts.toFixed(2), s: styleCellRight }
    ];

    MONTHS.forEach(m => {
      if (m.toUpperCase() === selectedMonth.toUpperCase()) {
        row.push(
          { v: '-', s: styleCellCenter },
          { v: p.netSec > 0 ? p.netSec : 0, s: p.netSec > 0 ? styleCellHighlight : styleCellCenter },
          { v: p.closing > 0 ? p.closing : 0, s: p.closing > 0 ? styleCellHighlight : styleCellCenter }
        );
      } else {
        row.push(
          { v: '', s: styleCellCenter },
          { v: '', s: styleCellCenter },
          { v: '', s: styleCellCenter }
        );
      }
    });

    wsData.push(row);
  });

  const rowTotal: any[] = [
    { v: 'Σ', s: styleTotalRow },
    { v: 'GRAND TOTAL (UNITS)', s: { ...styleTotalRow, alignment: { horizontal: 'left', vertical: 'center' } } },
    { v: '-', s: styleTotalRow }
  ];
  MONTHS.forEach(m => {
    if (m.toUpperCase() === selectedMonth.toUpperCase()) {
      rowTotal.push(
        { v: '-', s: styleTotalRow },
        { v: summary.totalSalesUnits, s: styleTotalRow },
        { v: summary.totalClosingUnits, s: styleTotalRow }
      );
    } else {
      rowTotal.push(
        { v: '', s: styleTotalRow },
        { v: '', s: styleTotalRow },
        { v: '', s: styleTotalRow }
      );
    }
  });
  wsData.push(rowTotal);

  const rowValue: any[] = [
    { v: '₹', s: styleTotalRow },
    { v: 'TOTAL VALUE (RUPEES)', s: { ...styleTotalRow, alignment: { horizontal: 'left', vertical: 'center' } } },
    { v: '-', s: styleTotalRow }
  ];
  MONTHS.forEach(m => {
    if (m.toUpperCase() === selectedMonth.toUpperCase()) {
      rowValue.push(
        { v: '-', s: styleTotalRow },
        { v: `₹ ${Math.round(summary.totalSalesValue).toLocaleString()}`, s: styleTotalRow },
        { v: `₹ ${Math.round(summary.totalClosingValue).toLocaleString()}`, s: styleTotalRow }
      );
    } else {
      rowValue.push(
        { v: '', s: styleTotalRow },
        { v: '', s: styleTotalRow },
        { v: '', s: styleTotalRow }
      );
    }
  });
  wsData.push(rowValue);

  const ws = XLSX.utils.aoa_to_sheet(wsData);
  ws['!merges'] = [
    { s: { r: 0, c: 0 }, e: { r: 0, c: totalCols - 1 } },
    { s: { r: 1, c: 0 }, e: { r: 1, c: totalCols - 1 } },
  ];
  MONTHS.forEach((_, idx) => {
    const startCol = 3 + idx * 3;
    ws['!merges']!.push({
      s: { r: 2, c: startCol },
      e: { r: 2, c: startCol + 2 }
    });
  });

  const colWidths: any[] = [
    { wch: 6 },
    { wch: 35 },
    { wch: 12 },
  ];
  MONTHS.forEach(() => {
    colWidths.push({ wch: 10 }, { wch: 12 }, { wch: 14 });
  });
  ws['!cols'] = colWidths;
  ws['!rows'] = [{ hpt: 30 }, { hpt: 22 }, { hpt: 22 }, { hpt: 20 }];

  // =============================================================
  // SHEET 2: 2-TIER PARTY BREAKDOWN (SEC & CLOSING UNDER PARTY)
  // =============================================================
  const bData: any[][] = [];
  const bTotalCols = 3 + activeParties.length * 2 + 2;

  // Row 1: Party Headers (Merged across 2 columns: SEC & CLOSING)
  const bRow1: any[] = [
    { v: 'S.N.', s: styleSubColHeader },
    { v: 'PRODUCT NAME', s: styleSubColHeader },
    { v: 'PTS (₹)', s: styleSubColHeader }
  ];
  activeParties.forEach(p => {
    bRow1.push(
      { v: p.toUpperCase(), s: stylePartyHeader },
      { v: '', s: stylePartyHeader }
    );
  });
  bRow1.push(
    { v: 'TOTAL ALL PARTIES', s: { ...stylePartyHeader, fill: { fgColor: { rgb: '0F172A' } } } },
    { v: '', s: stylePartyHeader }
  );
  bData.push(bRow1);

  // Row 2: Sub-headers (SEC & CLOSING)
  const bRow2: any[] = [
    { v: '', s: styleSubColHeader },
    { v: '', s: styleSubColHeader },
    { v: '', s: styleSubColHeader }
  ];
  activeParties.forEach(() => {
    bRow2.push(
      { v: 'SEC', s: styleSubColHeader },
      { v: 'CLOSING', s: styleSubColHeader }
    );
  });
  bRow2.push(
    { v: 'TOTAL SEC', s: { ...styleSubColHeader, font: { bold: true, color: { rgb: '0369A1' } } } },
    { v: 'TOTAL CLOSING', s: { ...styleSubColHeader, font: { bold: true, color: { rgb: '0369A1' } } } }
  );
  bData.push(bRow2);

  // Data Rows: 73 Master Products
  products.forEach(p => {
    const row: any[] = [
      { v: p.sn, s: styleCellCenter },
      { v: p.name, s: styleCellLeft },
      { v: p.pts.toFixed(2), s: styleCellRight }
    ];

    activeParties.forEach(party => {
      const partySales = p.partyBreakdown[party]?.sales || 0;
      const partyClosing = p.partyBreakdown[party]?.closing || 0;
      row.push(
        { v: partySales, s: partySales > 0 ? styleCellHighlight : styleCellCenter },
        { v: partyClosing, s: partyClosing > 0 ? styleCellHighlight : styleCellCenter }
      );
    });

    row.push(
      { v: p.netSec, s: { ...styleCellHighlight, fill: { fgColor: { rgb: 'E0F2FE' } } } },
      { v: p.closing, s: { ...styleCellHighlight, fill: { fgColor: { rgb: 'E0F2FE' } } } }
    );

    bData.push(row);
  });

  // Grand Total Row (Units)
  const bRowTotal: any[] = [
    { v: 'Σ', s: styleTotalRow },
    { v: 'GRAND TOTAL (UNITS)', s: { ...styleTotalRow, alignment: { horizontal: 'left', vertical: 'center' } } },
    { v: '-', s: styleTotalRow }
  ];
  activeParties.forEach(party => {
    const partyTotalSales = products.reduce((acc, p) => acc + (p.partyBreakdown[party]?.sales || 0), 0);
    const partyTotalClosing = products.reduce((acc, p) => acc + (p.partyBreakdown[party]?.closing || 0), 0);
    bRowTotal.push(
      { v: partyTotalSales, s: styleTotalRow },
      { v: partyTotalClosing, s: styleTotalRow }
    );
  });
  bRowTotal.push(
    { v: summary.totalSalesUnits, s: { ...styleTotalRow, font: { bold: true, sz: 12 } } },
    { v: summary.totalClosingUnits, s: { ...styleTotalRow, font: { bold: true, sz: 12 } } }
  );
  bData.push(bRowTotal);

  // Grand Total Row (Value in ₹)
  const bRowValue: any[] = [
    { v: '₹', s: styleTotalRow },
    { v: 'TOTAL VALUE (RUPEES)', s: { ...styleTotalRow, alignment: { horizontal: 'left', vertical: 'center' } } },
    { v: '-', s: styleTotalRow }
  ];
  activeParties.forEach(party => {
    const partyValSales = products.reduce((acc, p) => acc + ((p.partyBreakdown[party]?.sales || 0) * p.pts), 0);
    const partyValClosing = products.reduce((acc, p) => acc + ((p.partyBreakdown[party]?.closing || 0) * p.pts), 0);
    bRowValue.push(
      { v: `₹ ${Math.round(partyValSales).toLocaleString()}`, s: styleTotalRow },
      { v: `₹ ${Math.round(partyValClosing).toLocaleString()}`, s: styleTotalRow }
    );
  });
  bRowValue.push(
    { v: `₹ ${Math.round(summary.totalSalesValue).toLocaleString()}`, s: { ...styleTotalRow, font: { bold: true, sz: 11 } } },
    { v: `₹ ${Math.round(summary.totalClosingValue).toLocaleString()}`, s: { ...styleTotalRow, font: { bold: true, sz: 11 } } }
  );
  bData.push(bRowValue);

  const wsBreakdown = XLSX.utils.aoa_to_sheet(bData);

  // Merges for 2-Tier Breakdown Header
  wsBreakdown['!merges'] = [
    { s: { r: 0, c: 0 }, e: { r: 1, c: 0 } }, // S.N. vertical
    { s: { r: 0, c: 1 }, e: { r: 1, c: 1 } }, // PRODUCT NAME vertical
    { s: { r: 0, c: 2 }, e: { r: 1, c: 2 } }, // PTS vertical
  ];

  activeParties.forEach((_, idx) => {
    const startCol = 3 + idx * 2;
    wsBreakdown['!merges']!.push({
      s: { r: 0, c: startCol },
      e: { r: 0, c: startCol + 1 }
    });
  });

  const totStartCol = 3 + activeParties.length * 2;
  wsBreakdown['!merges']!.push({
    s: { r: 0, c: totStartCol },
    e: { r: 0, c: totStartCol + 1 }
  });

  // Column Widths for Breakdown
  const bCols: any[] = [
    { wch: 6 },
    { wch: 35 },
    { wch: 12 },
  ];
  activeParties.forEach(() => {
    bCols.push({ wch: 11 }, { wch: 12 });
  });
  bCols.push({ wch: 14 }, { wch: 16 });
  wsBreakdown['!cols'] = bCols;
  wsBreakdown['!rows'] = [{ hpt: 24 }, { hpt: 20 }];

  // Build & Trigger Download
  const wb = XLSX.utils.book_new();
  XLSX.utils.book_append_sheet(wb, ws, 'UN.SALES PROG');
  XLSX.utils.book_append_sheet(wb, wsBreakdown, 'PARTY BREAKDOWN');

  const fileName = `Dios_Master_Statement_${selectedMonth}_2026.xlsx`;
  XLSX.writeFile(wb, fileName);
}
