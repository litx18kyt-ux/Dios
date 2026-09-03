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

print("=== CBO SPO 1000x DEEP FINAL MASTER LOG ===\n")

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
LOGIN_URL = "https://dios.myreporting.net/erp/login"

def run():
    print("🚀 [1/5] Launching Chromium Engine...")
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

        # 3. Check if modal is open; if not open, click the green filter funnel
        page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const dialog = Array.from(document.querySelectorAll("*")).find(e => isVis(e) && (e.innerText || '').includes('From Date'));
            if (!dialog) {
                const imgs = Array.from(document.querySelectorAll("img, a, button, i")).filter(isVis);
                const filterBtn = imgs.find(e => (e.src || '').includes('filter') || (e.className || '').includes('filter') || (e.getAttribute('title') || '').toLowerCase().includes('filter'));
                if (filterBtn) filterBtn.click();
            }
        }''')
        page.wait_for_timeout(2000)

        # 4. Inject August 2026 Dates into the exact inputs holding '/'
        print("📅 [4/5] Injecting August 2026 Dates (01/08/2026 to 31/08/2026)...")
        date_res = page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const allInputs = Array.from(document.querySelectorAll('input')).filter(isVis);
            
            // Look for inputs that have a date format containing '/'
            const dateInputs = allInputs.filter(i => (i.value || '').includes('/') || (i.placeholder || '').toLowerCase().includes('date'));

            if (dateInputs.length >= 2) {
                dateInputs[0].value = "01/08/2026";
                dateInputs[0].dispatchEvent(new Event('input', {bubbles: true}));
                dateInputs[0].dispatchEvent(new Event('change', {bubbles: true}));

                dateInputs[1].value = "31/08/2026";
                dateInputs[1].dispatchEvent(new Event('input', {bubbles: true}));
                dateInputs[1].dispatchEvent(new Event('change', {bubbles: true}));

                return "SUCCESS: Set From=" + dateInputs[0].value + " To=" + dateInputs[1].value;
            } else if (allInputs.length >= 2) {
                allInputs[0].value = "01/08/2026";
                allInputs[0].dispatchEvent(new Event('change', {bubbles: true}));
                allInputs[1].value = "31/08/2026";
                allInputs[1].dispatchEvent(new Event('change', {bubbles: true}));
                return "SUCCESS via top inputs: " + allInputs[0].value + " to " + allInputs[1].value;
            }
            return "FAILED: Inputs found = " + allInputs.length;
        }''')
        print(f"   {date_res}")

        # Syncfusion picker fallback
        page.evaluate('''() => {
            const all = Array.from(document.querySelectorAll('*')).filter(e => e.ej2_instances && e.ej2_instances[0] && e.ej2_instances[0].getModuleName && e.ej2_instances[0].getModuleName() === 'datepicker');
            if (all.length >= 2) {
                all[0].ej2_instances[0].value = new Date(2026, 7, 1);
                if (all[0].ej2_instances[0].dataBind) all[0].ej2_instances[0].dataBind();
                all[1].ej2_instances[0].value = new Date(2026, 7, 31);
                if (all[1].ej2_instances[0].dataBind) all[1].ej2_instances[0].dataBind();
            }
        }''')
        page.wait_for_timeout(1000)

        # 5. Click the Blue 'GO' Button
        print("🔘 Clicking GO Button...")
        clicked_go = page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const btns = Array.from(document.querySelectorAll("button, input[type='button'], a")).filter(isVis);
            const goBtn = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase().includes('GO'));
            if (goBtn) {
                goBtn.click();
                return true;
            }
            return false;
        }''')
        print(f"   GO Click Status: {clicked_go}")

        print("⏳ Waiting 7 seconds for August 2026 grid to reload...")
        page.wait_for_timeout(7000)

        # 6. Download August Excel File
        print("📥 [5/5] Downloading August Excel...")
        aug_excel = "/workspaces/Dios/spo_august_verified.xls"

        with page.expect_download(timeout=25000) as dl_info:
            page.evaluate('''() => {
                const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
                const elms = Array.from(document.querySelectorAll("img, a, button, i")).filter(isVis);
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

    # 7. Parse August Excel
    print("\n" + "="*65)
    print("📊 FINAL VERIFIED AUGUST 2026 NUMBERS")
    print("="*65)

    if os.path.exists(aug_excel):
        aug_xlsx = "/workspaces/Dios/spo_august_verified.xlsx"
        shutil.copyfile(aug_excel, aug_xlsx)

        import openpyxl
        wb = openpyxl.load_workbook(aug_xlsx, data_only=True)
        ws = wb.active

        rows = list(ws.iter_rows(values_only=True))
        date_header = str(rows[2][0] if len(rows) > 2 else "")
        print(f"📅 Excel Header: {date_header[:80]}...\n")

        print(f"{'Stockist Name':<25} | {'Sales (₹)':<12} | {'Return (₹)':<12} | {'Expiry (₹)':<12} | {'Net Sales (₹)':<12}")
        print("-" * 80)

        for r in rows[6:]:
            if not r or not any(r):
                continue
            stk_name = str(r[1] or r[0] or '').strip()
            if any(k in stk_name.upper() for k in ['NAGDA', 'R.P', 'VARDHMAN', 'SUN', 'MODI', 'DWARIKA', 'TOTAL']):
                sales_amt = str(r[4] or '0').strip()
                goods_ret = str(r[5] or '0').strip()
                expiry_ret = str(r[9] or '0').strip()
                net_sales = str(r[14] or '0').strip()

                print(f"{stk_name:<25} | {sales_amt:<12} | {goods_ret:<12} | {expiry_ret:<12} | {net_sales:<12}")

    print("\n🏁 Master Extraction Completed! All details in: spo_test_output.txt")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"\n❌ Error:\n{traceback.format_exc()}")
