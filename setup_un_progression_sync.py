import os, sys

# 1. Create NEW FILE: src/data/seedUnSalesProg.ts (Exact historical data from 4_UN.SALES PROG..csv)
seed_code = '''export interface MonthUnitProgression {
  netPri: number;
  netSec: number;
  closing: number;
}

export interface ProductProgressionMap {
  [sn: number]: MonthUnitProgression;
}

export interface YearProgressionStore {
  [monthCode: string]: ProductProgressionMap;
}

export const INITIAL_UN_PROGRESSION_SEED: YearProgressionStore = {
  APR: {
    1: { netPri: 620, netSec: 495, closing: 385 },
    2: { netPri: 219, netSec: 139, closing: 260 },
    3: { netPri: 0, netSec: 0, closing: 0 },
    4: { netPri: 0, netSec: 0, closing: 0 },
    5: { netPri: 0, netSec: 0, closing: 0 },
    6: { netPri: 0, netSec: 2, closing: 24 },
    7: { netPri: 0, netSec: 0, closing: 0 },
    8: { netPri: 80, netSec: 76, closing: 91 },
    9: { netPri: 0, netSec: 8, closing: 37 },
    10: { netPri: 0, netSec: 0, closing: 0 },
    11: { netPri: 0, netSec: 0, closing: 0 },
    12: { netPri: 186, netSec: 245, closing: 212 },
    13: { netPri: 274, netSec: 374, closing: 135 },
    14: { netPri: 62, netSec: 0, closing: 10 },
    15: { netPri: 0, netSec: 0, closing: 140 },
    16: { netPri: 10, netSec: 20, closing: 22 },
    17: { netPri: 10, netSec: 12, closing: 55 },
    18: { netPri: 90, netSec: 35, closing: 21 },
    19: { netPri: 0, netSec: 9, closing: 44 },
    20: { netPri: 0, netSec: 48, closing: 30 },
    21: { netPri: 0, netSec: 3, closing: 13 },
    22: { netPri: 22, netSec: 39, closing: 46 },
    23: { netPri: 0, netSec: 5, closing: 6 },
    24: { netPri: 40, netSec: 40, closing: 57 },
    25: { netPri: 0, netSec: 0, closing: 0 },
    26: { netPri: 0, netSec: 9, closing: 7 },
    27: { netPri: 0, netSec: 0, closing: 0 },
    28: { netPri: 0, netSec: 0, closing: 0 },
    29: { netPri: 0, netSec: 0, closing: 0 },
    30: { netPri: 20, netSec: 10, closing: 20 },
    31: { netPri: 8, netSec: 134, closing: 111 },
    32: { netPri: 311, netSec: 277, closing: 309 },
    33: { netPri: 0, netSec: 6, closing: 62 },
    34: { netPri: 0, netSec: 0, closing: 20 },
    35: { netPri: 0, netSec: 0, closing: 0 },
    36: { netPri: 0, netSec: 0, closing: 0 },
    37: { netPri: 90, netSec: 138, closing: 207 },
    38: { netPri: 0, netSec: 59, closing: 97 },
    39: { netPri: 0, netSec: 0, closing: 0 },
    40: { netPri: 0, netSec: 42, closing: 109 },
    41: { netPri: 0, netSec: 0, closing: 33 },
    42: { netPri: 0, netSec: 0, closing: 0 },
    43: { netPri: 0, netSec: 0, closing: 0 },
    44: { netPri: 0, netSec: 0, closing: 0 },
    45: { netPri: 200, netSec: 199, closing: 135 },
    46: { netPri: 42, netSec: 35, closing: 65 },
    47: { netPri: 20, netSec: 34, closing: 116 },
    48: { netPri: 0, netSec: 2, closing: 76 },
    49: { netPri: 0, netSec: 0, closing: 0 },
    50: { netPri: 69, netSec: 116, closing: 111 },
    51: { netPri: 20, netSec: 29, closing: 34 },
    52: { netPri: 170, netSec: 171, closing: 243 },
    53: { netPri: 0, netSec: 43, closing: 148 },
    54: { netPri: 309, netSec: 1247, closing: 186 },
    55: { netPri: 100, netSec: 119, closing: 89 },
    56: { netPri: 370, netSec: 493, closing: 126 },
    57: { netPri: 0, netSec: 0, closing: 0 },
    58: { netPri: 170, netSec: 147, closing: 221 },
    59: { netPri: 0, netSec: 3, closing: 7 },
    60: { netPri: 40, netSec: 85, closing: 118 },
    61: { netPri: 0, netSec: 0, closing: 0 },
    62: { netPri: 922, netSec: 1048, closing: 546 },
    63: { netPri: 43, netSec: 91, closing: 84 },
    64: { netPri: 0, netSec: 0, closing: 0 },
    65: { netPri: 5, netSec: 23, closing: 72 },
    66: { netPri: 0, netSec: 14, closing: 18 },
    67: { netPri: 0, netSec: 0, closing: 0 },
    68: { netPri: 0, netSec: 2, closing: 19 },
    69: { netPri: 0, netSec: 0, closing: 0 },
    70: { netPri: 0, netSec: 4, closing: 34 },
    71: { netPri: 80, netSec: 73, closing: 114 },
    72: { netPri: 0, netSec: 0, closing: 0 },
    73: { netPri: 0, netSec: 0, closing: 0 }
  },
  MAY: {
    1: { netPri: 490, netSec: 350, closing: 147 },
    2: { netPri: 220, netSec: 128, closing: 143 },
    3: { netPri: 0, netSec: 0, closing: 0 },
    4: { netPri: 0, netSec: 0, closing: 0 },
    5: { netPri: 0, netSec: 0, closing: 0 },
    6: { netPri: 10, netSec: 8, closing: 10 },
    7: { netPri: 0, netSec: 0, closing: 0 },
    8: { netPri: 86, netSec: 123, closing: 47 },
    9: { netPri: 65, netSec: 39, closing: 36 },
    10: { netPri: 0, netSec: 0, closing: 0 },
    11: { netPri: 0, netSec: 0, closing: 0 },
    12: { netPri: 170, netSec: 251, closing: 101 },
    13: { netPri: 269, netSec: 276, closing: 172 },
    14: { netPri: 100, netSec: 121, closing: 19 },
    15: { netPri: 0, netSec: 0, closing: 0 },
    16: { netPri: 4, netSec: 8, closing: 7 },
    17: { netPri: 0, netSec: 14, closing: 0 },
    18: { netPri: 30, netSec: 34, closing: 37 },
    19: { netPri: 30, netSec: 6, closing: 18 },
    20: { netPri: 0, netSec: 17, closing: 9 },
    21: { netPri: 24, netSec: 40, closing: 99 },
    22: { netPri: 0, netSec: 27, closing: 61 },
    23: { netPri: 0, netSec: 0, closing: 0 },
    24: { netPri: 20, netSec: 9, closing: 5 },
    25: { netPri: 0, netSec: 0, closing: 0 },
    26: { netPri: 10, netSec: 31, closing: 0 },
    27: { netPri: 0, netSec: 0, closing: 0 },
    28: { netPri: 0, netSec: 0, closing: 0 },
    29: { netPri: 0, netSec: 0, closing: 0 },
    30: { netPri: 10, netSec: 11, closing: 19 },
    31: { netPri: 10, netSec: 46, closing: 85 },
    32: { netPri: 220, netSec: 195, closing: 229 },
    33: { netPri: 10, netSec: 26, closing: 41 },
    34: { netPri: 0, netSec: 3, closing: 17 },
    35: { netPri: 0, netSec: 0, closing: 0 },
    36: { netPri: 30, netSec: 49, closing: 0 },
    37: { netPri: 75, netSec: 80, closing: 259 },
    38: { netPri: 30, netSec: 41, closing: 79 },
    39: { netPri: 0, netSec: 0, closing: 0 },
    40: { netPri: 60, netSec: 36, closing: 100 },
    41: { netPri: 0, netSec: 0, closing: 0 },
    42: { netPri: 60, netSec: 56, closing: 19 },
    43: { netPri: 30, netSec: 0, closing: 0 },
    44: { netPri: 0, netSec: 0, closing: 0 },
    45: { netPri: 120, netSec: 112, closing: 167 },
    46: { netPri: 15, netSec: 9, closing: 70 },
    47: { netPri: 40, netSec: 24, closing: 160 },
    48: { netPri: 0, netSec: 3, closing: 41 },
    49: { netPri: 0, netSec: 0, closing: 0 },
    50: { netPri: 70, netSec: 95, closing: 25 },
    51: { netPri: 10, netSec: 24, closing: 26 },
    52: { netPri: 220, netSec: 259, closing: 206 },
    53: { netPri: 0, netSec: 83, closing: 44 },
    54: { netPri: 255, netSec: 935, closing: 167 },
    55: { netPri: 0, netSec: 25, closing: 75 },
    56: { netPri: 510, netSec: 408, closing: 46 },
    57: { netPri: 0, netSec: 0, closing: 0 },
    58: { netPri: 70, netSec: 96, closing: 120 },
    59: { netPri: 20, netSec: 5, closing: 18 },
    60: { netPri: 170, netSec: 135, closing: 63 },
    61: { netPri: 0, netSec: 0, closing: 0 },
    62: { netPri: 548, netSec: 850, closing: 500 },
    63: { netPri: 160, netSec: 150, closing: 128 },
    64: { netPri: 0, netSec: 0, closing: 0 },
    65: { netPri: 0, netSec: 20, closing: 68 },
    66: { netPri: 20, netSec: 20, closing: 23 },
    67: { netPri: 0, netSec: 0, closing: 0 },
    68: { netPri: 0, netSec: 3, closing: 16 },
    69: { netPri: 0, netSec: 0, closing: 0 },
    70: { netPri: 0, netSec: 0, closing: 0 },
    71: { netPri: 128, netSec: 96, closing: 51 },
    72: { netPri: 0, netSec: 0, closing: 0 },
    73: { netPri: 0, netSec: 0, closing: 0 }
  },
  JUN: {
    1: { netPri: 258, netSec: 353, closing: 308 },
    2: { netPri: 30, netSec: 123, closing: 254 },
    3: { netPri: 0, netSec: 0, closing: 0 },
    4: { netPri: 10, netSec: 10, closing: 0 },
    5: { netPri: 0, netSec: 0, closing: 0 },
    6: { netPri: 0, netSec: 0, closing: 6 },
    7: { netPri: 0, netSec: 0, closing: 0 },
    8: { netPri: 96, netSec: 180, closing: 153 },
    9: { netPri: 0, netSec: 15, closing: 63 },
    10: { netPri: 0, netSec: 0, closing: 0 },
    11: { netPri: 0, netSec: 0, closing: 0 },
    12: { netPri: 230, netSec: 254, closing: 89 },
    13: { netPri: 315, netSec: 230, closing: 199 },
    14: { netPri: 10, netSec: 130, closing: 19 },
    15: { netPri: 0, netSec: 0, closing: 0 },
    16: { netPri: 30, netSec: 16, closing: 1 },
    17: { netPri: 50, netSec: 25, closing: 15 },
    18: { netPri: 10, netSec: 22, closing: 46 },
    19: { netPri: 0, netSec: 15, closing: 33 },
    20: { netPri: 18, netSec: 18, closing: 0 },
    21: { netPri: 15, netSec: 40, closing: 81 },
    22: { netPri: 20, netSec: 40, closing: 52 },
    23: { netPri: 0, netSec: 6, closing: 0 },
    24: { netPri: 20, netSec: 46, closing: 21 },
    25: { netPri: 0, netSec: 0, closing: 0 },
    26: { netPri: 23, netSec: 21, closing: 5 },
    27: { netPri: 20, netSec: 10, closing: 0 },
    28: { netPri: 17, netSec: 10, closing: 0 },
    29: { netPri: 0, netSec: 0, closing: 0 },
    30: { netPri: 20, netSec: 12, closing: 27 },
    31: { netPri: 70, netSec: 92, closing: 88 },
    32: { netPri: 493, netSec: 419, closing: 69 },
    33: { netPri: 10, netSec: 16, closing: 28 },
    34: { netPri: 0, netSec: 0, closing: 0 },
    35: { netPri: 0, netSec: 0, closing: 0 },
    36: { netPri: 0, netSec: 0, closing: 0 },
    37: { netPri: 150, netSec: 104, closing: 176 },
    38: { netPri: 30, netSec: 40, closing: 55 },
    39: { netPri: 0, netSec: 0, closing: 0 },
    40: { netPri: 50, netSec: 32, closing: 71 },
    41: { netPri: 0, netSec: 0, closing: 0 },
    42: { netPri: 60, netSec: 38, closing: 41 },
    43: { netPri: 30, netSec: 31, closing: 14 },
    44: { netPri: 50, netSec: 30, closing: 0 },
    45: { netPri: 60, netSec: 186, closing: 108 },
    46: { netPri: 0, netSec: 13, closing: 79 },
    47: { netPri: 15, netSec: 22, closing: 73 },
    48: { netPri: 0, netSec: 6, closing: 35 },
    49: { netPri: 0, netSec: 3, closing: 7 },
    50: { netPri: 60, netSec: 59, closing: 37 },
    51: { netPri: 41, netSec: 42, closing: 12 },
    52: { netPri: 246, netSec: 239, closing: 108 },
    53: { netPri: 130, netSec: 136, closing: 124 },
    54: { netPri: 1640, netSec: 1584, closing: 165 },
    55: { netPri: 230, netSec: 13, closing: 49 },
    56: { netPri: 113, netSec: 415, closing: 135 },
    57: { netPri: 0, netSec: 0, closing: 0 },
    58: { netPri: 630, netSec: 77, closing: 92 },
    59: { netPri: 10, netSec: 10, closing: 0 },
    60: { netPri: 380, netSec: 108, closing: 94 },
    61: { netPri: 0, netSec: 0, closing: 0 },
    62: { netPri: 698, netSec: 926, closing: 252 },
    63: { netPri: 91, netSec: 141, closing: 143 },
    64: { netPri: 0, netSec: 0, closing: 0 },
    65: { netPri: 43, netSec: 27, closing: 18 },
    66: { netPri: 0, netSec: 0, closing: 0 },
    67: { netPri: 0, netSec: 0, closing: 0 },
    68: { netPri: 0, netSec: 0, closing: 0 },
    69: { netPri: 0, netSec: 0, closing: 0 },
    70: { netPri: 10, netSec: 18, closing: 0 },
    71: { netPri: 60, netSec: 110, closing: 96 },
    72: { netPri: 0, netSec: 0, closing: 0 },
    73: { netPri: 0, netSec: 0, closing: 0 }
  },
  JUL: {
    1: { netPri: 316, netSec: 413, closing: 329 },
    2: { netPri: 63, netSec: 89, closing: 260 },
    3: { netPri: 0, netSec: 0, closing: 0 },
    4: { netPri: 0, netSec: 0, closing: 10 },
    5: { netPri: 0, netSec: 0, closing: 0 },
    6: { netPri: 10, netSec: 10, closing: 26 },
    7: { netPri: 0, netSec: 0, closing: 0 },
    8: { netPri: 43, netSec: 93, closing: 120 },
    9: { netPri: 96, netSec: 45, closing: 94 },
    10: { netPri: 0, netSec: 0, closing: 0 },
    11: { netPri: 0, netSec: 0, closing: 0 },
    12: { netPri: 116, netSec: 229, closing: 230 },
    13: { netPri: 143, netSec: 231, closing: 369 },
    14: { netPri: 0, netSec: 0, closing: 0 },
    15: { netPri: 18, netSec: 11, closing: 48 },
    16: { netPri: -13, netSec: 3, closing: 53 },
    17: { netPri: 19, netSec: 9, closing: 54 },
    18: { netPri: 0, netSec: 12, closing: 53 },
    19: { netPri: 0, netSec: 12, closing: 21 },
    20: { netPri: 15, netSec: 46, closing: 24 },
    21: { netPri: 53, netSec: 25, closing: 140 },
    22: { netPri: 120, netSec: 46, closing: 131 },
    23: { netPri: 0, netSec: 0, closing: 0 },
    24: { netPri: 29, netSec: 16, closing: 60 },
    25: { netPri: 0, netSec: 0, closing: 0 },
    26: { netPri: 0, netSec: 8, closing: 15 },
    27: { netPri: 0, netSec: 0, closing: 20 },
    28: { netPri: 0, netSec: 0, closing: 20 },
    29: { netPri: 0, netSec: 0, closing: 0 },
    30: { netPri: 0, netSec: 6, closing: 21 },
    31: { netPri: 11, netSec: 117, closing: 214 },
    32: { netPri: 249, netSec: 272, closing: 366 },
    33: { netPri: 100, netSec: 74, closing: 77 },
    34: { netPri: 0, netSec: 3, closing: 29 },
    35: { netPri: 0, netSec: 0, closing: 0 },
    36: { netPri: 50, netSec: 40, closing: 50 },
    37: { netPri: 35, netSec: 116, closing: 317 },
    38: { netPri: 56, netSec: 33, closing: 80 },
    39: { netPri: 0, netSec: 0, closing: 15 },
    40: { netPri: 106, netSec: 84, closing: 84 },
    41: { netPri: 0, netSec: 0, closing: 30 },
    42: { netPri: 60, netSec: 42, closing: 68 },
    43: { netPri: 0, netSec: 14, closing: 30 },
    44: { netPri: 30, netSec: 0, closing: 60 },
    45: { netPri: 331, netSec: 118, closing: 97 },
    46: { netPri: -2, netSec: 16, closing: 95 },
    47: { netPri: 29, netSec: 49, closing: 92 },
    48: { netPri: 0, netSec: 0, closing: 111 },
    49: { netPri: 10, netSec: 7, closing: 40 },
    50: { netPri: 225, netSec: 143, closing: 80 },
    51: { netPri: 80, netSec: 41, closing: 71 },
    52: { netPri: 154, netSec: 216, closing: 232 },
    53: { netPri: 50, netSec: 143, closing: 156 },
    54: { netPri: 200, netSec: 1190, closing: 339 },
    55: { netPri: -221, netSec: 15, closing: 55 },
    56: { netPri: 370, netSec: 185, closing: 534 },
    57: { netPri: 0, netSec: 0, closing: 0 },
    58: { netPri: -491, netSec: 99, closing: 218 },
    59: { netPri: 20, netSec: 6, closing: 16 },
    60: { netPri: -200, netSec: 104, closing: 76 },
    61: { netPri: 150, netSec: 0, closing: 0 },
    62: { netPri: 1042, netSec: 987, closing: 615 },
    63: { netPri: 44, netSec: 113, closing: 167 },
    64: { netPri: 0, netSec: 0, closing: 0 },
    65: { netPri: 34, netSec: 25, closing: 99 },
    66: { netPri: 60, netSec: 35, closing: 46 },
    67: { netPri: 20, netSec: 0, closing: 20 },
    68: { netPri: 50, netSec: 13, closing: 33 },
    69: { netPri: 0, netSec: 0, closing: 0 },
    70: { netPri: -14, netSec: 0, closing: 6 },
    71: { netPri: 51, netSec: 109, closing: 111 },
    72: { netPri: 0, netSec: 0, closing: 0 },
    73: { netPri: 0, netSec: 0, closing: 0 }
  }
};
'''
with open("/workspaces/Dios/src/data/seedUnSalesProg.ts", "w") as f:
    f.write(seed_code)
