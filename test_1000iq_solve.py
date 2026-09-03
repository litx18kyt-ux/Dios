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

print("=== CBO SPO 1000-IQ COMPLETE SOLVER LOG ===\n")

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
LOGIN_URL = "https://dios.myreporting.net/erp/login"

def run():
    print("🚀 [1/6] Launching Chromium Engine...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
        page = context.new_page()
        page.set_default_timeout(30000)
        page.on("dialog", lambda d: d.accept())

        # 1. Login
        print("🔑 [2/6] Logging into CBO...")
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
        print("🧭 [3/6] Navigating to Reports -> Sales & Targets -> SPO Stockist Wise...")
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

        print("⏳ Waiting for SPO Stockist Wise Tab to render...")
        page.wait_for_selector("text=Total Records", timeout=25000)
        print("✅ Report Toolbar ('Total Records') found on screen!")

        # 3. Click the Green Filter Funnel in the Toolbar
        print("🔍 [4/6] Clicking Filter Funnel next to 'Total Records'...")
        funnel_res = page.evaluate('''() => {
            const all = Array.from(document.querySelectorAll('*'));
            const totalRec = all.find(e => (e.innerText || '').includes('Total Records'));
            if (!totalRec) return "ERROR: 'Total Records' not found";

            let toolbar = totalRec;
            for (let i = 0; i < 4; i++) {
                if (!toolbar.parentElement) break;
                toolbar = toolbar.parentElement;
                const filterBtn = toolbar.querySelector("img[src*='filter'], .filter, [title*='Filter']");
                if (filterBtn) {
                    filterBtn.click();
                    if (filterBtn.parentElement && filterBtn.parentElement.tagName === 'A') filterBtn.parentElement.click();
                    return "SUCCESS: Clicked filter funnel icon in toolbar!";
                }
            }
            return "ERROR: Filter icon not found in toolbar";
        }''')
        print(f"   {funnel_res}")

        # Wait for the Screenshot 3 modal to appear
        print("⏳ Waiting for Modal Dialog ('From Date*')...")
        page.wait_for_selector("text=From Date", timeout=15000)
        print("🎉 Screenshot 3 Modal Dialog is OPEN on screen!")

        # 4. Fill August 2026 Dates into Modal
        print("📅 [5/6] Filling August Dates (01/08/2026 to 31/08/2026)...")
        date_fill_res = page.evaluate('''() => {
            const all = Array.from(document.querySelectorAll('*'));
            const fromLabel = all.find(e => (e.innerText || '').trim().startsWith('From Date'));
            if (!fromLabel) return "ERROR: 'From Date' label not found";

            let modal = fromLabel;
            while (modal.parentElement && modal.parentElement !== document.body && modal.offsetWidth < 450) {
                modal = modal.parentElement;
            }

            const inputs = Array.from(modal.querySelectorAll("input"));
            if (inputs.length >= 2) {
                inputs[0].value = "01/08/2026";
                inputs[0].dispatchEvent(new Event('input', {bubbles: true}));
                inputs[0].dispatchEvent(new Event('change', {bubbles: true}));

                inputs[1].value = "31/08/2026";
                inputs[1].dispatchEvent(new Event('input', {bubbles: true}));
                inputs[1].dispatchEvent(new Event('change', {bubbles: true}));

                return "SUCCESS: Set From=" + inputs[0].value + " To=" + inputs[1].value;
            }
            return "ERROR: Inputs count = " + inputs.length;
        }''')
        print(f"   {date_fill_res}")
        page.wait_for_timeout(1000)

        # Click blue 'GO' button inside modal
        print("🔘 Clicking GO button...")
        clicked_go = page.evaluate('''() => {
            const all = Array.from(document.querySelectorAll('*'));
            const fromLabel = all.find(e => (e.innerText || '').trim().startsWith('From Date'));
            let modal = fromLabel ? fromLabel.parentElement : document.body;
            while (modal.parentElement && modal.parentElement !== document.body && modal.offsetWidth < 450) {
                modal = modal.parentElement;
            }
            const btns = Array.from(modal.querySelectorAll("button, input[type='button'], a"));
            const goBtn = btns.find(b => (b.innerText || b.value || '').trim().toUpperCase().includes('GO'));
            if (goBtn) {
                goBtn.click();
                return true;
            }
            return false;
        }''')
        print(f"   GO Clicked: {clicked_go}")

        print("⏳ Waiting 8 seconds for August 2026 data to load in grid...")
        page.wait_for_timeout(8000)

        # 5. Download August Excel
        print("📥 [6/6] Clicking Green Excel Icon in Toolbar...")
        aug_excel = "/workspaces/Dios/spo_august_verified.xls"

        with page.expect_download(timeout=25000) as dl_info:
            page.evaluate('''() => {
                const el = Array.from(document.querySelectorAll('*')).find(e => (e.innerText || '').includes('Total Records'));
                let toolbar = el ? el.parentElement : document;
                for (let i = 0; i < 4; i++) {
                    if (!toolbar.parentElement) break;
                    toolbar = toolbar.parentElement;
                    const excelBtn = toolbar.querySelector("img[src*='excel'], .excel, [title*='Excel'], .fa-file-excel");
                    if (excelBtn) {
                        excelBtn.click();
                        if (excelBtn.parentElement && excelBtn.parentElement.tagName === 'A') excelBtn.parentElement.click();
                        return;
                    }
                }
                const b = Array.from(document.querySelectorAll("img, a, button")).find(e => (e.src || '').includes('excel') || (e.className || '').includes('excel'));
                if (b) b.click();
            }''')

        dl = dl_info.value
        dl.save_as(aug_excel)
        print(f"🎉 Excel Saved: {aug_excel} ({os.path.getsize(aug_excel)} bytes)")

        browser.close()

    # 6. Parse and Print the Final Verified August Numbers
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
        print(f"📅 Excel Header: {date_header[:80]}...\n")

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

    print("\n🏁 Master Extraction Completed! All details in: spo_test_output.txt")

if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        print(f"\n❌ Execution Error:\n{traceback.format_exc()}")
