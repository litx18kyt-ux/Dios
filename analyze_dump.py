import os
import sys
import json
import re
from bs4 import BeautifulSoup

LOG_FILE = "/workspaces/Dios/spo_test_output.txt"
HTML_FILE = "/workspaces/Dios/full_cbo_page.html"
JSON_FILE = "/workspaces/Dios/cbo_api_response.json"

def log(msg):
    print(msg)
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(msg + "\n")

with open(LOG_FILE, "w", encoding="utf-8") as f:
    f.write("=== CBO INTERNAL ARCHITECTURE & API X-RAY ===\n\n")

# 1. READ HTML DUMP (282 KB)
if os.path.exists(HTML_FILE):
    log(f"📄 Reading {HTML_FILE} ({os.path.getsize(HTML_FILE)} bytes)...")
    with open(HTML_FILE, "r", encoding="utf-8") as f:
        html = f.read()

    soup = BeautifulSoup(html, "html.parser")

    # Find all custom <cbo-...> tags
    cbo_tags = list(set([tag.name for tag in soup.find_all(re.compile(r'^cbo-'))]))
    log(f"\n🧩 Custom CBO Angular Components ({len(cbo_tags)}):")
    for t in cbo_tags:
        log(f"   <{t}>")

    # Find where SPO Stockist Wise is in the HTML
    log("\n🔍 Searching for 'SPO Stockist Wise' in HTML:")
    spo_elms = soup.find_all(lambda tag: 'SPO Stockist Wise' in tag.get_text() and len(tag.find_all()) <= 2)
    for idx, el in enumerate(spo_elms[:3]):
        log(f"   Match [{idx}] <{el.name}>: class='{el.get('class')}' id='{el.get('id')}'")
        if el.parent:
            log(f"      Parent <{el.parent.name}>: class='{el.parent.get('class')}' href='{el.parent.get('href')}'")
            log(f"      HTML snippet: {str(el.parent)[:200]}")

    # Check bottom tab bar (like Screenshot 1 & 2)
    log("\n📑 Tabs rendered in the DOM:")
    tab_elms = soup.find_all(class_=re.compile(r'tab|nav-link|footer-tab', re.I))
    for t in tab_elms[:5]:
        txt = t.get_text(strip=True)
        if txt:
            log(f"   Tab: '{txt}' <{t.name}> class='{t.get('class')}'")

# 2. READ CAPTURED API JSON (Table Data!)
if os.path.exists(JSON_FILE):
    log("\n" + "="*65)
    log("📊 EXTRACTING DATA FROM /workspaces/Dios/cbo_api_response.json")
    log("="*65)
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        api_data = json.load(f)

    for idx, resp in enumerate(api_data):
        d = resp.get("json", {})
        if not d or not isinstance(d, dict):
            continue

        tables = d.get("Tables", {})
        if "MUTIPLEMONTH" in tables:
            log(f"\n🎯 FOUND 'MUTIPLEMONTH' TABLE IN API RESPONSE [{idx}] ({len(tables['MUTIPLEMONTH'])} rows):")
            for r in tables["MUTIPLEMONTH"]:
                month = r.get("X_AXIS") or r.get("MONTH")
                series = r.get("SERIES")
                val = r.get("VALUE")
                ach = r.get("ACH")
                page_code = r.get("PAGE_CODE")
                log(f"   📅 Month: {month:<8} | Series: {series:<35} | Value: {val:<8} Lacs | Ach: {ach}%")

        if "YEARLY" in tables:
            log(f"\n🎯 FOUND 'YEARLY' TABLE:")
            for r in tables["YEARLY"]:
                log(f"   YTD: {r.get('X_AXIS')} | Series: {r.get('SERIES')} | Value: {r.get('VALUE')} Lacs")

        if "DIVISIONWISESALE" in tables:
            log(f"\n🎯 FOUND 'DIVISIONWISESALE' TABLE:")
            for r in tables["DIVISIONWISESALE"]:
                log(f"   Division: {r.get('X_AXIS')} | Series: {r.get('SERIES')} | Value: ₹{r.get('VALUE'):,}")

log("\n🏁 Done! Results written to: spo_test_output.txt")
