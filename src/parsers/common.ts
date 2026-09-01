import * as pdfjsLib from 'pdfjs-dist';
import { MASTER_PRODUCTS, MasterProduct } from '../data/masterProducts';

if (typeof window !== 'undefined') {
  pdfjsLib.GlobalWorkerOptions.workerSrc = `https://unpkg.com/pdfjs-dist@${pdfjsLib.version}/build/pdf.worker.min.mjs`;
}

export interface PartyParseSummary {
  partyName: string;
  fileName: string;
  itemCount: number;
  totalSales: number;
  totalClosing: number;
  items: Record<number, { sales: number; closing: number }>;
}

// Smart Normalizer: Automatically splits joined letters & numbers (e.g. M25 -> M 25, 40H -> 40 H, 60K -> 60 K)
export function cleanStr(s: string): string {
  return s
    .toUpperCase()
    .replace(/([A-Z])(\d)/g, '$1 $2')
    .replace(/(\d)([A-Z])/g, '$1 $2')
    .replace(/[^A-Z0-9\s]/g, ' ')
    .replace(/\s+/g, ' ')
    .trim();
}

function hasWord(text: string, word: string): boolean {
  const cleanW = word.replace(/[^A-Z0-9]/gi, '\\$&');
  const regex = new RegExp(`\\b${cleanW}\\b`, 'i');
  return regex.test(text);
}

const PROD_BY_SN: Record<number, MasterProduct> = {};
MASTER_PRODUCTS.forEach(p => { PROD_BY_SN[p.sn] = p; });

