import os
import sys
import shutil
import json

LOG_FILE = "/workspaces/Dios/spo_test_output.txt"

def log(msg):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

with open(LOG_FILE, "w", encoding="utf-8") as f:
    f.write("=== SPO AUGUST 2026 EXCEL DATA PARSED ===\n\n")

EXCEL_FILE = "/workspaces/Dios/spo_august_filtered.xls"
XLSX_FILE = "/workspaces/Dios/spo_august_filtered.xlsx"

# Copy as .xlsx
shutil.copyfile(EXCEL_FILE, XLSX_FILE)

try:
    import openpyxl
    wb = openpyxl.load_workbook(XLSX_FILE, data_only=True)
    ws = wb.active
    log(f"📑 Sheet Name: {ws.title}")

    all_rows = list(ws.iter_rows(values_only=True))
    log(f"📊 Total Rows: {len(all_rows)}\n")

    log("--- 📋 COMPLETE ROW-BY-ROW EXCEL DATA ---")
    for idx, row in enumerate(all_rows):
        clean_row = [str(c).strip() if c is not None else "" for c in row]
        if any(clean_row):
            # Print row with index
            log(f"Row [{idx:02d}] -> " + " | ".join(clean_row))

    log("\n" + "="*60)
    log("🎯 COLUMN HEADERS DETECTED")
    log("="*60)
    for idx, row in enumerate(all_rows):
        row_str = " ".join([str(c).upper() for c in row if c])
        if "STOCKIST" in row_str:
            log(f"Header at Row [{idx}]:")
            for col_idx, cell in enumerate(row):
                if cell:
                    log(f"   Col [{col_idx:02d}]: {cell}")
            break

except Exception as e:
    log(f"❌ Error: {str(e)}")

log("\n🏁 Done! All results written to: spo_test_output.txt")
