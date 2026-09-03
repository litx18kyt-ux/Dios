import os
import sys
import time
import shutil
import traceback
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

print("=== CBO SPO EXACT AUGUST EXCEL DOWNLOAD (TARGETED FIX) ===\n")

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
LOGIN_URL = "https://dios.myreporting.net/erp/login"

def run():
    print("🚀 [1/5] Launching Engine...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
        page = context.new_page()
        page.set_default_timeout(35000)
        page.on("dialog", lambda d: d.accept())

        # 1. Login
        print("🔑 [2/5] Logging into CBO...")
        page.goto(LOGIN_URL, timeout=60000, wait_until="domcontentloaded")
        page.wait_for_timeout(1000)
        page.fill("input[type='text']:visible", CBO_USER)
        page.fill("input[type='password']:visible", CBO_PASS)
        page.locator("button:visible:has-text('Login'), input[type='submit']:visible, .btn-success:visible").first.click()

        page.wait_for_url("**/dashboard/home**", timeout=45000)
        page.wait_for_load_state("networkidle")
        page.wait_for_timeout(1500)
        print("✅ Dashboard Ready!")

        # Dismiss any post-login alert if present
        try:
            page.keyboard.press("Escape")
        except Exception:
            pass

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

        page.evaluate('''() => {
            const elms = Array.from(document.querySelectorAll('a, span, li, td'));
            const spo = elms.find(e => (e.innerText || '').trim().includes('SPO Stockist Wise'));
            if (spo) {
                spo.dispatchEvent(new MouseEvent('mouseover', {bubbles: true}));
                spo.click();
                if (spo.parentElement && spo.parentElement.tagName === 'A') spo.parentElement.click();
            }
        }''')
        page.wait_for_timeout(4000)

        # 3. Click the REPORT'S Filter Funnel (.last) - NOT Dashboard's!
        print("🔍 [4/5] Clicking the Report's Filter Funnel Icon (.last)...")
        filter_btn = page.locator("img[src*='filter'], a:has(img[src*='filter']), .fa-filter").last
        filter_btn.click(force=True)
        print("   ✅ Clicked SPO Report Toolbar's Filter Funnel!")

        # 4. Wait for the Screenshot 3 Modal
        print("⏳ Waiting for SPO Stockist Wise Modal...")
        modal = page.locator("ngb-modal-window, div[role='dialog'], .modal").last
        modal.wait_for(state="visible", timeout=15000)
        modal_text = modal.inner_text()
        print(f"🎉 Modal is OPEN! Header Preview: {modal_text[:60]}...")

        # Find all inputs inside this open modal
        inputs = modal.locator("input").all()
        print(f"   Found {len(inputs)} inputs inside SPO Modal")
        for idx, inp in enumerate(inputs[:5]):
            print(f"      Input [{idx}]: val='{inp.get_attribute('value')}' ph='{inp.get_attribute('placeholder')}'")

        # Fill August 2026 Dates
        print("📅 Setting August 2026 Dates (01/08/2026 to 31/08/2026)...")
        if len(inputs) >= 2:
            # From Date
            inputs[0].click()
            inputs[0].fill("01/08/2026")
            inputs[0].dispatch_event("input")
            inputs[0].dispatch_event("change")
            print("   ✅ Set From Date -> 01/08/2026")

            # To Date
            inputs[1].click()
            inputs[1].fill("31/08/2026")
            inputs[1].dispatch_event("input")
            inputs[1].dispatch_event("change")
            print("   ✅ Set To Date   -> 31/08/2026")

        page.wait_for_timeout(500)

        # Click the blue GO button inside the modal
        print("🔘 Clicking GO Button inside modal...")
        go_btn = modal.locator("button#GO, button:has-text('GO'), input[value*='GO'], .btn-primary:has-text('GO')").first
        if go_btn.count() > 0:
            go_btn.click(force=True)
            print("   ✅ Clicked GO button inside modal!")
        else:
            page.keyboard.press("F4")
            print("   ✅ Pressed F4 shortcut!")

        print("⏳ Waiting 8 seconds for August grid to reload...")
        page.wait_for_timeout(8000)

        # 5. Download August Excel File
        print("📥 [5/5] Downloading August Excel...")
        aug_excel = "/workspaces/Dios/spo_august_verified.xls"

        with page.expect_download(timeout=25000) as dl_info:
            excel_btn = page.locator("img[src*='excel'], a:has(img[src*='excel']), .fa-file-excel").last
            excel_btn.click(force=True)

        dl = dl_info.value
        dl.save_as(aug_excel)
        print(f"🎉 SUCCESS! Excel Saved: {aug_excel} ({os.path.getsize(aug_excel)} bytes)")

        browser.close()

    # 6. Parse and Print the Verified August Data
    print("\n" + "="*65)
    print("📊 PARSING AUGUST 2026 VERIFIED EXCEL DATA")
    print("="*65)

    if os.path.exists(aug_excel):
        aug_xlsx = "/workspaces/Dios/spo_august_verified.xlsx"
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

    print("\n🏁 Master Execution Complete! All output in: spo_test_output.txt")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"\n❌ Error:\n{traceback.format_exc()}")
