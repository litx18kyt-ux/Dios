import os
import sys
import json
from bs4 import BeautifulSoup

LOG_FILE = "/workspaces/Dios/spo_test_output.txt"
JSON_FILE = "/workspaces/Dios/cbo_api_response.json"
MODAL_FILE = "/workspaces/Dios/modal_dump.html"

def log(msg):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

with open(LOG_FILE, "w", encoding="utf-8") as f:
    f.write("=== CBO JSON & MODAL X-RAY DECODER ===\n\n")

# 1. READ CAPTURED CBO API RESPONSES
if os.path.exists(JSON_FILE):
    log("📂 Reading /workspaces/Dios/cbo_api_response.json...")
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        responses = json.load(f)

    log(f"Total API Responses in JSON: {len(responses)}\n")

    for idx, resp in enumerate(responses):
        log("="*65)
        log(f"🔍 INSPECTING RESPONSE [{idx}] - Status: {resp.get('status')}")
        log("="*65)
        data = resp.get("json", {})
        if not data or not isinstance(data, dict):
            continue

        # Check PageCode & Title
        if "PageCode" in data:
            log(f"PageCode: {data.get('PageCode')}")
        if "UIComponentName" in data:
            log(f"UIComponentName: {data.get('UIComponentName')}")

        # Check Filter Data (Exact Field Names!)
        if "FilterData" in data and data["FilterData"]:
            log(f"\n🎯 FilterData (Current Default Values):")
            log(json.dumps(data["FilterData"], indent=2))

        # Check Filter Controls (Exact Labels, Types, IDs)
        if "FilterControlList" in data and data["FilterControlList"]:
            log(f"\n📋 FilterControlList (Controls Metadata):")
            for c in data["FilterControlList"]:
                name = c.get("ControlName") or c.get("Name") or c.get("Field")
                label = c.get("Label") or c.get("DisplayName")
                ctype = c.get("ControlType") or c.get("Type")
                val = c.get("DefaultValue") or c.get("Value")
                log(f"   👉 Control: Name='{name}', Label='{label}', Type='{ctype}', Value='{val}'")

        # Check Tables & Data Rows (Response 3!)
        if "Tables" in data and data["Tables"]:
            log(f"\n📊 TABLES FOUND IN RESPONSE [{idx}]:")
            tables = data["Tables"]
            if isinstance(tables, list):
                for t_idx, tbl in enumerate(tables):
                    log(f"\n--- Table [{t_idx}] ({len(tbl)} rows) ---")
                    for r_idx, row in enumerate(tbl[:8]):
                        log(f"Row [{r_idx}]: {row}")
            elif isinstance(tables, dict):
                for k, v in tables.items():
                    log(f"Table Key '{k}': {len(v) if isinstance(v, list) else type(v)}")
                    if isinstance(v, list) and v:
                        log(f"Sample row: {v[0]}")

        if "List" in data and data["List"]:
            log(f"\n📊 LIST DATA (Rows: {len(data['List'])}):")
            for r_idx, row in enumerate(data["List"][:8]):
                log(f"List Row [{r_idx}]: {row}")

# 2. READ MODAL HTML DUMP (To see exact DatePicker HTML)
if os.path.exists(MODAL_FILE):
    log("\n" + "="*65)
    log("🔬 INSPECTING MODAL HTML DUMP (modal_dump.html)")
    log("="*65)
    with open(MODAL_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")
    inputs = soup.find_all(["input", "select", "ejs-datepicker"])
    log(f"Total Inputs/Pickers found in HTML: {len(inputs)}")
    for inp in inputs:
        tag = inp.name
        itype = inp.get("type", "")
        iid = inp.get("id", "")
        iname = inp.get("name", "")
        ival = inp.get("value", "")
        iph = inp.get("placeholder", "")
        iclass = " ".join(inp.get("class", []))
        log(f"   <{tag} type='{itype}'> id='{iid}' name='{iname}' value='{ival}' placeholder='{iph}' class='{iclass}'")

log("\n🏁 Inspection Complete! Detailed output saved in: spo_test_output.txt")
