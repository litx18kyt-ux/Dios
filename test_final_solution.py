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

print("=== CBO SPO MASTER FINAL EXTRACTION LOG ===\n")

CBO_USER = os.getenv("CBO_USER", "6958BANWARI")
CBO_PASS = os.getenv("CBO_PASS", "6958")
LOGIN_URL = "https://dios.myreporting.net/erp/login"

def run():
    print("🚀 [1/5] Launching Chromium Browser...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True, args=['--no-sandbox', '--disable-setuid-sandbox'])
        context = browser.new_context(viewport={"width": 1440, "height": 900}, accept_downloads=True)
        page = context.new_page()
        page.set_default_timeout(25000)
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

        # 3. Check / Open Filter Dialog directly
        print("📅 [4/5] Interacting with Filter Modal (Screenshot 3)...")
        
        # Check if dialog is open; if not open, click the green filter funnel
        modal_status = page.evaluate('''() => {
            const isVis = el => el && (el.offsetWidth > 0 || el.offsetHeight > 0);
            const dialog = document.querySelector(".modal, .popup, [role='dialog'], .e-dialog");
            if (!dialog || !isVis(dialog)) {
                const icons = Array.from(document.querySelectorAll("img, a, button, i")).filter(isVis);
                const funnel = icons.find(e => (e.src || '').includes('filter') || (e.className || '').includes('filter') || (e.getAttribute('title') || '').toLowerCase().includes('filter'));
                if (funnel) {
                    funnel.click();
                    return "Opened modal via funnel icon";
                }
                return "Modal already open or funnel not found";
            }
            return "Modal is open";
        }''')
        print(f"   Modal status: {modal_status}")
        page.wait_for_timeout(2000)

        # 4. Inject August 2026 Dates directly into Syncfusion pickers & inputs
        date_inject_res = page.evaluate('''() => {
            // Method A: Syncfusion ej2_instances
            const allElements = Array.from(document.querySelectorAll('*')).filter(e => e.ej2_instances && e.ej2_instances.length > 0);
            const pickers = allElements.filter(e => e.ej2_instances[0].getModuleName && e.ej2_instances[0].getModuleName() === 'datepicker');
            
            let syncSuccess = false;
            if (pickers.length >= 2) {
                const dFrom = new Date(2026, 7, 1);   // Aug 1, 2026
                const dTo = new Date(2026, 7, 31);   // Aug 31, 2026

                pickers[0].ej2_instances[0].value = dFrom;
                if (pickers[0].ej2_instances[0].dataBind) pickers[0].ej2_instances[0].dataBind();

                pickers[1].ej2_instances[0].value = dTo;
                if (pickers[1].ej2_instances[0].dataBind) pickers[1].ej2_instances[0].dataBind();
                syncSuccess = true;
            }

            // Method B: Set input values
            const inputs = Array.from(document.querySelectorAll("input"));
            const dateInps = inputs.filter(i => (i.value || '').includes('/') || (i.name || i.id || '').toLowerCase().includes('date'));
            if (dateInps.length >= 2) {
                dateInps[0].value = "01/08/2026";
                dateInps[0].dispatchEvent(new Event('input', {bubbles: true}));
                dateInps[0].dispatchEvent(new Event('change', {bubbles: true}));

                dateInps[1].value = "31/08/2026";
                dateInps[1].dispatchEvent(new Event('input', {bubbles: true}));
                dateInps[1].dispatchEvent(new Event('change', {bubbles: true}));
            }

            return syncSuccess ? "SUCCESS via Syncfusion Pickers!" : ("Set via " + dateInps.length + " date inputs");
        }''')
        print(f"   Date Injection: {date_inject_res}")
        page.wait_for_timeout(1000)

        # 5. Click the blue 'GO' button inside the modal
        print("🔘 Clicking GO button...")
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
        print(f"   GO Clicked: {clicked_go}")

        print("⏳ Waiting 8 seconds for August 2026 data to load in grid...")
        page.wait_for_timeout(8000)

        # 6. Download the August Excel File via Green Excel Icon
        print("📥 [5/5] Downloading August Excel...")
        aug_excel = "/workspaces/Dios/spo_august_final.xls"

        with page.expect_download(timeout=25000) as dl_info:
            page.evaluate('''() => {
                const elms = Array.from(document.querySelectorAll("a, button, img, i"));
                const excelBtn = elms.find(e => {
                    const cls = (e.className || '').toLowerCase();
                    const title = (e.getAttribute('title') || '').toLowerCase();
                    const src = (e.src || '').toLowerCase();
                    return cls.includes('excel') || title.includes('excel') || src.includes('excel') || cls.includes('fa-file-excel');
                });
                if (excelBtn) {
                    excelBtn.click();
                    if (excelBtn.parentElement && excelBtn.parentElement.tagName === 'A') excelBtn.parentElement.click();
                }
            }''')
        
        dl = dl_info.value
        dl.save_as(aug_excel)
        print(f"🎉 SUCCESS! File downloaded to: {aug_excel} ({os.path.getsize(aug_excel)} bytes)")

        browser.close()

    # 7. Open and Parse August 2026 Numbers
    print("\n" + "="*65)
    print("📊 PARSING AUGUST 2026 CBO DATA")
    print("="*65)

    if os.path.exists(aug_excel):
        aug_xlsx = "/workspaces/Dios/spo_august_final.xlsx"
        shutil.copyfile(aug_excel, aug_xlsx)

        import openpyxl
        wb = openpyxl.load_workbook(aug_xlsx, data_only=True)
        ws = wb.active

        rows = list(ws.iter_rows(values_only=True))
        date_header = str(rows[2][0] if len(rows) > 2 else "")
        print(f"📅 Excel Header Range: {date_header[:80]}...\n")

        print(f"{'Stockist Name':<25} | {'Sales (₹)':<12} | {'Return (₹)':<12} | {'Expiry (₹)':<12} | {'Net Sales (₹)':<12}")
        print("-" * 80)

        for r in rows[6:]:
            if not r or not any(r):
                continue
            stk_name = str(r[1] or '').strip()
            if not stk_name:
                stk_name = str(r[0] or '').strip()

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
        print(f"\n❌ Execution Error:\n{traceback.format_exc()}")