print("✓ Created src/data/seedUnSalesProg.ts with complete historical data for APR, MAY, JUN, JUL!")

# 2. Create NEW FILE: src/data/unProgressionStore.ts (Universal Persistence & Auto-Sync Engine)
store_code = '''import { INITIAL_UN_PROGRESSION_SEED, YearProgressionStore, ProductProgressionMap } from './seedUnSalesProg';
import { MASTER_PRODUCTS } from './masterProducts';

const STORAGE_KEY = 'dios_un_sales_progression_v1';

export const MONTH_CODES = ['APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC', 'JAN', 'FEB', 'MAR'];

export class UnProgressionStore {
  private data: YearProgressionStore;

  constructor() {
    this.data = this.loadFromStorage();
  }

  private loadFromStorage(): YearProgressionStore {
    try {
      const saved = localStorage.getItem(STORAGE_KEY);
      if (saved) {
        const parsed = JSON.parse(saved);
        // Merge with seed to ensure all products exist
        MONTH_CODES.forEach(m => {
          if (!parsed[m]) parsed[m] = {};
          const seedMonth = INITIAL_UN_PROGRESSION_SEED[m] || {};
          MASTER_PRODUCTS.forEach(p => {
            if (!parsed[m][p.sn]) {
              parsed[m][p.sn] = seedMonth[p.sn] || { netPri: 0, netSec: 0, closing: 0 };
            }
          });
        });
        return parsed;
      }
    } catch(e) {}

    // Default Seed
    const initial: YearProgressionStore = {};
    MONTH_CODES.forEach(m => {
      initial[m] = {};
      const seedMonth = INITIAL_UN_PROGRESSION_SEED[m] || {};
      MASTER_PRODUCTS.forEach(p => {
        initial[m][p.sn] = seedMonth[p.sn] || { netPri: 0, netSec: 0, closing: 0 };
      });
    });
    return initial;
  }

  public getData(): YearProgressionStore {
    return this.data;
  }

  public getMonthData(monthCode: string): ProductProgressionMap {
    return this.data[monthCode] || {};
  }

  public updateCell(monthCode: string, sn: number, field: 'netPri' | 'netSec' | 'closing', value: number) {
    if (!this.data[monthCode]) this.data[monthCode] = {};
    if (!this.data[monthCode][sn]) this.data[monthCode][sn] = { netPri: 0, netSec: 0, closing: 0 };
    this.data[monthCode][sn][field] = value;
    this.persist();
  }

  public syncFromAggregator(monthCode: string, aggregatedProducts: Array<{ sn: number; netPri?: number; netSec: number; closing: number }>) {
    if (!this.data[monthCode]) this.data[monthCode] = {};
    aggregatedProducts.forEach(p => {
      this.data[monthCode][p.sn] = {
        netPri: p.netPri !== undefined ? p.netPri : 0,
        netSec: p.netSec || 0,
        closing: p.closing || 0
      };
    });
    this.persist();
  }

  public resetToSeed() {
    localStorage.removeItem(STORAGE_KEY);
    this.data = this.loadFromStorage();
  }

  private persist() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(this.data));
    } catch(e) {}
  }
}

export const unProgressionStore = new UnProgressionStore();
'''
with open("/workspaces/Dios/src/data/unProgressionStore.ts", "w") as f:
    f.write(store_code)
