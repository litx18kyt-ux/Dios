export interface FwDayEntry {
  date: number;
  day: string;
  areaWorked: string;
  tpSubmitted: string;
  drsMet: string | number;
  chemistsMet: string | number;
  withManager?: boolean;
  workType?: string;
}

export interface PartyBreakdownItem {
  id: string;
  partyName: string;
  amount: number;
  note?: string;
}

export interface MonthBreakdownMap {
  [key: string]: PartyBreakdownItem[];
}

export interface DhruviProductEntry {
  sn: number;
  salesFormula: string;
  salesQty: number;
  closingFormula: string;
  closingQty: number;
}

export const DEFAULT_STOCKISTS = [
  'NAGDA DISTRIBUTORS',
  'MODI DISTRIBUTORS',
  'SHREE VARDHMAN PHARMA',
  'SUN DISTRIBUTORS',
  'R.P. AGENCIES',
  'DWARIKA MEDICALS'
];

export const memoryStore = {
  dcrDataByMonth: {} as Record<string, FwDayEntry[]>,
  currentDcrMonth: 'Aug-2026',
  effortLevelData: null as Record<string, Record<string, string>> | null,
  salesBreakdown: {} as MonthBreakdownMap,
  dhruviEntries: {} as Record<number, DhruviProductEntry>,
  beName: 'BANWARI LAL MEENA',
  hqName: 'UDAIPUR',
  lastSyncedMonthCode: 'AUG'
};
