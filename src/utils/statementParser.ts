import * as XLSX from 'xlsx';
import * as pdfjsLib from 'pdfjs-dist';
import { MASTER_PRODUCTS, MasterProduct } from '../data/masterProducts';

pdfjsLib.GlobalWorkerOptions.workerSrc = `https://unpkg.com/pdfjs-dist@${pdfjsLib.version}/build/pdf.worker.min.mjs`;

export interface PartyParseSummary {
  partyName: string;
  fileName: string;
  itemCount: number;
  totalSales: number;
  totalClosing: number;
  items: Record<number, { sales: number; closing: number }>;
}

export interface AggregatedProduct {
  sn: number;
  name: string;
  pts: number;
  netSec: number;
  closing: number;
  salesValue: number;
  closingValue: number;
  partyBreakdown: Record<string, { partyName: string; sales: number; closing: number }>;
}

function cleanStr(s: string): string {
  return s
    .toUpperCase()
    .replace(/[^A-Z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

interface MatchRule {
  master: MasterProduct;
  regex: RegExp;
  priority: number;
}

const MATCH_RULES: MatchRule[] = [];

MASTER_PRODUCTS.forEach(master => {
  master.keywords.forEach(kw => {
    const cleanKw = cleanStr(kw);
    const regexPattern = `\\b${cleanKw.replace(/\s+/g, '\\s+')}\\b`;
    const regex = new RegExp(regexPattern, 'i');
    
    let priority = cleanKw.length;
    if (cleanKw.includes('6 25') || cleanKw.includes('60K') || cleanKw.includes('60 K') || cleanKw.includes('60')) priority += 60;
    if (cleanKw.includes('CTC') || cleanKw.includes('F20') || cleanKw.includes('F 20') || cleanKw.includes('1GM')) priority += 55;
    if (cleanKw.includes('EZ 10') || cleanKw.includes('EZ 20') || cleanKw.includes('EZ 40')) priority += 50;
    if (cleanKw.includes('E 25') || cleanKw.includes('E25') || cleanKw.includes('M 1000') || cleanKw.includes('1000')) priority += 45;
    if (cleanKw.includes('M 75') || cleanKw.includes('M75') || cleanKw.includes('MSR')) priority += 40;
    if (cleanKw.includes('M OD') || cleanKw.includes('M 500') || cleanKw.includes('500')) priority += 35;
    if (cleanKw.includes('GOLD') || cleanKw.includes('FORTE') || cleanKw.includes('FOTRE') || cleanKw.includes('AM')) priority += 30;

    MATCH_RULES.push({ master, regex, priority });
  });
});

MATCH_RULES.sort((a, b) => b.priority - a.priority);

function matchMasterProduct(rawName: string): MasterProduct | null {
  const cleaned = cleanStr(rawName);

  for (const rule of MATCH_RULES) {
    if (rule.regex.test(cleaned)) {
      if (rule.master.name === 'VINTEL CT TAB' && /\bCTC\b/i.test(cleaned)) continue;
      if (rule.master.name === 'VALROS F TAB' && /\b(20|F20|F 20)\b/i.test(cleaned)) continue;
      if (rule.master.name === 'VINTEL 40 TAB' && /\b(AM|AM40|AM 40|H|H40|H 40)\b/i.test(cleaned)) continue;
      if (rule.master.name === 'CALGYM TAB' && /\b(60K|60 K|60)\b/i.test(cleaned)) continue;
      if (rule.master.name === 'VALROS EZ-10' && /\b(20|40)\b/i.test(cleaned)) continue;
      if (rule.master.name === 'VALROS GOLD 10 CAPS' && /\b(20|GOLD 20)\b/i.test(cleaned)) continue;
      if (rule.master.name === 'XILDA M 500 TAB' && /\b(1000|1GM)\b/i.test(cleaned)) continue;

      return rule.master;
    }
  }
  return null;
}

// -------------------------------------------------------------
// 1. Y-TOLERANCE CLUSTERED PDF EXTRACTOR
// -------------------------------------------------------------
async function parsePdfViaRTL(file: File, partyName: string): Promise<PartyParseSummary> {
  const buffer = await file.arrayBuffer();
  const pdf = await pdfjsLib.getDocument({ data: buffer }).promise;
  
  const items: Record<number, { sales: number; closing: number }> = {};
  let count = 0;
  let totalSales = 0;
  let totalClosing = 0;

  const isRP = partyName.toLowerCase().includes('r.p') || partyName.toLowerCase().includes('rp');
  const packingRegex = /(\b\d+\s*[*xX']\s*\d+\s*(?:TAB|CAP)?|\b\d+\s*S\b|\b\d+\s*'S\b|\b10S\b|\b15S\b|\b4S\b|\b1\*1\*14\s*TAB\b)/i;

  for (let pageNum = 1; pageNum <= pdf.numPages; pageNum++) {
    const page = await pdf.getPage(pageNum);
    const textContent = await page.getTextContent();

    interface RawItem {
      x: number;
      y: number;
      text: string;
    }

    const rawItems: RawItem[] = textContent.items.map((it: any) => ({
      x: it.transform[4],
      y: it.transform[5],
      text: String(it.str || '').trim()
    })).filter(it => it.text.length > 0);

    // Sort items top-to-bottom (Y descending)
    rawItems.sort((a, b) => b.y - a.y);

    // Cluster items into lines within 4px Y-tolerance
    const clusteredLines: Array<Array<{ x: number; text: string }>> = [];
    const lineRefY: number[] = [];

    rawItems.forEach(item => {
      let matchedLineIdx = -1;
      for (let i = 0; i < lineRefY.length; i++) {
        if (Math.abs(lineRefY[i] - item.y) <= 4.0) {
          matchedLineIdx = i;
          break;
        }
      }

      if (matchedLineIdx !== -1) {
        clusteredLines[matchedLineIdx].push({ x: item.x, text: item.text });
      } else {
        lineRefY.push(item.y);
        clusteredLines.push([{ x: item.x, text: item.text }]);
      }
    });

    // Process each clustered line
    clusteredLines.forEach(lineItems => {
      // Sort left-to-right (X ascending)
      lineItems.sort((a, b) => a.x - b.x);
      const fullLine = lineItems.map(it => it.text).join(' ').trim();

      if (!fullLine || fullLine.toUpperCase().includes('PAGE NO') || fullLine.toUpperCase().includes('DIOS LIFE') || fullLine.toUpperCase().includes('PRODUCT NAME') || fullLine.startsWith('***') || fullLine.toUpperCase().includes('TOTAL')) {
        return;
      }

      let rawName = '';
      let quantitiesStr = '';

      const match = fullLine.match(packingRegex);
      if (match && match.index !== undefined) {
        rawName = fullLine.slice(0, match.index).trim();
        quantitiesStr = fullLine.slice(match.index + match[0].length).trim();
      } else {
        const tokens = fullLine.split(/\s+/);
        const nums: string[] = [];
        const nTokens: string[] = [];
        for (let i = tokens.length - 1; i >= 0; i--) {
          const t = tokens[i].replace(/,/g, '');
          if (/^-?\d+(\.\d+)?$/.test(t) && nums.length < 9) {
            nums.unshift(t);
          } else {
            nTokens.unshift(tokens[i]);
          }
        }
        rawName = nTokens.join(' ');
        quantitiesStr = nums.join(' ');
      }

      if (rawName) {
        const matched = matchMasterProduct(rawName);
        if (matched) {
          const numTokens = (quantitiesStr.match(/-?\d+(\.\d+)?/g) || []).map(Number);
          let sales = 0;
          let closing = 0;

          // 8 Columns (R.P. Agencies SwilERP: Op, Rec, Ret_P, Tot, Issue, Ret_S, Closing, Exp)
          if (numTokens.length === 8 || isRP && numTokens.length >= 8) {
            sales = numTokens[4]; // Issue Qty
            closing = numTokens[6]; // Closing Balance
          }
          // 7 Columns (Sun Distributors SwilERP: Op, Rec, Tot, Issue, Closing, Dump, Exp)
          else if (numTokens.length === 7) {
            sales = numTokens[3];
            closing = numTokens[4];
          }
          // 6 Columns
          else if (numTokens.length === 6) {
            sales = numTokens[3];
            closing = numTokens[4];
          }
          // 4 Columns (Marg: Op, Rec, Issue, Closing)
          else if (numTokens.length === 4) {
            sales = numTokens[2];
            closing = numTokens[3];
          }
          else if (numTokens.length >= 2) {
            sales = numTokens[numTokens.length - 2];
            closing = numTokens[numTokens.length - 1];
          }

          if (!items[matched.sn]) {
            items[matched.sn] = { sales: 0, closing: 0 };
            count++;
          }
          items[matched.sn].sales += sales;
          items[matched.sn].closing += closing;
          totalSales += sales;
          totalClosing += closing;
        }
      }
    });
  }

  return {
    partyName,
    fileName: file.name,
    itemCount: count,
    totalSales,
    totalClosing,
    items,
  };
}

// -------------------------------------------------------------
// 2. Excel / XLS to Clean CSV Parser Pipeline
// -------------------------------------------------------------
async function parseExcelViaCsv(file: File, partyName: string): Promise<PartyParseSummary> {
  const buffer = await file.arrayBuffer();
  const wb = XLSX.read(buffer, { type: 'array' });
  const firstSheet = wb.Sheets[wb.SheetNames[0]];

  const csvContent = XLSX.utils.sheet_to_csv(firstSheet);
  const lines = csvContent.split('\n');

  const items: Record<number, { sales: number; closing: number }> = {};
  let count = 0;
  let totalSales = 0;
  let totalClosing = 0;

  let headerIdx = -1;
  let prodCol = 0;
  let salesCol = -1;
  let closingCol = -1;

  for (let i = 0; i < Math.min(lines.length, 15); i++) {
    const line = lines[i] || '';
    const upper = line.toUpperCase();

    if (upper.includes('PRODUCT') || upper.includes('ITEM') || upper.includes('DESCRIPTION')) {
      headerIdx = i;
      const headers = line.split(',');
      headers.forEach((h, idx) => {
        const hClean = h.replace(/[^A-Z]/gi, '').toUpperCase();
        if (hClean.includes('PRODUCT') || hClean.includes('ITEM') || hClean.includes('DESC')) prodCol = idx;
        if (hClean.includes('ISSUE') || hClean.includes('SALES') || hClean.includes('NETSEC')) salesCol = idx;
        if (hClean.includes('CLOSING') || hClean.includes('BALANCE')) closingCol = idx;
      });
      break;
    }
  }

  if (salesCol === -1) salesCol = partyName.includes('Vardhman') ? 7 : (partyName.includes('Modi') ? 4 : 6);
  if (closingCol === -1) closingCol = partyName.includes('Vardhman') ? 13 : (partyName.includes('Modi') ? 5 : 8);

  const startRow = headerIdx >= 0 ? headerIdx + 1 : 1;

  for (let i = startRow; i < lines.length; i++) {
    const line = lines[i];
    if (!line || !line.trim()) continue;

    const cols = line.split(',').map(c => c.replace(/^"|"$/g, '').trim());
    const rawProd = cols[prodCol] || '';

    if (!rawProd || rawProd.toUpperCase().includes('TOTAL') || rawProd.toUpperCase().includes('GRAND')) continue;

    const matched = matchMasterProduct(rawProd);
    if (matched) {
      const sales = parseFloat(cols[salesCol] || '0') || 0;
      const closing = parseFloat(cols[closingCol] || '0') || 0;

      if (!items[matched.sn]) {
        items[matched.sn] = { sales: 0, closing: 0 };
        count++;
      }
      items[matched.sn].sales += sales;
      items[matched.sn].closing += closing;
      totalSales += sales;
      totalClosing += closing;
    }
  }

  return {
    partyName,
    fileName: file.name,
    itemCount: count,
    totalSales,
    totalClosing,
    items,
  };
}

export async function parseSinglePartyFile(file: File, partyName: string): Promise<PartyParseSummary> {
  const isPdf = file.name.toLowerCase().endsWith('.pdf') || file.type.includes('pdf');
  if (isPdf) {
    return await parsePdfViaRTL(file, partyName);
  } else {
    return await parseExcelViaCsv(file, partyName);
  }
}