print("✓ Created src/data/unProgressionStore.ts with multi-month sync engine!")

# 3. Update UnSalesProgSheet.tsx with Auto-Sync Button, Month Filter, CUMM & Value Totals
un_sheet_code = '''import React, { useState, useEffect } from 'react';
import { Table2, Search, Zap, Save, Download, RefreshCw, Check, Info } from 'lucide-react';
import { MASTER_PRODUCTS } from '../../data/masterProducts';
import { unProgressionStore, MONTH_CODES } from '../../data/unProgressionStore';

export const UnSalesProgSheet: React.FC = () => {
  const [search, setSearch] = useState('');
  const [targetMonth, setTargetMonth] = useState('AUG');
  const [gridData, setGridData] = useState(() => unProgressionStore.getData());
  const [statusMsg, setStatusMsg] = useState<string | null>(null);

  const filtered = MASTER_PRODUCTS.filter(p => 
    p.name.toLowerCase().includes(search.toLowerCase()) || String(p.sn).includes(search)
  );

  const handleCellChange = (month: string, sn: number, field: 'netPri' | 'netSec' | 'closing', valStr: string) => {
    const val = parseFloat(valStr) || 0;
    unProgressionStore.updateCell(month, sn, field, val);
    setGridData({ ...unProgressionStore.getData() });
  };

  const handleAutoSyncFromMemory = () => {
    setGridData({ ...unProgressionStore.getData() });
    setStatusMsg(`🎉 Synced '${targetMonth}' from Statement Aggregator!`);
    setTimeout(() => setStatusMsg(null), 3500);
  };

  const handleSave = () => {
    setStatusMsg('✅ Data saved successfully to persistent memory!');
    setTimeout(() => setStatusMsg(null), 2500);
  };

  const handleExportCSV = () => {
    let csv = `UNIT SALES PROGRESSION (HQ TOTAL)\n`;
    csv += `S.N.,PRODUCT NAME,PTS,` + MONTH_CODES.map(m => `${m} PRI,${m} SEC,${m} CL`).join(',') + `,CUMM PRI,CUMM SEC,CUMM CL,TOTAL SEC VAL (Rs)\n`;
    
    MASTER_PRODUCTS.forEach(p => {
      let cummPri = 0;
      let cummSec = 0;
      let cummCl = 0;
      
      const mCells: string[] = [];
      MONTH_CODES.forEach(m => {
        const item = gridData[m]?.[p.sn] || { netPri: 0, netSec: 0, closing: 0 };
        cummPri += item.netPri || 0;
        cummSec += item.netSec || 0;
        cummCl += item.closing || 0;
        mCells.push(`${item.netPri || ''},${item.netSec || ''},${item.closing || ''}`);
      });

      const totalVal = cummSec * p.pts;
      csv += `${p.sn},"${p.name}",${p.pts.toFixed(2)},${mCells.join(',')},${cummPri},${cummSec},${cummCl},${Math.round(totalVal)}\n`;
    });

    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.setAttribute('download', `4_UN_SALES_PROG_HQ_TOTAL.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="bg-slate-900 border border-slate-800 rounded-2xl p-4 md:p-6 shadow-xl space-y-4">
      {/* Top Header */}
      <div className="flex flex-col lg:flex-row lg:items-center justify-between gap-4 pb-4 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <span className="p-2.5 bg-cyan-500/20 text-cyan-400 rounded-xl border border-cyan-500/30">
            <Table2 size={22} />
          </span>
          <div>
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              4. UNIT SALES PROGRESSION (HQ TOTAL)
              <span className="text-[10px] bg-cyan-500/20 text-cyan-300 border border-cyan-500/40 px-2 py-0.5 rounded-full font-mono font-bold">
                12-Month Live Engine
              </span>
            </h2>
            <p className="text-xs text-slate-400">Pre-seeded APR-JUL • Auto-Sync with Statement Aggregator</p>
          </div>
        </div>

        {/* Action Controls */}
        <div className="flex flex-wrap items-center gap-2.5">
          {/* Target Month Select */}
          <div className="flex items-center gap-2 bg-slate-950 px-3 py-1.5 rounded-xl border border-cyan-500/40">
            <span className="text-xs text-slate-400 font-semibold">Month:</span>
            <select
              value={targetMonth}
              onChange={(e) => setTargetMonth(e.target.value)}
              className="bg-transparent text-xs font-bold text-cyan-400 focus:outline-none cursor-pointer"
            >
              {MONTH_CODES.map(m => (
                <option key={m} value={m} className="bg-slate-900 text-white">{m} 2026</option>
              ))}
            </select>

            <button
              onClick={handleAutoSyncFromMemory}
              className="flex items-center gap-1.5 px-3 py-1.5 bg-gradient-to-r from-cyan-600 to-blue-600 hover:from-cyan-500 hover:to-blue-500 text-white rounded-lg text-xs font-bold shadow-md shadow-cyan-600/20 transition cursor-pointer"
            >
              <Zap size={14} className="text-yellow-300" /> Auto-Sync {targetMonth}
            </button>
          </div>

          <button
            onClick={handleSave}
            className="flex items-center gap-1.5 px-3.5 py-2 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 rounded-xl text-xs font-semibold transition cursor-pointer"
          >
            <Save size={14} /> Save
          </button>

          <button
            onClick={handleExportCSV}
            className="flex items-center gap-1.5 px-3.5 py-2 bg-emerald-600 hover:bg-emerald-500 text-white rounded-xl text-xs font-bold shadow-md shadow-emerald-600/20 transition cursor-pointer"
          >
            <Download size={14} /> Export CSV
          </button>
        </div>
      </div>

      {statusMsg && (
        <div className="p-3 bg-emerald-950/70 border border-emerald-500/50 text-emerald-300 rounded-xl text-xs flex items-center gap-2">
          <Check size={16} className="text-emerald-400 shrink-0" />
          <span>{statusMsg}</span>
        </div>
      )}

      {/* Search Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3">
        <div className="relative w-full sm:w-80">
          <Search size={14} className="absolute left-3 top-1/2 -translate-y-1/2 text-slate-500" />
          <input
            type="text"
            placeholder="Search in 73 products..."
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-8 pr-3 py-1.5 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
          />
        </div>
        <div className="text-xs text-slate-400 flex items-center gap-2">
          <Info size={14} className="text-cyan-400" />
          <span>Statement Aggregator me <b>"Sync to Data Hub"</b> karne par yahan live refresh ho jata hai.</span>
        </div>
      </div>

      {/* Main 12-Month Table */}
      <div className="overflow-x-auto max-h-[620px] border border-slate-800 rounded-xl">
        <table className="w-full text-left text-xs border-collapse">
          <thead className="sticky top-0 bg-slate-950 text-slate-400 font-bold uppercase border-b border-slate-800 z-20">
            <tr>
              <th rowSpan={2} className="p-2.5 text-center w-10 bg-slate-950 border-r border-slate-800">S.N.</th>
              <th rowSpan={2} className="p-2.5 min-w-[200px] bg-slate-950 border-r border-slate-800">Product Name</th>
              <th rowSpan={2} className="p-2.5 text-right w-20 bg-slate-950 border-r border-slate-800">PTS (₹)</th>
              {MONTH_CODES.map(m => (
                <th
                  key={m}
                  colSpan={3}
                  className={`p-2 text-center border-r border-slate-800 ${m === targetMonth ? 'bg-cyan-950/60 text-cyan-300 font-extrabold border-b-2 border-cyan-400' : 'bg-slate-950'}`}
                >
                  {m} 2026
                </th>
              ))}
              <th colSpan={3} className="p-2 text-center bg-purple-950/40 text-purple-300 border-r border-slate-800">CUMM UNITS</th>
              <th rowSpan={2} className="p-2.5 text-right min-w-[110px] bg-emerald-950/40 text-emerald-300 font-bold">TOTAL SEC (₹)</th>
            </tr>
            <tr className="border-b border-slate-800 text-[10px]">
              {MONTH_CODES.map(m => (
                <React.Fragment key={m}>
                  <th className="p-1 text-center text-blue-400 bg-slate-950/80 w-14">PRI</th>
                  <th className="p-1 text-center text-cyan-400 bg-slate-950/80 w-14">SEC</th>
                  <th className="p-1 text-center text-emerald-400 bg-slate-950/80 w-14 border-r border-slate-800">CL</th>
                </React.Fragment>
              ))}
              <th className="p-1 text-center text-blue-300 bg-purple-950/30 w-14">PRI</th>
              <th className="p-1 text-center text-cyan-300 bg-purple-950/30 w-14">SEC</th>
              <th className="p-1 text-center text-emerald-300 bg-purple-950/30 w-14 border-r border-slate-800">CL</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60">
            {filtered.map(p => {
              let cummPri = 0;
              let cummSec = 0;
              let cummCl = 0;

              return (
                <tr key={p.sn} className="hover:bg-slate-800/40 transition">
                  <td className="p-2 text-center text-slate-500 font-mono border-r border-slate-800/60">{p.sn}</td>
                  <td className="p-2 font-medium text-white border-r border-slate-800/60">{p.name}</td>
                  <td className="p-2 text-right font-mono text-amber-300 border-r border-slate-800/60">{p.pts.toFixed(2)}</td>

                  {MONTH_CODES.map(m => {
                    const item = gridData[m]?.[p.sn] || { netPri: 0, netSec: 0, closing: 0 };
                    cummPri += item.netPri || 0;
                    cummSec += item.netSec || 0;
                    cummCl += item.closing || 0;
                    const isTarget = m === targetMonth;

                    return (
                      <React.Fragment key={m}>
                        {/* NET PRI */}
                        <td className={`p-0.5 text-center ${isTarget ? 'bg-blue-950/20' : ''}`}>
                          <input
                            type="text"
                            value={item.netPri !== 0 ? item.netPri : ''}
                            onChange={e => handleCellChange(m, p.sn, 'netPri', e.target.value)}
                            placeholder="-"
                            className="w-full py-1 px-1 bg-transparent text-center font-mono text-xs text-blue-300 focus:bg-slate-950 focus:outline-none"
                          />
                        </td>
                        {/* NET SEC */}
                        <td className={`p-0.5 text-center ${isTarget ? 'bg-cyan-950/20' : ''}`}>
                          <input
                            type="text"
                            value={item.netSec !== 0 ? item.netSec : ''}
                            onChange={e => handleCellChange(m, p.sn, 'netSec', e.target.value)}
                            placeholder="-"
                            className="w-full py-1 px-1 bg-transparent text-center font-mono text-xs text-cyan-300 font-bold focus:bg-slate-950 focus:outline-none"
                          />
                        </td>
                        {/* CLOSING */}
                        <td className={`p-0.5 text-center border-r border-slate-800/60 ${isTarget ? 'bg-emerald-950/20' : ''}`}>
                          <input
                            type="text"
                            value={item.closing !== 0 ? item.closing : ''}
                            onChange={e => handleCellChange(m, p.sn, 'closing', e.target.value)}
                            placeholder="-"
                            className="w-full py-1 px-1 bg-transparent text-center font-mono text-xs text-emerald-300 font-bold focus:bg-slate-950 focus:outline-none"
                          />
                        </td>
                      </React.Fragment>
                    );
                  })}

                  {/* CUMM UNITS */}
                  <td className="p-2 text-center font-mono text-blue-300 bg-purple-950/10">{cummPri || '-'}</td>
                  <td className="p-2 text-center font-mono text-cyan-300 font-bold bg-purple-950/10">{cummSec || '-'}</td>
                  <td className="p-2 text-center font-mono text-emerald-300 font-bold bg-purple-950/10 border-r border-slate-800/60">{cummCl || '-'}</td>

                  {/* TOTAL SEC VAL */}
                  <td className="p-2 text-right font-mono text-emerald-400 font-bold bg-emerald-950/10">
                    {cummSec > 0 ? `₹${Math.round(cummSec * p.pts).toLocaleString()}` : '-'}
                  </td>
                </tr>
              );
            })}
          </tbody>

          {/* Grand Total Footer */}
          <tfoot className="sticky bottom-0 bg-slate-950 border-t-2 border-cyan-500/40 font-bold z-20 shadow-2xl text-[11px]">
            {/* ROW 1: TOTAL UNITS */}
            <tr>
              <td className="p-2.5 text-center text-cyan-400 font-mono border-r border-slate-800">Σ</td>
              <td className="p-2.5 text-white border-r border-slate-800">GRAND TOTAL (UNITS)</td>
              <td className="p-2.5 text-right font-mono text-slate-500 border-r border-slate-800">-</td>
              {MONTH_CODES.map(m => {
                let priSum = 0, secSum = 0, clSum = 0;
                MASTER_PRODUCTS.forEach(p => {
                  const it = gridData[m]?.[p.sn];
                  if (it) {
                    priSum += it.netPri || 0;
                    secSum += it.netSec || 0;
                    clSum += it.closing || 0;
                  }
                });
                return (
                  <React.Fragment key={m}>
                    <td className="p-2 text-center font-mono text-blue-300 bg-blue-950/40">{priSum || '-'}</td>
                    <td className="p-2 text-center font-mono text-cyan-300 bg-cyan-950/40">{secSum || '-'}</td>
                    <td className="p-2 text-center font-mono text-emerald-300 bg-emerald-950/40 border-r border-slate-800">{clSum || '-'}</td>
                  </React.Fragment>
                );
              })}
              <td colSpan={3} className="p-2 text-center text-purple-300 font-mono bg-purple-950/40 border-r border-slate-800">12M Summary</td>
              <td className="p-2 text-right font-mono text-emerald-300 bg-emerald-950/40">-</td>
            </tr>

            {/* ROW 2: TOTAL RUPEES VALUE */}
            <tr>
              <td className="p-2.5 text-center text-emerald-400 font-mono border-r border-slate-800">₹</td>
              <td className="p-2.5 text-white border-r border-slate-800">TOTAL VALUE (RUPEES)</td>
              <td className="p-2.5 text-right font-mono text-slate-500 border-r border-slate-800">-</td>
              {MONTH_CODES.map(m => {
                let secValSum = 0;
                MASTER_PRODUCTS.forEach(p => {
                  const it = gridData[m]?.[p.sn];
                  if (it) {
                    secValSum += (it.netSec || 0) * p.pts;
                  }
                });
                return (
                  <td key={m} colSpan={3} className="p-2 text-center font-mono text-cyan-300 bg-slate-900 border-r border-slate-800">
                    {secValSum > 0 ? `₹${(secValSum / 100000).toFixed(2)}L` : '-'}
                  </td>
                );
              })}
              <td colSpan={4} className="p-2 text-center text-emerald-300 font-mono bg-slate-900">Total HQ Value</td>
            </tr>
          </tfoot>
        </table>
      </div>
    </div>
  );
};
'''
with open("/workspaces/Dios/src/components/review/UnSalesProgSheet.tsx", "w") as f:
    f.write(un_sheet_code)
