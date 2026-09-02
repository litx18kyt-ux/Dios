export interface FwDayEntry {
  date: number;
  day: string;
  areaWorked: string;
  tpSubmitted: string;
  drsMet: string | number;
  chemistsMet: string | number;
  withManager?: boolean;
  workType?: string; // 'Working', 'Leave', 'Holiday', 'Meeting', 'Transit', 'Admin'
}

export const memoryStore = {
  dcrDataByMonth: {} as Record<string, FwDayEntry[]>,
  currentDcrMonth: 'Aug-2026',
  effortLevelData: null as Record<string, Record<string, string>> | null,
  beName: 'BANWARI LAL MEENA',
  hqName: 'UDAIPUR',
  lastSyncedMonthCode: 'AUG'
};