export function matchMasterProduct(rawName: string): MasterProduct | null {
  const c = cleanStr(rawName);

  // 1. VINTEL FAMILY (100% Isolated Pairing)
  if (c.includes('VINTEL')) {
    // 6.25
    if (c.includes('6 25') || c.includes('625') || c.includes('6.25')) return PROD_BY_SN[61]; // VINTEL CTC 6.25 TAB
    // CTC
    if (hasWord(c, 'CTC')) return PROD_BY_SN[62]; // VINTEL CTC TAB
    // CT
    if (hasWord(c, 'CT')) return PROD_BY_SN[60]; // VINTEL CT TAB
    // CD
    if (hasWord(c, 'CD')) return PROD_BY_SN[59]; // VINTEL CD TAB
    // AM / AM 40 / 40 AM
    if (hasWord(c, 'AM')) return PROD_BY_SN[58]; // VINTEL AM40 TAB
    // H 80
    if (hasWord(c, 'H') && hasWord(c, '80')) return PROD_BY_SN[64]; // VINTEL H80 TAB
    // H 40 / 40 H
    if (hasWord(c, 'H') && hasWord(c, '40')) return PROD_BY_SN[63]; // VINTEL H40 TAB
    // M 25 / 25 M
    if (hasWord(c, 'M') && hasWord(c, '25')) return PROD_BY_SN[65]; // Vintel M25 TAB
    // M 50 / 50 M
    if (hasWord(c, 'M') && hasWord(c, '50')) return PROD_BY_SN[66]; // Vintel M50 TAB
    // Pure 20
    if (hasWord(c, '20') && !hasWord(c, 'M')) return PROD_BY_SN[55]; // VINTEL 20 TAB
    // Pure 80
    if (hasWord(c, '80') && !hasWord(c, 'H')) return PROD_BY_SN[57]; // VINTEL 80 TAB
    // Pure 40 (Strictly without H, AM, M, CTC, CT)
    if (hasWord(c, '40') && !hasWord(c, 'H') && !hasWord(c, 'AM')) return PROD_BY_SN[56]; // VINTEL 40 TAB
    return PROD_BY_SN[56];
  }

  // 2. LINAGET FAMILY (100% Isolated Pairing)
  if (c.includes('LINAGET')) {
    if (hasWord(c, 'OD') && (hasWord(c, '1000') || c.includes('5 1000'))) return PROD_BY_SN[23]; // LINAGET-M-OD5/1000 TAB
    if (hasWord(c, 'OD') || c.includes('5 500') || c.includes('5/500')) return PROD_BY_SN[24]; // LINAGET-M-OD5/500 TAB
    if (hasWord(c, 'DM')) return PROD_BY_SN[19]; // LINAGET DM TAB
    if (hasWord(c, 'D')) return PROD_BY_SN[21]; // LINAGET-D TAB
    if (hasWord(c, 'E')) return PROD_BY_SN[22]; // LINAGET-E25
    if (hasWord(c, 'M') && hasWord(c, '1000')) return PROD_BY_SN[25]; // LINAGET-M1000 TAB
    if (hasWord(c, 'M') && hasWord(c, '500')) return PROD_BY_SN[26]; // LINAGET-M500 TAB
    if (hasWord(c, '5')) return PROD_BY_SN[20]; // LINAGET-5 TAB
    return PROD_BY_SN[20];
  }

  // 3. VIDMET FAMILY
  if (c.includes('VIDMET')) {
    if (hasWord(c, 'G') || hasWord(c, '80')) return PROD_BY_SN[52]; // VIDMET G 80 TAB
    if (hasWord(c, '1000') || hasWord(c, '1GM') || hasWord(c, 'GM')) return PROD_BY_SN[53]; // VIDMET SR 1000MG TAB
    if (hasWord(c, '500')) return PROD_BY_SN[54]; // VIDMET SR 500MG TAB
    return PROD_BY_SN[54];
  }

  // 4. PREMYLIN FAMILY
  if (c.includes('PREMYLIN')) {
    if (hasWord(c, 'SR') || hasWord(c, 'MSR')) return PROD_BY_SN[32]; // PREMYLIN MSR TAB
    if (hasWord(c, '75')) return PROD_BY_SN[31]; // PREMYLIN M 75 TAB
    return PROD_BY_SN[31];
  }

  // 5. VALROS FAMILY
  if (c.includes('VALROS')) {
    if (hasWord(c, 'EZ') && hasWord(c, '40')) return PROD_BY_SN[44]; // VALROS EZ-40
    if (hasWord(c, 'EZ') && hasWord(c, '20')) return PROD_BY_SN[43]; // VALROS EZ-20
    if (hasWord(c, 'EZ')) return PROD_BY_SN[42]; // VALROS EZ-10
    if (hasWord(c, 'GOLD') && hasWord(c, '20')) return PROD_BY_SN[47]; // VALROS GOLD 20 CAPS
    if (hasWord(c, 'GOLD')) return PROD_BY_SN[46]; // VALROS GOLD 10 CAPS
    if (hasWord(c, 'ASP') && hasWord(c, '150')) return PROD_BY_SN[41]; // VALROS ASP150 CAPS
    if (hasWord(c, 'ASP')) return PROD_BY_SN[40]; // VALROS ASP CAPS
    if (hasWord(c, 'F') && hasWord(c, '20')) return PROD_BY_SN[48]; // VALROS-F20 TAB
    if (hasWord(c, 'F')) return PROD_BY_SN[45]; // VALROS F TAB
    if (hasWord(c, '40')) return PROD_BY_SN[39]; // VALROS 40TAB
    if (hasWord(c, '20')) return PROD_BY_SN[38]; // VALROS 20 TAB
    if (hasWord(c, '10')) return PROD_BY_SN[37]; // VALROS 10 TAB
    return PROD_BY_SN[37];
  }

  // 6. VIDGLIT FAMILY
  if (c.includes('VIDGLIT')) {
    if (hasWord(c, 'FORTE') || hasWord(c, 'FOTRE')) return PROD_BY_SN[49]; // VIDGLIT M FOTRE TAB
    if (hasWord(c, 'M')) return PROD_BY_SN[50]; // VIDGLIT M TAB
    return PROD_BY_SN[51]; // VIDGLIT TAB
  }

  // 7. CALGYM FAMILY
  if (c.includes('CALGYM')) {
    if (hasWord(c, '60') || c.includes('60K')) return PROD_BY_SN[1]; // CALGYM 60K CAPS
    return PROD_BY_SN[2]; // CALGYM TAB
  }

  // 8. XILDA FAMILY
  if (c.includes('XILDA')) {
    if (hasWord(c, 'M') && hasWord(c, '1000')) return PROD_BY_SN[70]; // XILDA M 1000 TAB
    if (hasWord(c, 'M')) return PROD_BY_SN[71]; // XILDA M 500 TAB
    if (hasWord(c, 'P')) return PROD_BY_SN[72]; // XILDA P TAB
    return PROD_BY_SN[69]; // XILDA 50 TAB
  }

  // 9. VINVES FAMILY
  if (c.includes('VINVES') || c.includes('VINVSE')) {
    if (hasWord(c, '100')) return PROD_BY_SN[67]; // VINVES-100 TAB
    return PROD_BY_SN[68]; // VINVES-50 TAB
  }

  // 10. SOLEM FAMILY
  if (c.includes('SOLEM')) {
    if (hasWord(c, '250')) return PROD_BY_SN[35]; // SOLEM 250 TAB
    return PROD_BY_SN[36]; // SOLEM 500 TAB
  }

  // 11. ESIPRAM FAMILY
  if (c.includes('ESIPRAM')) {
    if (hasWord(c, 'PLUS')) return PROD_BY_SN[13]; // ESIPRAM PLUS TAB
    return PROD_BY_SN[12]; // ESIPRAM 10MG TAB
  }

  // 12. FITJEE FAMILY
  if (c.includes('FITJEE')) {
    if (hasWord(c, 'Q') || c.includes('Q10')) return PROD_BY_SN[17]; // FITJEE Q10 TAB
    if (hasWord(c, 'DM')) return PROD_BY_SN[16]; // FITJEE DM TABLET
    if (hasWord(c, 'CAPSULE')) return PROD_BY_SN[15]; // FITJEE CAPSULE
    return PROD_BY_SN[14]; // FITJEE CAPS
  }

  // 13. CITICURE FAMILY
  if (c.includes('CITICURE')) {
    if (hasWord(c, 'PLUS')) return PROD_BY_SN[6]; // CITICURE PLUS TAB
    return PROD_BY_SN[5]; // CITICURE 500 TAB
  }

  // 14. OTHERS
  if (c.includes('CILDIOS')) {
    if (hasWord(c, '20')) return PROD_BY_SN[4];
    return PROD_BY_SN[3];
  }
  if (c.includes('METDIOS')) {
    if (hasWord(c, '50')) return PROD_BY_SN[28];
    return PROD_BY_SN[27];
  }
  if (c.includes('DIOZAM')) {
    if (hasWord(c, '5')) return PROD_BY_SN[11];
    return PROD_BY_SN[10];
  }
  if (c.includes('NEUTOCID')) {
    if (hasWord(c, 'DSR')) return PROD_BY_SN[29];
    return PROD_BY_SN[30];
  }
  if (c.includes('PROSTADO')) {
    if (hasWord(c, 'D')) return PROD_BY_SN[33];
    return PROD_BY_SN[34];
  }
  if (c.includes('DIOFLAM')) return PROD_BY_SN[7];
  if (c.includes('DIOMILIN')) return PROD_BY_SN[8];
  if (c.includes('DIOSGLT')) return PROD_BY_SN[9];
  if (c.includes('ISIRON')) return PROD_BY_SN[18];
  if (c.includes('ZIRON')) return PROD_BY_SN[73];

  return null;
}