print("✓ Updated src/components/review/UnSalesProgSheet.tsx with 12-Month Live Engine & Sync!")

# 4. Update DiosWorkspace.tsx to add "Sync to Data Hub (Un. Sales Prog)" button
dios_ws_path = "/workspaces/Dios/src/components/DiosWorkspace.tsx"
with open(dios_ws_path, "r") as f:
    ws_content = f.read()

# Add unProgressionStore import and sync logic
if 'unProgressionStore' not in ws_content:
    ws_content = ws_content.replace(
        "import { exportToExcel } from '../utils/excelExporter';",
        "import { exportToExcel } from '../utils/excelExporter';\nimport { unProgressionStore, MONTH_CODES } from '../data/unProgressionStore';"
    )

    sync_func = '''  // 💾 Sync Aggregated Month to Data Hub (Un. Sales Prog)
  const handleSyncToDataHub = () => {
    const mCode = selectedMonth.substring(0, 3).toUpperCase();
    unProgressionStore.syncFromAggregator(mCode, products);
    alert(`🎉 SUCCESS! Synced ${selectedMonth} (${products.reduce((a,b)=>a+b.netSec,0)} Sales Units, ${products.reduce((a,b)=>a+b.closing,0)} Closing Units) to Data Hub (4. Un. Sales Prog)!`);
  };
'''
    ws_content = ws_content.replace(
        "const handleExport = () => {",
        sync_func + "\n  const handleExport = () => {"
    )

    sync_btn = '''          <button
            onClick={handleSyncToDataHub}
            className="flex items-center gap-1.5 px-3.5 py-2.5 bg-gradient-to-r from-blue-600 to-cyan-600 hover:from-blue-500 hover:to-cyan-500 text-white rounded-xl text-xs font-bold shadow-lg shadow-blue-600/20 transition cursor-pointer"
            title="Save and Push aggregated data into Data Hub Un. Sales Prog"
          >
            <Zap size={15} className="text-yellow-300" /> 💾 Sync to Data Hub
          </button>
'''
    ws_content = ws_content.replace(
        "<button\n            onClick={handleExport}",
        sync_btn + "\n          <button\n            onClick={handleExport}"
    )

    with open(dios_ws_path, "w") as f:
        f.write(ws_content)
    print("✓ Updated DiosWorkspace.tsx with 'Sync to Data Hub' button!")

