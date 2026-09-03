import os
import sys
import time
import shutil
import json
import re
from playwright.sync_api import sync_playwright

LOG_FILE = "/workspaces/Dios/spo_test_output.txt"

class TeeLogger:
    def __init__(self, filename):
        self.terminal = sys.stdout
        self.logfile = open(filename, "w", encoding="utf-8")

    def write(self, message):
        self.terminal.write(message)
        self.terminal.flush()
        self.logfile.write(message)
        self.logfile.flush()

    def flush(self):
        self.terminal.flush()
        self.logfile.flush()

sys.stdout = TeeLogger(LOG_FILE)
sys.stderr = sys.stdout

print("=== CBO SPO 10,000-IQ NETWORK REWRITER ENGINE ===\n")

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
LOGIN_URL = "https://dios.myreporting.net/erp/login"

def run():
    print("🚀 [1/5] Launching Engine with In-Flight HTTP Rewriter...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
        page = context.new_page()
        page.set_default_timeout(35000)

        # ⚡ IN-FLIGHT NETWORK ROUTE REWRITER
        # Catch any request going to /api/common/apirequest and rewrite September -> August
        def route_handler(route):
            req = route.request
            if "apirequest" in req.url and req.method == "POST":
                original_body = req.post_data or ""
                
                # Check if this request contains dates or month info
                needs_rewrite = any(k in original_body for k in ['01/09/2026', '03/09/2026', '2026-09', 'Sep', 'SEP'])
                
                if needs_rewrite:
                    # Rewrite to August 2026 (01/08/2026 to 31/08/2026)
                    new_body = original_body
                    new_body = new_body.replace("01/09/2026", "01/08/2026")
                    new_body = new_body.replace("03/09/2026", "31/08/2026")
                    new_body = new_body.replace("2026-09-01", "2026-08-01")
                    new_body = new_body.replace("2026-09-03", "2026-08-31")
                    new_body = new_body.replace("September-2026", "August-2026")
                    new_body = new_body.replace("Sep-2026", "Aug-2026")
                    new_body = new_body.replace("Sep", "Aug")
                    
                    print(f"\n⚡ [INTERCEPTOR] In-Flight Payload Rewritten to AUGUST!")
                    print(f"   Original Preview: {original_body[:120]}...")
                    print(f"   Modified Preview: {new_body[:120]}...")
                    
                    # Forward modified payload with original headers
                    route.continue_(post_data=new_body)
                    return
                else:
                    if len(original_body) > 0:
                        print(f"ℹ️ [API PASS] {req.method} {req.url} (Body: {original_body[:80]}...)")
            
            route.continue_()

        page.route("**/api/common/apirequest", route_handler)

        # 1. Login
        print("🔑 [2/5] Logging in to CBO...")
        page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(1000)
        page.fill("input[type='text']:visible", CBO_USER)
        page.fill("input[type='password']:visible", CBO_PASS)
        page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first.click()

        page.wait_for_url("**/dashboard/home**", timeout=45000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1500)
        print("✅ Dashboard Ready!")

        # 2. Open Reports -> Sales & Targets -> SPO Stockist Wise
        print("🧭 [3/5] Navigating to SPO Stockist Wise...")
        page.locator("a:has-text('Reports'), span:has-text('Reports')").first.click()
        page.wait_for_timeout(600)

        page.evaluate('''() => {
            const elms = Array.from(document.querySelectorAll('a, span, li, td'));
            const st = elms.find(e => (e.innerText || '').trim() === 'Sales & Targets');
            if (st) {
                st.dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
                st.dispatchEvent(new MouseEvent('mouseenter', {bubbles: true}));
                st.click();
            }
        }''')
        page.wait_for_timeout(600)

        # Click SPO Stockist Wise
        page.evaluate('''() => {
            const elms = Array.from(document.querySelectorAll('a, span, li, td'));
            const spo = elms.find(e => (e.innerText || '').trim().includes('SPO Stockist Wise'));
            if (spo) {
                spo.dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
                spo.click();
                if (spo.parentElement && spo.parentElement.tagName === 'A') spo.parentElement.click();
            }
        }''')
        page.wait_for_timeout(3500)

        # 3. Trigger Refresh / Reload Icon if report is on screen
        print("🔄 [4/5] Triggering Refresh to force API reload with rewritten August dates...")
        page.evaluate('''() => {
            // Click the refresh icon next to Excel
            const imgs = Array.from(document.querySelectorAll("img, a, button"));
            const ref = imgs.find(e => (e.src || '').includes('refresh') || (e.getAttribute('title') || '').toLowerCase().includes('refresh') || (e.className || '').includes('refresh'));
            if (ref) {
                ref.click();
                if (ref.parentElement && ref.parentElement.tagName === 'A') ref.parentElement.click();
            }
        }''')
        page.wait_for_timeout(7000)

        # 4. Download Excel via Green Excel Icon
        print("📥 [5/5] Downloading Generated Excel...")
        aug_excel = "/workspaces/Dios/spo_august_network_hack.xls"

        with page.expect_download(timeout=25000) as dl_info:
            page.evaluate('''() => {
                const elms = Array.from(document.querySelectorAll("img, a, button"));
                const excelBtn = elms.find(e => {
                    const src = (e.src || '').toLowerCase();
                    const cls = (e.className || '').toLowerCase();
                    const title = (e.getAttribute('title') || '').toLowerCase();
                    return src.includes('excel') || cls.includes('excel') || title.includes('excel') || cls.includes('fa-file-excel');
                });
                if (excelBtn) {
                    excelBtn.click();
                    if (excelBtn.parentElement && excelBtn.parentElement.tagName === 'A') excelBtn.parentElement.click();
                }
            }''')

        dl = dl_info.value
        dl.save_as(aug_excel)
        print(f"🎉 Excel Saved: {aug_excel} ({os.path.getsize(aug_excel)} bytes)")

        browser.close()

    # 5. Parse and Inspect
    print("\n" + "="*65)
    print("📊 PARSING AUGUST 2026 DATA")
    print("="*65)

    if os.path.exists(aug_excel):
        aug_xlsx = "/workspaces/Dios/spo_august_network_hack.xlsx"
        shutil.copyfile(aug_excel, aug_xlsx)

        import openpyxl
        wb = openpyxl.load_workbook(aug_xlsx, data_only=True)
        ws = wb.active

        rows = list(ws.iter_rows(values_only=True))
        date_header = str(rows[2][0] if len(rows) > 2 else "")
        print(f"📅 Excel Date Range: {date_header[:80]}...\n")

        print(f"{'Stockist Name':<25} | {'Sales (₹)':<12} | {'Return (₹)':<12} | {'Expiry (₹)':<12} | {'Net Sales (₹)':<12}")
        print("-" * 80)

        for r in rows[6:]:
            if not r or not any(r):
                continue
            name = str(r[1] or r[0] or '').strip()
            if any(k in name.upper() for k in ['NAGDA', 'R.P', 'VARDHMAN', 'SUN', 'MODI', 'DWARIKA', 'TOTAL']):
                sales_amt = str(r[4] or '0').strip()
                goods_ret = str(r[5] or '0').strip()
                expiry_ret = str(r[9] or '0').strip()
                net_sales = str(r[14] or '0').strip()

                print(f"{name:<25} | {sales_amt:<12} | {goods_ret:<12} | {expiry_ret:<12} | {net_sales:<12}")

    print("\n🏁 Done! All results written to: spo_test_output.txt")

if __name__ == "__main__":
    run()
