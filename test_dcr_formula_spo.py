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

print("=== APPLYING DCR SYNCFUSION FORMULA TO SPO STOCKIST WISE ===\n")

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
LOGIN_URL = "https://dios.myreporting.net/erp/login"

def run():
    print("🚀 [1/5] Launching Browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
        page = context.new_page()
        page.set_default_timeout(30000)
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

        # 2. Open Reports -> Sales & Targets -> SPO Stockist Wise
        print("🧭 [3/5] Navigating to SPO Stockist Wise...")
        page.locator("a:has-text('Reports'), span:has-text('Reports'), li:has-text('Reports')").first.click()
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
        page.wait_for_timeout(3000)

        # 3. Ensure Filter Modal is Open
        print("🔍 Checking Filter Dialog status...")
        modal_opened = page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const dialog = document.querySelector(".modal, .popup, [role='dialog'], .e-dialog");
            if (!dialog || !isVis(dialog)) {
                // Click green funnel icon
                const imgs = Array.from(document.querySelectorAll("img, a, button, i")).filter(isVis);
                const filterBtn = imgs.find(e => (e.src || '').includes('filter') || (e.className || '').includes('filter') || (e.getAttribute('title') || '').toLowerCase().includes('filter'));
                if (filterBtn) {
                    filterBtn.click();
                    return "Opened via filter icon click";
                }
                return "Filter icon not found";
            }
            return "Already open";
        }''')
        print(f"   Modal Status: {modal_opened}")
        page.wait_for_timeout(2000)

        # 4. APPLY DCR SYNCFUSION FORMULA
        print("📅 [4/5] Applying DCR Syncfusion DatePickers Formula (01/08/2026 to 31/08/2026)...")
        dcr_formula_res = page.evaluate('''() => {
            // Find all elements with ej2_instances
            const allElements = Array.from(document.querySelectorAll('*')).filter(e => e.ej2_instances && e.ej2_instances.length > 0);
            
            // Filter pickers exactly like server.py DCR code
            const pickers = allElements.filter(e => e.ej2_instances[0].getModuleName && e.ej2_instances[0].getModuleName().toLowerCase().includes('date'));
            
            if (pickers.length >= 2) {
                // In JS: Month is 0-indexed (January=0, August=7)
                const dFrom = new Date(2026, 7, 1);   // 01/08/2026
                const dTo = new Date(2026, 7, 31);   // 31/08/2026

                const oldFrom = pickers[0].ej2_instances[0].value;
                const oldTo = pickers[1].ej2_instances[0].value;

                pickers[0].ej2_instances[0].value = dFrom;
                if (pickers[0].ej2_instances[0].dataBind) pickers[0].ej2_instances[0].dataBind();

                pickers[1].ej2_instances[0].value = dTo;
                if (pickers[1].ej2_instances[0].dataBind) pickers[1].ej2_instances[0].dataBind();

                return "SUCCESS: Pickers Found=" + pickers.length + " | Old: [" + oldFrom + " to " + oldTo + "] -> New: [" + dFrom.toDateString() + " to " + dTo.toDateString() + "]";
            }

            // Fallback diagnostics: list all ej2 module names
            const modules = allElements.map(e => e.ej2_instances[0].getModuleName ? e.ej2_instances[0].getModuleName() : "unknown");
            return "FAILED: Pickers count=" + pickers.length + " | Found ej2 modules: " + JSON.stringify(modules);
        }''')
        print(f"   {dcr_formula_res}")
        page.wait_for_timeout(1000)

        # 5. Click GO Button (Exactly like server.py DCR)
        print("🔘 Clicking GO Button...")
        clicked_go = page.evaluate('''() => {
            const btns = Array.from(document.querySelectorAll('button, input[type=button], input[type=submit], a'));
            const go = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase().includes('GO'));
            if (go) {
                go.click();
                return true;
            }
            return false;
        }''')
        print(f"   GO Clicked: {clicked_go}")

        print("⏳ Waiting 8 seconds for August 2026 data to load in grid...")
        page.wait_for_timeout(8000)

        # 6. Download August Excel (Exactly like server.py DCR)
        print("📥 [5/5] Downloading August Excel...")
        aug_excel = "/workspaces/Dios/spo_august_dcr_formula.xls"

        with page.expect_download(timeout=25000) as dl_info:
            page.evaluate('''() => {
                const elms = Array.from(document.querySelectorAll('a, button, i, span, img'));
                const btn = elms.find(e => {
                    const cls = (e.className || '').toLowerCase();
                    const title = (e.getAttribute('title') || '').toLowerCase();
                    const src = (e.src || '').toLowerCase();
                    return cls.includes('excel') || title.includes('excel') || src.includes('excel') || cls.includes('fa-file-excel');
                });
                if (btn) btn.click();
            }''')

        dl = dl_info.value
        dl.save_as(aug_excel)
        print(f"🎉 Excel Saved: {aug_excel} ({os.path.getsize(aug_excel)} bytes)")

        browser.close()

    # 7. Parse and Verify August Numbers
    print("\n" + "="*65)
    print("📊 PARSING AUGUST 2026 DATA")
    print("="*65)

    if os.path.exists(aug_excel):
        aug_xlsx = "/workspaces/Dios/spo_august_dcr_formula.xlsx"
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
    try:
        run()
    except Exception as e:
        print(f"\n❌ Error:\n{traceback.format_exc()}")
